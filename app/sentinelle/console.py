"""Données de la console institution (demo/console.html).

Rejoue une fois le flux de démo, transfert par transfert, comme le ferait le service, et garde
pour chaque transfert son score, ses raisons et quelques signaux lisibles. La console applique
ensuite elle-même les seuils choisis par l'établissement : c'est lui qui décide à partir de quel
score on avertit l'expéditeur et à partir de quel score on bloque.
"""
from pathlib import Path

import numpy as np
import pandas as pd

from . import config
from .moteur import Moteur
from .raisons import expliquer
from .rejeu import magasin_depuis

# Signaux montrés à l'analyste dans la fiche d'une alerte.
APERCU = ["premier_contact", "dst_anciennete_j", "dst_nb_recus", "dst_nouveaux_exp_24h",
          "dst_nb_sorties", "dst_sorties_rapides", "dst_ratio_sorties_entrees"]
SCORE_MIN_RAISONS = 0.05     # en dessous, aucun seuil raisonnable n'alerte : inutile de rédiger une raison


def noter(moteur, lignes):
    """Score et raisons pour une liste de dictionnaires de signaux, quel que soit le seuil."""
    if not lignes:
        return []
    x = np.array([[l[n] for n in moteur.signaux] for l in lignes], dtype=np.float32)
    d = moteur._xgb.DMatrix(x, feature_names=list(moteur.signaux))
    contrib = moteur.booster.predict(d, pred_contribs=True, iteration_range=moteur.plage)
    scores = 1.0 / (1.0 + np.exp(-contrib.sum(axis=1)))
    sortie = []
    for ligne, c, score in zip(lignes, contrib, scores):
        raisons = []
        if score >= SCORE_MIN_RAISONS:
            raisons = expliquer(ligne, dict(zip(moteur.signaux, map(float, c[:-1]))), 2, moteur.montant_eleve)
        sortie.append((round(float(score), 4), raisons))
    return sortie


def _apercu(signaux):
    return {n: round(float(signaux[n]), 3) for n in APERCU}


def preparer(dossier=None):
    """Retourne (moteur, magasin après le flux, données de la console)."""
    dossier = Path(dossier or config.MODELES)
    moteur = Moteur(dossier)
    magasin = magasin_depuis(pd.read_csv(dossier / "demo_historique.csv"))
    flux = pd.read_csv(dossier / "demo_flux.csv")
    lignes, signaux = [], []
    for ligne in flux.itertuples(index=False):
        if ligne.type == "TRANSFER":
            signaux.append(magasin.signaux(ligne.t, ligne.src, ligne.dst, ligne.montant))   # noté AVANT d'être enregistré
            lignes.append(ligne)
        magasin.ajouter(ligne.t, ligne.type, ligne.montant, ligne.src, ligne.dst)
    transferts = [{
        "t": int(l.t), "src": str(l.src), "dst": str(l.dst), "montant": float(l.montant),
        "score": score, "raisons": raisons, "fraude": int(l.y), "victime": bool(l.victime),
        "scen": str(l.scen), "apercu": _apercu(s),
    } for l, s, (score, raisons) in zip(lignes, signaux, noter(moteur, signaux))]
    m = moteur.meta.get("mesures") or {}
    donnees = {
        "seuils": {"avertir": moteur.seuil_alerte, "bloquer": moteur.seuil_blocage},
        "origine": moteur.meta.get("origine"), "nb_signaux": len(moteur.signaux),
        "mesures": {k: m.get(k) for k in ("decoupage", "jours", "victimes", "fausses_alertes", "alertes_justes",
                                          "reference_simple", "scenario_cache", "premier_transfert_mule_vierge")},
        "transferts": transferts,
    }
    return moteur, magasin, donnees


def noter_un(moteur, magasin, src, dst, montant, enregistrer=False):
    """Une transaction saisie à la main, notée contre l'historique connu après le flux."""
    t = magasin.horloge + 60
    signaux = magasin.signaux(t, src, dst, montant)
    score, raisons = noter(moteur, [signaux])[0]
    if enregistrer:
        magasin.ajouter(t, "TRANSFER", montant, src, dst)
    return {"t": t, "src": src, "dst": dst, "montant": float(montant), "score": score,
            "raisons": raisons or expliquer(signaux, {}, 2, moteur.montant_eleve),
            "fraude": None, "victime": None, "scen": "saisie", "apercu": _apercu(signaux),
            "enregistre": bool(enregistrer)}
