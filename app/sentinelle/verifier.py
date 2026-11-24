"""Vérifier que le modèle intégré au service est bien celui qui a été évalué :
`python -m sentinelle.verifier`.

Rejoue le flux de démo transfert par transfert, comme le fait le service, et compare chaque
score à celui calculé par lot pendant l'intégration.
"""
import pandas as pd

from . import config
from .moteur import Moteur
from .rejeu import magasin_depuis, rejouer


def verifier(dossier=None, journal=print):
    dossier = dossier or config.MODELES
    moteur = Moteur(dossier)
    historique = pd.read_csv(f"{dossier}/demo_historique.csv")
    flux = pd.read_csv(f"{dossier}/demo_flux.csv")
    magasin = magasin_depuis(historique)
    verdicts, _ = rejouer(moteur, magasin, flux)
    ecarts = [abs(v["score"] - v["score_lot"]) for v in verdicts]
    desaccords = sum(moteur.decider(v["score_lot"]) != v["decision"] for v in verdicts)
    pire = max(ecarts) if ecarts else 0.0
    journal(f"{len(verdicts):,} transferts rejoués ; écart maximal de score entre le service et "
            f"l'évaluation : {pire:.4f} ; décisions différentes : {desaccords}")
    return {"transferts": len(verdicts), "ecart_max": pire, "decisions_differentes": desaccords}


if __name__ == "__main__":
    r = verifier()
    raise SystemExit(0 if r["ecart_max"] < 0.01 and r["decisions_differentes"] <= max(1, r["transferts"] // 500) else 1)
