"""Signaux du compte destinataire, calculés par lot : passé uniquement, sans soldes.

Le même code tourne sur CPU (numpy) et sur GPU (cupy). Le calcul en ligne, transfert par
transfert, est dans magasin.py ; tests/ vérifie que les deux donnent les mêmes valeurs.
"""
import numpy as np
import pandas as pd

from .config import JOUR

K = 1 << 23   # > durée totale en secondes (31 jours = 2 678 400)

NOMS = [
    "montant", "premier_contact", "dst_anciennete_j", "dst_nb_recus", "dst_nb_recus_24h",
    "dst_somme_recue_24h", "dst_nouveaux_exp_24h", "dst_nouveaux_exp_72h", "dst_part_nouveaux_exp",
    "dst_nb_sorties", "dst_ratio_sorties_entrees", "dst_sorties_rapides", "dst_part_sorties_rapides",
    "dst_min_depuis_entree", "montant_vs_habitude_dst", "src_anciennete_j", "src_nb_envois",
    "src_nb_envois_10min", "src_recu_30min_vs_montant",
]


class Histo:
    """Événements d'un compte triés par (compte, t). Répond : combien, quelle somme, AVANT t."""
    def __init__(self, xp, compte, t, valeur=None):
        cle = compte * K + t
        o = xp.argsort(cle)
        self.xp, self.cle = xp, cle[o]
        v = xp.ones(len(cle)) if valeur is None else valeur[o].astype(xp.float64)
        self.cs = xp.concatenate([xp.zeros(1), xp.cumsum(v)])
    def bornes(self, compte, t, fenetre=None):
        xp = self.xp
        depuis = 0 if fenetre is None else xp.maximum(t - fenetre, 0)
        lo = xp.searchsorted(self.cle, compte * K + depuis, side="left")
        hi = xp.searchsorted(self.cle, compte * K + t, side="left")     # strictement avant t
        return lo, hi
    def nb(self, compte, t, fenetre=None):
        lo, hi = self.bornes(compte, t, fenetre); return (hi - lo).astype(self.xp.float32)
    def somme(self, compte, t, fenetre=None):
        lo, hi = self.bornes(compte, t, fenetre); return self.cs[hi] - self.cs[lo]
    def depuis_dernier(self, compte, t):          # -1 si aucun événement passé
        lo, hi = self.bornes(compte, t)
        dernier = self.cle[self.xp.maximum(hi - 1, 0)] % K
        return self.xp.where(hi > lo, t - dernier, -1).astype(self.xp.float32)
    def depuis_premier(self, compte, t):          # ancienneté ; -1 si compte jamais vu
        lo, hi = self.bornes(compte, t)
        premier = self.cle[self.xp.minimum(lo, len(self.cle) - 1)] % K
        return self.xp.where(hi > lo, t - premier, -1).astype(self.xp.float32)


def rang_dans_paire(xp, s, d, t):
    """Nombre de transferts déjà faits de s vers d avant celui-ci."""
    paire = s * (1 << 24) + d
    o = np.lexsort((t, paire)) if xp is np else xp.lexsort(xp.stack([t, paire]))
    p = paire[o]
    rang = xp.empty(len(p), dtype=xp.int64)
    rang[o] = xp.arange(len(p)) - xp.searchsorted(p, p, side="left")
    return rang


def signaux(xp, t, src, dst, montant, est_tr, est_sortie):
    """Une ligne de signaux par TRANSFERT (le moment où Sentinelle note le destinataire)."""
    t, src, dst, a = (xp.asarray(v) for v in (t, src, dst, montant))
    tr, so = xp.asarray(est_tr), xp.asarray(est_sortie)
    T, S, D, A = t[tr], src[tr], dst[tr], a[tr]
    premier_contact = (rang_dans_paire(xp, S, D, T) == 0)
    vu      = Histo(xp, xp.concatenate([src, dst]), xp.concatenate([t, t]))   # toute activité
    entree  = Histo(xp, D, T, A)                                # transferts reçus
    neuf    = Histo(xp, D, T, premier_contact)                  # ... venant d'un expéditeur jamais vu
    sortie  = Histo(xp, src[so], t[so], a[so])                  # transferts envoyés et retraits
    rapide  = Histo(xp, src[so], t[so], entree.nb(src[so], t[so], 1800) > 0)  # sortie < 30 min après une entrée
    envoi   = Histo(xp, S, T, A)                                # transferts envoyés seulement
    nb_in, nb_out, som_in = entree.nb(D, T), sortie.nb(D, T), entree.somme(D, T)
    # Pas de signal « heure » : nos scénarios sont injectés à toute heure, PaySim non. Ce serait un artefact.
    f = {
        "montant": A,
        "premier_contact": premier_contact,
        "dst_anciennete_j": xp.where(vu.depuis_premier(D, T) < 0, -1, vu.depuis_premier(D, T) / JOUR),
        "dst_nb_recus": nb_in,
        "dst_nb_recus_24h": entree.nb(D, T, JOUR),
        "dst_somme_recue_24h": entree.somme(D, T, JOUR),
        "dst_nouveaux_exp_24h": neuf.somme(D, T, JOUR),
        "dst_nouveaux_exp_72h": neuf.somme(D, T, 3 * JOUR),
        "dst_part_nouveaux_exp": neuf.somme(D, T) / xp.maximum(nb_in, 1),
        "dst_nb_sorties": nb_out,
        "dst_ratio_sorties_entrees": sortie.somme(D, T) / (som_in + 1),
        "dst_sorties_rapides": rapide.somme(D, T),
        "dst_part_sorties_rapides": rapide.somme(D, T) / xp.maximum(nb_out, 1),
        "dst_min_depuis_entree": entree.depuis_dernier(D, T) / 60,
        "montant_vs_habitude_dst": xp.where(nb_in > 0, A * nb_in / (som_in + 1), -1),
        "src_anciennete_j": xp.where(vu.depuis_premier(S, T) < 0, -1, vu.depuis_premier(S, T) / JOUR),
        "src_nb_envois": envoi.nb(S, T),
        "src_nb_envois_10min": envoi.nb(S, T, 600),
        "src_recu_30min_vs_montant": entree.somme(S, T, 1800) / (A + 1),
    }
    assert list(f) == NOMS
    vers_np = (lambda v: v) if xp is np else xp.asnumpy
    return pd.DataFrame({k: vers_np(v).astype(np.float32) for k, v in f.items()})


def preparer_evenements(tout):
    """Transforme le tableau des transactions en tableaux numériques pour signaux()."""
    codes, comptes = pd.factorize(pd.concat([tout["src"], tout["dst"]], ignore_index=True))
    assert len(comptes) < (1 << 24) and int(tout["t"].max()) < K
    n = len(tout)
    return dict(t=tout["t"].to_numpy(np.int64), src=codes[:n].astype(np.int64), dst=codes[n:].astype(np.int64),
                montant=tout["montant"].to_numpy(np.float64),
                est_tr=(tout["type"] == "TRANSFER").to_numpy(),
                est_sortie=tout["type"].isin(["TRANSFER", "CASH_OUT"]).to_numpy())
