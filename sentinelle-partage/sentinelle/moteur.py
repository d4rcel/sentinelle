"""Le moteur de score : charge le modèle entraîné (fichier .ubj) et rend un verdict.

Le modèle n'est jamais entraîné ici. Il vient de modeles/sentinelle_v1.ubj, produit sur GPU
ou sur CPU par le notebook ou par `python -m sentinelle.entrainer`, puis intégré par
`python -m sentinelle.integrer`. Le service tourne sans GPU.
"""
import json
import time
from pathlib import Path

import numpy as np

from . import config
from .raisons import expliquer

DECISIONS = ("laisser_passer", "alerter", "bloquer")
MESSAGES = {
    "laisser_passer": "Rien d'inhabituel sur le compte destinataire.",
    "alerter": "Attention : ce compte se comporte comme un compte utilisé pour des arnaques.",
    "bloquer": "Transfert bloqué : ce compte se comporte comme un compte utilisé pour des arnaques.",
}


class ModeleAbsent(RuntimeError):
    pass


def plage_d_arbres(booster):
    """Les arbres à utiliser : jusqu'au meilleur tour si l'entraînement s'est arrêté tôt.

    Par défaut, Booster.predict utilise tous les arbres, y compris ceux ajoutés après le meilleur
    tour. On reprend ici le comportement du notebook (XGBClassifier), qui s'arrête au meilleur.
    """
    meilleur = booster.attr("best_iteration")
    return (0, int(meilleur) + 1) if meilleur is not None else (0, 0)


class Moteur:
    def __init__(self, dossier=None):
        import xgboost as xgb
        self._xgb = xgb
        dossier = Path(dossier or config.MODELES)
        fichier, meta = dossier / config.FICHIER_MODELE, dossier / config.FICHIER_META
        if not fichier.is_file() or not meta.is_file():
            raise ModeleAbsent(
                f"Modèle absent de {dossier}. Y déposer {config.FICHIER_MODELE}, puis lancer "
                "`python -m sentinelle.integrer` (ou `python -m sentinelle.entrainer` pour l'entraîner ici)."
            )
        self.meta = json.loads(meta.read_text(encoding="utf-8"))
        self.signaux = self.meta["signaux"]
        self.seuil_alerte = float(self.meta["seuil_alerte"])
        self.seuil_blocage = float(self.meta.get("seuil_blocage", 2.0))   # 2.0 : jamais de blocage
        self.montant_eleve = self.meta.get("montant_eleve")
        self.booster = xgb.Booster()
        self.booster.load_model(str(fichier))
        self.plage = plage_d_arbres(self.booster)

    def decider(self, score):
        return "bloquer" if score >= self.seuil_blocage else "alerter" if score >= self.seuil_alerte else "laisser_passer"

    def noter_signaux(self, lignes, k=2):
        """lignes : liste de dictionnaires de signaux. Retourne un verdict par ligne."""
        if not lignes:
            return []
        x = np.array([[l[n] for n in self.signaux] for l in lignes], dtype=np.float32)
        d = self._xgb.DMatrix(x, feature_names=list(self.signaux))
        # pred_contribs : une colonne par signal, plus le biais. Leur somme est la marge du modèle.
        contrib = self.booster.predict(d, pred_contribs=True, iteration_range=self.plage)
        scores = 1.0 / (1.0 + np.exp(-contrib.sum(axis=1)))
        verdicts = []
        for ligne, c, score in zip(lignes, contrib, scores):
            decision = self.decider(float(score))
            raisons = []
            if decision != "laisser_passer":
                raisons = expliquer(ligne, dict(zip(self.signaux, map(float, c[:-1]))), k, self.montant_eleve)
            verdicts.append({"score": round(float(score), 4), "decision": decision,
                             "message": MESSAGES[decision], "raisons": raisons})
        return verdicts

    def noter(self, magasin, src, dst, montant, t=None):
        """Verdict pour un transfert sur le point d'être confirmé. Ne modifie pas le magasin."""
        debut = time.perf_counter()
        t = magasin.horloge + 1 if t is None else int(t)
        signaux = magasin.signaux(t, src, dst, montant)
        verdict = self.noter_signaux([signaux])[0]
        verdict.update(t=t, expediteur=src, destinataire=dst, montant=float(montant), signaux=signaux,
                       latence_ms=round((time.perf_counter() - debut) * 1000, 2))
        return verdict
