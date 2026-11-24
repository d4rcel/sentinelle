"""Entraîner le modèle ici : `python -m sentinelle.entrainer`.

Secours quand aucun modèle n'a pu être téléchargé, et commande à lancer sur la machine GPU du
hackathon : s'il y a un GPU NVIDIA, XGBoost s'entraîne dessus et les temps CPU et GPU sont notés.
Le modèle est ensuite intégré comme n'importe quel modèle déposé (voir integrer.py).
"""
import argparse
import shutil
import subprocess
import time
from pathlib import Path

import numpy as np

from . import config
from .integrer import Contexte, integrer


def gpu_present():
    # Sans GPU, XGBoost bascule sur le CPU avec un simple avertissement : on vérifie nous-mêmes.
    return bool(shutil.which("nvidia-smi")) and subprocess.run(["nvidia-smi"], capture_output=True).returncode == 0


def entrainer(device, Xa, ya, arbres=512, arret=50, **eval_):
    import xgboost as xgb
    m = xgb.XGBClassifier(n_estimators=arbres, max_depth=6, learning_rate=0.1, tree_method="hist",
                          device=device, eval_metric="aucpr", early_stopping_rounds=arret,
                          scale_pos_weight=float((ya == 0).sum() / max(ya.sum(), 1)), random_state=config.SEED)
    t0 = time.perf_counter()
    m.fit(Xa, ya, verbose=False, **eval_)
    return m, time.perf_counter() - t0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--paysim", help="chemin du CSV PaySim (sinon cherché dans data/)")
    p.add_argument("--modeles", help="dossier de sortie (défaut : modeles/)")
    p.add_argument("--n", type=int, default=config.N_PAR_SCENARIO, help="instances par scénario")
    p.add_argument("--volume", type=int, default=0,
                   help="recopier l'entraînement N fois pour chronométrer CPU contre GPU (ex. 20)")
    a = p.parse_args(argv)
    dossier = Path(a.modeles or config.MODELES); dossier.mkdir(parents=True, exist_ok=True)

    ctx = Contexte(a.paysim, n=a.n)
    ctx.verifier_sans_fuite()
    print("Test anti-fuite réussi : aucun signal ne lit le futur, aucune colonne de solde n'est chargée.")
    X, y, app, val = ctx.X, ctx.y, ctx.app, ctx.val
    temps, gpu = {"signaux_cpu": round(ctx.temps_signaux, 2)}, gpu_present()

    modele, temps["xgb_cpu"] = entrainer("cpu", X[app], y[app], eval_set=[(X[val], y[val])])
    print(f"XGBoost CPU : {temps['xgb_cpu']:.1f} s, {modele.best_iteration + 1} arbres retenus")
    origine = "entraîné sur cette machine, sur CPU"
    if gpu:
        entrainer("cuda", X[app][:1000], y[app][:1000], arbres=5, arret=None)          # échauffement
        modele, temps["xgb_gpu"] = entrainer("cuda", X[app], y[app], eval_set=[(X[val], y[val])])
        print(f"XGBoost GPU : {temps['xgb_gpu']:.1f} s, {modele.best_iteration + 1} arbres retenus")
        origine = "entraîné sur cette machine, sur GPU"
    else:
        print("Pas de GPU NVIDIA ici : entraînement sur CPU seulement.")
    if a.volume:
        rng = np.random.default_rng(config.SEED)
        Xa = X[app].to_numpy()
        Xgros = np.tile(Xa, (a.volume, 1)) * rng.uniform(0.98, 1.02, (len(Xa) * a.volume, 1)).astype(np.float32)
        ygros = np.tile(y[app], a.volume)
        print(f"Volume grossi (pour chronométrer seulement) : {len(Xgros):,} lignes")
        _, temps["xgb_gros_cpu"] = entrainer("cpu", Xgros, ygros, arbres=200, arret=None)
        print(f"  CPU, 200 arbres : {temps['xgb_gros_cpu']:.1f} s")
        if gpu:
            _, temps["xgb_gros_gpu"] = entrainer("cuda", Xgros, ygros, arbres=200, arret=None)
            print(f"  GPU, 200 arbres : {temps['xgb_gros_gpu']:.1f} s, "
                  f"soit x{temps['xgb_gros_cpu'] / temps['xgb_gros_gpu']:.1f}")

    modele.get_booster().save_model(str(dossier / config.FICHIER_MODELE))
    fichier_meta = dossier / config.FICHIER_META
    if fichier_meta.is_file():
        fichier_meta.unlink()                      # les anciennes mesures ne valent plus pour ce modèle
    meta = integrer(dossier, ctx=ctx, origine=origine)
    import json
    meta["temps_s"].update({k: round(v, 2) for k, v in temps.items()})
    fichier_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Modèle enregistré dans {dossier / config.FICHIER_MODELE}")


if __name__ == "__main__":
    main()
