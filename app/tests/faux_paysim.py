"""Fabrique un petit fichier au format de PaySim pour tester sans les 470 Mo du vrai jeu."""
import numpy as np
import pandas as pd


def ecrire(chemin, n=120_000, seed=0):
    rng = np.random.default_rng(seed)
    typ = rng.choice(["CASH_OUT", "PAYMENT", "CASH_IN", "TRANSFER", "DEBIT"], n, p=[.35, .34, .22, .083, .007])
    pd.DataFrame({
        "step": np.sort(rng.integers(1, 744, n)), "type": typ, "amount": rng.lognormal(11, 1.5, n).round(2),
        "nameOrig": [f"C{i}" for i in rng.integers(0, 10**9, n)], "oldbalanceOrg": 0.0, "newbalanceOrig": 0.0,
        "nameDest": np.where(typ == "PAYMENT", [f"M{i}" for i in rng.integers(0, 50_000, n)],
                             [f"C{i}" for i in rng.integers(0, 12_000, n)]),
        "oldbalanceDest": 0.0, "newbalanceDest": 0.0,
        "isFraud": (rng.random(n) < 0.0013).astype(int), "isFlaggedFraud": 0,
    }).to_csv(chemin, index=False)
    return chemin
