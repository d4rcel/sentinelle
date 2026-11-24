"""Réglages communs à l'entraînement, au service et à la démo."""
import glob
import os
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
MODELES = Path(os.environ.get("SENTINELLE_MODELES", RACINE / "modeles"))

SEED = 42
JOUR = 24 * 3600                 # tout le temps est compté en secondes
N_PAR_SCENARIO = 300             # instances injectées par scénario
SCENARIO_CACHE = "S4_chaine"     # jamais montré à l'entraînement
JOUR_VALIDATION, JOUR_TEST = 20, 24   # entraînement < 20 <= validation < 24 <= test
FAUSSES_ALERTES, FAUX_BLOCAGES = 0.01, 0.001   # taux visés sur la validation

FICHIER_MODELE = "sentinelle_v1.ubj"
FICHIER_META = "sentinelle_v1.json"


def trouver_paysim(chemin=None):
    """Cherche le CSV de PaySim : argument, variable SENTINELLE_PAYSIM, puis dossiers data/ voisins."""
    candidats = [chemin, os.environ.get("SENTINELLE_PAYSIM")]
    for base in (RACINE / "data", RACINE.parent / "data", RACINE.parent.parent / "data", Path("/kaggle/input")):
        candidats += sorted(glob.glob(str(base / "**" / "PS_*_log.csv"), recursive=True))
    for c in candidats:
        if c and Path(c).is_file():
            return Path(c)
    raise FileNotFoundError(
        "PaySim introuvable. Lancer scripts/telecharger_donnees.sh paysim, "
        "ou donner le chemin du CSV avec --paysim ou la variable SENTINELLE_PAYSIM."
    )
