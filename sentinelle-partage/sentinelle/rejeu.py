"""Rejouer un flux enregistré à travers le moteur, comme si les transferts arrivaient en direct."""
from .magasin import Magasin

COLONNES = ["t", "type", "montant", "src", "dst"]


def magasin_depuis(tableau):
    """Construit un magasin à partir d'un tableau d'opérations passées, triées par temps."""
    return Magasin().charger(tableau[COLONNES].itertuples(index=False, name=None))


def rejouer(moteur, magasin, flux, debut=0, nb_transferts=None):
    """Joue le flux à partir de la ligne `debut`. Chaque transfert est noté AVANT d'être enregistré.

    Retourne (verdicts des transferts joués, position de la prochaine ligne à jouer).
    """
    lignes, signaux, position = [], [], debut
    for ligne in flux.iloc[debut:].itertuples(index=False):
        if nb_transferts is not None and len(lignes) >= nb_transferts:
            break
        if ligne.type == "TRANSFER":
            signaux.append(magasin.signaux(ligne.t, ligne.src, ligne.dst, ligne.montant))
            lignes.append(ligne)
        magasin.ajouter(ligne.t, ligne.type, ligne.montant, ligne.src, ligne.dst)
        position += 1
    verdicts = moteur.noter_signaux(signaux)
    for verdict, ligne in zip(verdicts, lignes):
        verdict.update(t=int(ligne.t), expediteur=ligne.src, destinataire=ligne.dst,
                       montant=float(ligne.montant), fraude=int(ligne.y), scen=ligne.scen,
                       victime=bool(ligne.victime), score_lot=float(ligne.score_lot))
    return verdicts, position
