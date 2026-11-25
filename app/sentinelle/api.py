"""Le service de score : `uvicorn sentinelle.api:app --port 8000`.

L'établissement de l'expéditeur appelle POST /noter juste avant la confirmation, puis
POST /transferts si l'expéditeur confirme. Le service garde l'historique des comptes en mémoire.
Documentation interactive : http://127.0.0.1:8000/docs
"""
import threading
from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from . import config, console
from .moteur import ModeleAbsent, Moteur
from .rejeu import magasin_depuis

app = FastAPI(title="Sentinelle", version="1.0",
              description="Note le compte destinataire d'un transfert instantané avant sa confirmation.")
_verrou = threading.Lock()
_etat = {}


class Operation(BaseModel):
    expediteur: str = Field(min_length=1, description="identifiant du compte débité")
    destinataire: str = Field(min_length=1, description="identifiant du compte crédité")
    montant: float = Field(gt=0)
    t: Optional[int] = Field(None, ge=0, description="temps en secondes ; par défaut, juste après la dernière opération connue")


def _charger():
    """Charge le modèle et l'historique de départ. Appelé au premier besoin et par /reinitialiser."""
    try:
        moteur = Moteur()
    except ModeleAbsent as e:
        raise HTTPException(status_code=503, detail=str(e))
    historique = config.MODELES / "demo_historique.csv"
    magasin = magasin_depuis(pd.read_csv(historique)) if historique.is_file() else magasin_depuis(
        pd.DataFrame(columns=["t", "type", "montant", "src", "dst"]))
    _etat.update(moteur=moteur, magasin=magasin)


def _pret():
    if "moteur" not in _etat:
        _charger()
    return _etat["moteur"], _etat["magasin"]


@app.get("/sante")
def sante():
    with _verrou:
        moteur, magasin = _pret()
        return {"etat": "ok", "origine_du_modele": moteur.meta.get("origine"),
                "signaux": len(moteur.signaux), "seuil_alerte": moteur.seuil_alerte,
                "seuil_blocage": moteur.seuil_blocage, "comptes_connus": len(magasin.comptes),
                "operations_connues": magasin.nb_evenements, "horloge": magasin.horloge}


@app.post("/noter")
def noter(op: Operation):
    """Verdict pour un transfert sur le point d'être confirmé. Ne change rien à l'historique."""
    with _verrou:
        moteur, magasin = _pret()
        return moteur.noter(magasin, op.expediteur, op.destinataire, op.montant, op.t)


def _enregistrer(type_, op):
    with _verrou:
        _, magasin = _pret()
        t = magasin.horloge + 1 if op.t is None else op.t
        magasin.ajouter(t, type_, op.montant, op.expediteur, op.destinataire)
        return {"enregistre": True, "type": type_, "t": t}


@app.post("/transferts")
def transfert(op: Operation):
    """Enregistre un transfert confirmé : il entre dans l'historique des deux comptes."""
    return _enregistrer("TRANSFER", op)


@app.post("/retraits")
def retrait(op: Operation):
    """Enregistre un retrait en espèces de `expediteur` chez l'agent `destinataire`."""
    return _enregistrer("CASH_OUT", op)


@app.get("/comptes/{compte}")
def compte(compte: str):
    """Ce que le service sait d'un compte."""
    with _verrou:
        _, magasin = _pret()
        return magasin.resume(compte)


@app.post("/reinitialiser")
def reinitialiser():
    """Recharge le modèle et l'historique de départ (utile entre deux démonstrations)."""
    with _verrou:
        _charger()
        return {"reinitialise": True, "operations_connues": _etat["magasin"].nb_evenements}


# ----------------------------------------------------------------------------- console institution
class Saisie(BaseModel):
    expediteur: str = Field(min_length=1)
    destinataire: str = Field(min_length=1)
    montant: float = Field(gt=0)
    enregistrer: bool = Field(False, description="ajouter le transfert à l'historique après l'avoir noté")


def _console():
    """Prépare une fois les données de la console : le flux de démo rejoué et noté."""
    if "console" not in _etat:
        try:
            moteur, magasin, donnees = console.preparer()
        except (ModeleAbsent, FileNotFoundError) as e:
            raise HTTPException(status_code=503, detail=f"Console indisponible : {e}")
        _etat["console"] = {"moteur": moteur, "magasin": magasin, "donnees": donnees}
    return _etat["console"]


@app.get("/demo", include_in_schema=False)
def page_console():
    """La console institution : flux, file du département risque, transaction unique."""
    return FileResponse(config.RACINE / "demo" / "console.html", media_type="text/html")


@app.get("/demo/donnees")
def donnees_console():
    """Le flux de démo noté transfert par transfert. Les seuils sont appliqués par la console."""
    with _verrou:
        return _console()["donnees"]


@app.post("/demo/noter")
def noter_console(op: Saisie):
    """Note une transaction saisie à la main contre l'historique connu à la fin du flux."""
    with _verrou:
        c = _console()
        return console.noter_un(c["moteur"], c["magasin"], op.expediteur, op.destinataire, op.montant, op.enregistrer)
