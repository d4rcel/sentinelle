"""Historique des comptes en mémoire et calcul des signaux en ligne, un transfert à la fois.

C'est ce que le service utilise au moment où l'expéditeur s'apprête à confirmer.
Les valeurs sont les mêmes que celles du calcul par lot de signaux.py (vérifié par les tests) :
seuls les événements strictement antérieurs à t comptent.
"""
from bisect import bisect_left, bisect_right

from .config import JOUR
from .signaux import NOMS


class _Compte:
    __slots__ = ("premier", "in_t", "in_m", "in_neuf", "out_t", "out_m", "out_rapide", "env_t")

    def __init__(self):
        self.premier = None                                   # première activité connue
        self.in_t, self.in_m, self.in_neuf = [], [], []        # transferts reçus
        self.out_t, self.out_m, self.out_rapide = [], [], []   # transferts envoyés et retraits
        self.env_t = []                                       # transferts envoyés seulement


_VIDE = _Compte()


def _inserer(t, temps, *listes_valeurs):
    i = bisect_right(temps, t)
    temps.insert(i, t)
    for liste, valeur in listes_valeurs:
        liste.insert(i, valeur)


class Magasin:
    """Tout ce que Sentinelle sait des comptes à un instant donné."""

    def __init__(self):
        self.comptes = {}
        self.paires = {}     # (expéditeur, destinataire) -> nombre de transferts déjà faits
        self.horloge = 0     # temps du dernier événement enregistré, en secondes
        self.nb_evenements = 0

    def _compte(self, nom):
        c = self.comptes.get(nom)
        if c is None:
            c = self.comptes[nom] = _Compte()
        return c

    def ajouter(self, t, type_, montant, src, dst):
        """Enregistre une opération confirmée. Seuls TRANSFER et CASH_OUT nourrissent les flux."""
        t, montant = int(t), float(montant)
        cs, cd = self._compte(src), self._compte(dst)
        for c in (cs, cd):
            if c.premier is None or t < c.premier:
                c.premier = t
        if type_ in ("TRANSFER", "CASH_OUT"):
            lo = bisect_left(cs.in_t, max(t - 1800, 0))
            rapide = bisect_left(cs.in_t, t) > lo             # sortie moins de 30 min après une entrée
            _inserer(t, cs.out_t, (cs.out_m, montant), (cs.out_rapide, 1.0 if rapide else 0.0))
        if type_ == "TRANSFER":
            deja = self.paires.get((src, dst), 0)
            self.paires[(src, dst)] = deja + 1
            _inserer(t, cd.in_t, (cd.in_m, montant), (cd.in_neuf, 1.0 if deja == 0 else 0.0))
            _inserer(t, cs.env_t)
        self.horloge = max(self.horloge, t)
        self.nb_evenements += 1

    def charger(self, lignes):
        """lignes : itérable de (t, type, montant, src, dst), dans l'ordre du temps."""
        for t, type_, montant, src, dst in lignes:
            self.ajouter(t, type_, montant, src, dst)
        return self

    def signaux(self, t, src, dst, montant):
        """Signaux d'un transfert de `montant` de src vers dst au temps t, AVANT qu'il soit confirmé."""
        t, a = int(t), float(montant)
        cs, cd = self.comptes.get(src, _VIDE), self.comptes.get(dst, _VIDE)

        def anciennete(c):
            return -1.0 if c.premier is None or c.premier >= t else (t - c.premier) / JOUR

        hi = bisect_left(cd.in_t, t)
        lo24 = bisect_left(cd.in_t, max(t - JOUR, 0))
        lo72 = bisect_left(cd.in_t, max(t - 3 * JOUR, 0))
        nb_in, som_in = hi, sum(cd.in_m[:hi])
        ho = bisect_left(cd.out_t, t)
        nb_out, rapides = ho, sum(cd.out_rapide[:ho])
        he = bisect_left(cs.env_t, t)
        hs, ls = bisect_left(cs.in_t, t), bisect_left(cs.in_t, max(t - 1800, 0))
        f = {
            "montant": a,
            "premier_contact": 1.0 if self.paires.get((src, dst), 0) == 0 else 0.0,
            "dst_anciennete_j": anciennete(cd),
            "dst_nb_recus": float(nb_in),
            "dst_nb_recus_24h": float(hi - lo24),
            "dst_somme_recue_24h": sum(cd.in_m[lo24:hi]),
            "dst_nouveaux_exp_24h": sum(cd.in_neuf[lo24:hi]),
            "dst_nouveaux_exp_72h": sum(cd.in_neuf[lo72:hi]),
            "dst_part_nouveaux_exp": sum(cd.in_neuf[:hi]) / max(nb_in, 1),
            "dst_nb_sorties": float(nb_out),
            "dst_ratio_sorties_entrees": sum(cd.out_m[:ho]) / (som_in + 1),
            "dst_sorties_rapides": rapides,
            "dst_part_sorties_rapides": rapides / max(nb_out, 1),
            "dst_min_depuis_entree": ((t - cd.in_t[hi - 1]) if hi else -1) / 60,
            "montant_vs_habitude_dst": a * nb_in / (som_in + 1) if nb_in else -1.0,
            "src_anciennete_j": anciennete(cs),
            "src_nb_envois": float(he),
            "src_nb_envois_10min": float(he - bisect_left(cs.env_t, max(t - 600, 0))),
            "src_recu_30min_vs_montant": sum(cs.in_m[ls:hs]) / (a + 1),
        }
        assert list(f) == NOMS
        return f

    def resume(self, compte, t=None):
        """Ce que l'on sait d'un compte, pour l'affichage."""
        c = self.comptes.get(compte)
        if c is None:
            return {"compte": compte, "connu": False}
        t = self.horloge + 1 if t is None else int(t)
        hi, ho = bisect_left(c.in_t, t), bisect_left(c.out_t, t)
        return {
            "compte": compte, "connu": True,
            "anciennete_jours": None if c.premier is None or c.premier >= t else round((t - c.premier) / JOUR, 1),
            "transferts_recus": hi, "somme_recue": round(sum(c.in_m[:hi]), 2),
            "sorties": ho, "somme_sortie": round(sum(c.out_m[:ho]), 2),
            "sorties_rapides": int(sum(c.out_rapide[:ho])),
        }
