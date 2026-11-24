"""Trafic de fond PaySim et injection des scénarios d'arnaque (docs/scenarios-fraude.md).

Même code que le notebook Kaggle, avec la même graine : les données produites sont les mêmes.
Délais, nombre de mules et montants sont des HYPOTHÈSES DE SIMULATION tirées au hasard.
"""
import numpy as np
import pandas as pd

from .config import JOUR

COLONNES = ["t", "type", "montant", "src", "dst", "y", "scen"]


def charger_paysim(chemin, rng):
    """Lit PaySim sans les colonnes de solde (l'auteur écrit qu'elles ne doivent pas être utilisées)."""
    ps = pd.read_csv(chemin, usecols=["step", "type", "amount", "nameOrig", "nameDest", "isFraud"])
    # Les fraudes natives de PaySim ne sont pas des comptes mules : on les retire
    # pour que l'étiquette ne désigne que nos scénarios.
    ps = ps[ps["isFraud"] == 0]
    return pd.DataFrame({
        # PaySim avance par pas d'une heure : on tire la seconde au hasard dans l'heure.
        "t": (ps["step"].to_numpy() - 1) * 3600 + rng.integers(0, 3600, len(ps)),
        "type": ps["type"].to_numpy(),
        "montant": ps["amount"].to_numpy(),
        "src": ps["nameOrig"].to_numpy(),
        "dst": ps["nameDest"].to_numpy(),
        "y": 0,
        "scen": "fond",
    })


def injecter(fond, rng, n):
    """Ajoute au trafic de fond n instances de chaque scénario et des contre-exemples légitimes."""
    T_MAX = int(fond["t"].max())
    tr = fond[fond["type"] == "TRANSFER"]
    CLIENTS = tr["dst"].unique()                                      # comptes clients existants
    Q_MONTANT = np.quantile(tr["montant"], np.linspace(0, 1, 1001))   # montants réalistes
    L = []
    _n = iter(range(10**9))
    AGENTS = [f"A{i:05d}" for i in range(400)]

    def nouveau():  return f"X{next(_n):09d}"                  # compte créé pour le scénario
    def client():   return CLIENTS[rng.integers(len(CLIENTS))]  # compte déjà présent dans PaySim
    def agent():    return AGENTS[rng.integers(len(AGENTS))]
    def expediteur():                                          # comme dans PaySim : presque jamais d'historique
        return nouveau() if rng.random() < 0.9 else client()
    def mn(a, b):   return int(rng.uniform(a, b) * 60)         # durée en secondes, bornes en minutes
    def montant(lo=0.10, hi=0.98):                             # montant pris dans la distribution PaySim
        return float(Q_MONTANT[rng.integers(int(lo * 1000), int(hi * 1000))])
    def debut(marge=4):
        return int(rng.uniform(JOUR, T_MAX - marge * JOUR))
    def tx(t, typ, a, src, dst, y, scen):
        if 0 <= t <= T_MAX:
            L.append((int(t), typ, round(float(a), 2), src, dst, y, scen))

    def habiller(compte, t, p=0.5):
        """Petit historique normal avant l'arnaque, pour qu'une mule ne soit pas toujours un compte vierge."""
        if rng.random() < p:
            for _ in range(rng.integers(1, 5)):
                tx(t - rng.uniform(2, 20) * JOUR, "TRANSFER", montant(0.05, 0.5), expediteur(), compte, 0, "fond_mule")

    def s1_erreur(n):       # la victime « rembourse » elle-même un faux dépôt
        equipes = []
        for _ in range(n):
            if equipes and rng.random() < 0.5:        # une équipe de mules ressert pour une autre victime
                m1, m2, t = equipes[rng.integers(len(equipes))]
                t += int(rng.uniform(0.2, 4) * JOUR)
            else:
                m1, m2, t = nouveau(), nouveau(), debut()
                habiller(m1, t)
            equipes.append((m1, m2, t))
            a, part = montant(), rng.uniform(0.4, 0.7)
            tx(t, "TRANSFER", a, expediteur(), m1, 1, "S1_erreur")
            t2 = t + mn(2, 15)
            tx(t2, "TRANSFER", a * part, m1, m2, 1, "S1_erreur")
            tx(t2 + mn(1, 10), "CASH_OUT", a * (1 - part) * 0.98, m1, agent(), 1, "S1_erreur")
            tx(t2 + mn(3, 20), "CASH_OUT", a * part * 0.98, m2, agent(), 1, "S1_erreur")

    def s2_faux_agent(n):   # le fraudeur vide le compte en rafale vers 1 ou 2 mules
        for _ in range(n):
            t, v = debut(), expediteur()
            mules = [nouveau() for _ in range(rng.integers(1, 3))]
            for m in mules: habiller(m, t)
            recu = dict.fromkeys(mules, 0.0)
            for _ in range(rng.integers(2, 6)):
                m, a = mules[rng.integers(len(mules))], montant(0.2, 0.8)
                tx(t, "TRANSFER", a, v, m, 1, "S2_faux_agent")
                recu[m] += a
                t += mn(0.5, 3)
            for m, a in recu.items():
                if a: tx(t + mn(3, 20), "CASH_OUT", a * 0.98, m, agent(), 1, "S2_faux_agent")

    def s3_collecteur(n):   # une même mule reçoit plusieurs victimes en 24 à 72 h
        for _ in range(n):
            t0, m = debut(), nouveau()
            habiller(m, t0)
            moments = np.sort(t0 + rng.uniform(0, rng.uniform(1, 3) * JOUR, rng.integers(4, 13)))
            pot = 0.0
            for i, t in enumerate(moments):
                a = montant(0.1, 0.9)
                tx(t, "TRANSFER", a, expediteur(), m, 1, "S3_collecteur")
                pot += a
                if rng.random() < 0.6 or i == len(moments) - 1:   # la mule ne garde presque rien
                    if rng.random() < 0.25:
                        m2, t2 = nouveau(), t + mn(2, 15)
                        tx(t2, "TRANSFER", pot, m, m2, 1, "S3_collecteur")
                        tx(t2 + mn(3, 20), "CASH_OUT", pot * 0.98, m2, agent(), 1, "S3_collecteur")
                    else:
                        tx(t + mn(2, 30), "CASH_OUT", pot * 0.98, m, agent(), 1, "S3_collecteur")
                    pot = 0.0

    def s4_chaine(n):       # l'argent traverse 2 à 4 étages avant le retrait
        for _ in range(n):
            t, m = debut(), nouveau()
            habiller(m, t, p=1.0)                     # la première mule a toujours un passé normal
            a = montant(0.3, 0.98)
            tx(t, "TRANSFER", a, expediteur(), m, 1, "S4_chaine")
            etage = [(m, a, t)]
            for _ in range(rng.integers(1, 4)):
                suivant = []
                for src, a, t in etage:
                    parts = [rng.uniform(0.4, 0.6)] if rng.random() < 0.5 else [1.0]
                    parts += [1 - parts[0]] if parts[0] < 1 else []
                    for p in parts:
                        m2, t2 = nouveau(), t + mn(1, 8)
                        tx(t2, "TRANSFER", a * p * 0.99, src, m2, 1, "S4_chaine")
                        suivant.append((m2, a * p * 0.99, t2))
                etage = suivant
            for src, a, t in etage:
                tx(t + mn(2, 15), "CASH_OUT", a * 0.98, src, agent(), 1, "S4_chaine")

    # --- Contre-exemples légitimes (y = 0) : ils ressemblent à une mule sans en être une.
    def l_tontine(n):       # mêmes expéditeurs chaque semaine, pot reversé à un membre
        for _ in range(n):
            chef = client()
            membres = [expediteur() for _ in range(rng.integers(8, 16))]
            a, t0 = montant(0.02, 0.3), int(rng.uniform(0, 6 * JOUR))
            for semaine in range(4):
                t = t0 + semaine * 7 * JOUR
                for mb in membres:
                    tx(t + rng.uniform(0, 6 * 3600), "TRANSFER", a, mb, chef, 0, "L_tontine")
                tx(t + rng.uniform(8, 30) * 3600, "TRANSFER", a * len(membres), chef, membres[semaine % len(membres)], 0, "L_tontine")

    def l_commerce(n):      # beaucoup de clients nouveaux, petits montants, solde qui reste
        for _ in range(n):
            boutique = client() if rng.random() < 0.5 else nouveau()
            caisse = 0.0
            for jour in np.sort(rng.integers(0, 30, rng.integers(20, 61))):
                a = montant(0.01, 0.25)
                tx(jour * JOUR + rng.uniform(8, 20) * 3600, "TRANSFER", a, expediteur(), boutique, 0, "L_commerce")
                caisse += a
                if rng.random() < 0.1:
                    tx((jour + 1) * JOUR + rng.uniform(8, 12) * 3600, "CASH_OUT", caisse * rng.uniform(0.3, 0.7), boutique, agent(), 0, "L_commerce")
                    caisse = 0.0

    def l_etudiant(n):      # compte récent, retrait rapide, mais toujours la même famille
        for _ in range(n):
            etu, famille, t = nouveau(), [expediteur() for _ in range(rng.integers(1, 3))], debut(15)
            for _ in range(rng.integers(2, 5)):
                a = montant(0.05, 0.6)
                tx(t, "TRANSFER", a, famille[rng.integers(len(famille))], etu, 0, "L_etudiant")
                tx(t + mn(10, 90), "CASH_OUT", a * rng.uniform(0.7, 1.0), etu, agent(), 0, "L_etudiant")
                t += int(rng.uniform(3, 10) * JOUR)

    def l_nouveau(n):       # compte neuf ordinaire : reçoit 1 à 3 transferts, retire parfois, rarement vite
        for _ in range(n):
            cpt, t = nouveau(), debut(1)
            for _ in range(rng.integers(1, 4)):
                a = montant(0.05, 0.98)
                tx(t, "TRANSFER", a, expediteur(), cpt, 0, "L_nouveau")
                if rng.random() < 0.35:
                    attente = mn(5, 30) if rng.random() < 0.3 else mn(120, 3000)
                    tx(t + attente, "CASH_OUT", a * rng.uniform(0.5, 1.0), cpt, agent(), 0, "L_nouveau")
                t += int(rng.uniform(0.1, 6) * JOUR)

    for f in (s1_erreur, s2_faux_agent, s3_collecteur, s4_chaine):
        f(n)
    l_tontine(n); l_commerce(n); l_etudiant(2 * n); l_nouveau(10 * n)

    inj = pd.DataFrame(L, columns=COLONNES)
    tout = pd.concat([fond, inj], ignore_index=True).sort_values("t", kind="stable", ignore_index=True)
    return tout, float(Q_MONTANT[900])


def construire(chemin_paysim, seed, n):
    """Retourne (toutes les transactions triées par temps, 90e centile des montants de transfert)."""
    rng = np.random.default_rng(seed)
    fond = charger_paysim(chemin_paysim, rng)
    return injecter(fond, rng, n)
