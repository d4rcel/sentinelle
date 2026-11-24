"""La raison lisible : traduit les signaux qui pèsent le plus en phrases vraies pour ce transfert."""


def _n(v):
    return int(round(v))


def _montant(v):
    return f"{v:,.0f}".replace(",", " ")


def _jours(v):
    return "moins d'un jour" if v < 1 else ("1 jour" if v < 2 else f"{int(v)} jours")


def _phrase(nom, s, montant_eleve):
    """Phrase pour un signal, ou None si elle ne serait pas vraie avec la valeur observée."""
    v = s[nom]
    if nom == "premier_contact":
        return "l'expéditeur n'a jamais envoyé d'argent à ce compte" if v == 1 else None
    if nom == "dst_anciennete_j":
        if v < 0:
            return "ce compte n'a aucune activité connue avant ce transfert"
        return f"ce compte n'est actif que depuis {_jours(v)}" if v < 15 else None
    if nom == "dst_nb_recus":
        return "ce compte n'a encore jamais reçu de transfert" if v == 0 else None
    if nom == "dst_nb_recus_24h":
        return f"ce compte a reçu {_n(v)} transferts en 24 heures" if v >= 2 else None
    if nom == "dst_somme_recue_24h":
        return f"ce compte a reçu {_montant(v)} en 24 heures" if v > 0 else None
    if nom == "dst_nouveaux_exp_24h":
        return f"ce compte a reçu de l'argent de {_n(v)} nouveaux expéditeurs en 24 heures" if v >= 2 else None
    if nom == "dst_nouveaux_exp_72h":
        return f"ce compte a reçu de l'argent de {_n(v)} nouveaux expéditeurs en 3 jours" if v >= 2 else None
    if nom == "dst_part_nouveaux_exp":
        ok = v >= 0.8 and s["dst_nb_recus"] >= 2
        return "presque tous ceux qui paient ce compte ne l'ont fait qu'une fois" if ok else None
    if nom == "dst_nb_sorties":
        return f"ce compte a déjà fait sortir de l'argent {_n(v)} fois" if v >= 2 else None
    if nom == "dst_ratio_sorties_entrees":
        return "ce compte ne garde presque rien de ce qu'il reçoit" if v >= 0.8 else None
    if nom == "dst_sorties_rapides":
        if v < 1:
            return None
        fois = "une fois" if _n(v) == 1 else f"{_n(v)} fois"
        return f"ce compte a déjà vidé des fonds moins de 30 minutes après les avoir reçus ({fois})"
    if nom == "dst_part_sorties_rapides":
        return "ce compte vide presque toujours les fonds dès qu'il les reçoit" if v >= 0.5 else None
    if nom == "dst_min_depuis_entree":
        if not 0 <= v <= 60:
            return None
        return "ce compte vient de recevoir un autre transfert" if v < 1 else f"ce compte a reçu un autre transfert il y a {_n(v)} min"
    if nom == "montant_vs_habitude_dst":
        return "le montant est bien plus élevé que ce que ce compte reçoit d'habitude" if v >= 3 else None
    if nom == "montant":
        return "le montant est élevé" if montant_eleve is not None and v >= montant_eleve else None
    if nom == "src_anciennete_j":
        return "le compte expéditeur n'a aucune activité connue" if v < 0 else None
    if nom == "src_nb_envois":
        return f"l'expéditeur a déjà envoyé {_n(v)} transferts" if v >= 3 else None
    if nom == "src_nb_envois_10min":
        return f"l'expéditeur enchaîne les transferts : {_n(v) + 1} en moins de 10 minutes" if v >= 1 else None
    if nom == "src_recu_30min_vs_montant":
        return "l'expéditeur vient lui-même de recevoir de l'argent, qu'il fait suivre aussitôt" if v > 0 else None
    return None


# Deux signaux d'une même famille diraient deux fois la même chose : on n'en garde qu'un.
_FAMILLE = {
    "dst_sorties_rapides": "rapide", "dst_part_sorties_rapides": "rapide",
    "dst_nouveaux_exp_24h": "inconnus", "dst_nouveaux_exp_72h": "inconnus",
    "dst_nb_recus_24h": "recu24", "dst_somme_recue_24h": "recu24",
    "dst_anciennete_j": "neuf", "dst_nb_recus": "neuf",
}
SANS_RAISON_DOMINANTE = "plusieurs petits signaux réunis, sans raison dominante"


def expliquer(signaux, contributions, k=2, montant_eleve=None):
    """Les k signaux qui poussent le plus vers la fraude, dits en clair.

    signaux et contributions : dictionnaires nom -> valeur. Une phrase n'est gardée que si elle
    est vraie pour la valeur observée ; sinon on passe au signal suivant.
    """
    phrases, familles = [], set()
    for nom in sorted(contributions, key=contributions.get, reverse=True):
        if contributions[nom] <= 0 or len(phrases) == k:
            break
        famille = _FAMILLE.get(nom, nom)
        if famille in familles:
            continue
        phrase = _phrase(nom, signaux, montant_eleve)
        if phrase:
            phrases.append(phrase)
            familles.add(famille)
    return phrases or [SANS_RAISON_DOMINANTE]
