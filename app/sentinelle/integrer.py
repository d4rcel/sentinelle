"""Intégrer un modèle au système : `python -m sentinelle.integrer`.

À lancer après avoir déposé modeles/sentinelle_v1.ubj (téléchargé depuis Kaggle ou depuis la
machine GPU du hackathon). Aucun entraînement ici. La commande :
  1. reconstruit les mêmes données simulées que le notebook (même graine) ;
  2. note tous les transferts avec le modèle déposé ;
  3. règle les seuils d'alerte et de blocage sur la validation, mesure sur le test ;
  4. écrit modeles/sentinelle_v1.json et les données de la démo (flux, historique, cas).
"""
import argparse
import datetime
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from . import config, donnees
from .config import JOUR
from .signaux import NOMS, preparer_evenements, signaux


class Contexte:
    """Les données simulées et leurs signaux, calculés une fois."""

    def __init__(self, paysim=None, seed=config.SEED, n=config.N_PAR_SCENARIO, journal=print):
        t0 = time.perf_counter()
        chemin = config.trouver_paysim(paysim)
        journal(f"Lecture de {chemin} et injection des scénarios...")
        self.tout, self.montant_eleve = donnees.construire(chemin, seed, n)
        self.seed, self.n = seed, n
        self.ev = preparer_evenements(self.tout)
        t1 = time.perf_counter()
        self.X = signaux(np, **self.ev)
        self.temps_signaux = time.perf_counter() - t1
        self.idx_tr = np.flatnonzero(self.ev["est_tr"])            # lignes de `tout` qui sont des transferts
        self.meta = self.tout.loc[self.ev["est_tr"], ["t", "y", "scen"]].reset_index(drop=True)
        jour = self.meta["t"] / JOUR
        cache = self.meta["scen"] == config.SCENARIO_CACHE
        self.app = ((jour < config.JOUR_VALIDATION) & ~cache).to_numpy()   # scénario caché retiré
        self.val = ((jour >= config.JOUR_VALIDATION) & (jour < config.JOUR_TEST) & ~cache).to_numpy()
        self.test = (jour >= config.JOUR_TEST).to_numpy()                 # scénario caché compris
        self.y = self.meta["y"].to_numpy()
        journal(f"{len(self.tout):,} opérations, {len(self.X):,} transferts à noter, "
                f"{int(self.y.sum()):,} frauduleux ; signaux calculés en {self.temps_signaux:.1f} s "
                f"(total {time.perf_counter() - t0:.0f} s)")

    def verifier_sans_fuite(self):
        """En coupant les données au jour 15, les signaux d'avant le jour 15 ne doivent pas bouger."""
        coupe = self.ev["t"] < 15 * JOUR
        Xc = signaux(np, **{k: v[coupe] for k, v in self.ev.items()})
        avant = (self.ev["t"][self.ev["est_tr"]] < 15 * JOUR)
        assert np.allclose(self.X[avant].to_numpy(), Xc.to_numpy(), rtol=1e-4, atol=1e-2), "Un signal lit le futur !"


def noter_tout(booster, X):
    import xgboost as xgb
    noms = booster.feature_names
    if noms is not None and list(noms) != NOMS:
        raise ValueError(f"Ce modèle n'attend pas les signaux du projet.\n  modèle : {noms}\n  projet : {NOMS}")
    from .moteur import plage_d_arbres
    return booster.predict(xgb.DMatrix(X.to_numpy(), feature_names=NOMS), iteration_range=plage_d_arbres(booster))


def mesurer(ctx, score):
    """Seuils réglés sur la validation, mesures sur le test."""
    from sklearn.metrics import average_precision_score
    y, meta, X = ctx.y, ctx.meta, ctx.X
    sains_val = score[ctx.val & (y == 0)]
    seuil_alerte = float(np.quantile(sains_val, 1 - config.FAUSSES_ALERTES))
    seuil_blocage = max(float(np.quantile(sains_val, 1 - config.FAUX_BLOCAGES)), seuil_alerte)
    res = meta[ctx.test].assign(score=score[ctx.test])
    res["alerte"], res["blocage"] = res["score"] >= seuil_alerte, res["score"] >= seuil_blocage
    par_scen = res.groupby("scen").agg(transferts=("y", "size"), fraudes=("y", "sum"),
                                       part_alertee=("alerte", "mean"), part_bloquee=("blocage", "mean"))
    fraude, sain = res[res["y"] == 1], res[res["y"] == 0]
    vierge = res[(res["y"] == 1) & (X.loc[res.index, "dst_nb_recus"] == 0)
                 & (X.loc[res.index, "src_recu_30min_vs_montant"] == 0)]
    cache = res[res["scen"] == config.SCENARIO_CACHE]
    alertes = res[res["alerte"]]

    def part(serie):
        return None if len(serie) == 0 else round(float(serie.mean()), 4)

    return {
        "seuil_alerte": seuil_alerte, "seuil_blocage": seuil_blocage,
        "mesures": {
            "decoupage": {nom: {"transferts": int(m.sum()), "fraudes": int(y[m].sum())}
                          for nom, m in (("entrainement", ctx.app), ("validation", ctx.val), ("test", ctx.test))},
            "precision_moyenne": round(float(average_precision_score(res["y"], res["score"])), 4),
            "hasard": round(float(res["y"].mean()), 4),
            "fraudes_signalees": part(fraude["alerte"]), "fraudes_bloquees": part(fraude["blocage"]),
            "fausses_alertes": part(sain["alerte"]), "faux_blocages": part(sain["blocage"]),
            "alertes_justes": part(alertes["y"]),
            "scenario_cache": {"nom": config.SCENARIO_CACHE, "part_alertee": part(cache["alerte"]),
                               "transferts": int(len(cache))},
            "premier_transfert_mule_vierge": {"alertes": int(vierge["alerte"].sum()), "total": int(len(vierge))},
            "par_scenario": [dict(scen=s, transferts=int(r.transferts), fraudes=int(r.fraudes),
                                  part_alertee=round(float(r.part_alertee), 4),
                                  part_bloquee=round(float(r.part_bloquee), 4))
                             for s, r in par_scen.iterrows()],
        },
    }


def _operations(tout, lignes):
    """Lignes de `tout` sous forme de listes [t, type, montant, src, dst] pour le JSON."""
    t = tout.iloc[lignes]
    return [[int(a), b, float(c), d, e] for a, b, c, d, e in
            zip(t["t"], t["type"], t["montant"], t["src"], t["dst"])]


def exporter_demo(ctx, score, seuil_alerte, dossier):
    """Écrit le flux d'une journée de test, l'historique de ses comptes et quelques cas choisis."""
    tout, ev, X, meta = ctx.tout, ctx.ev, ctx.X, ctx.meta
    t, src, dst = ev["t"], ev["src"], ev["dst"]
    victime = (ctx.y == 1) & (X["src_recu_30min_vs_montant"].to_numpy() == 0)   # premier maillon : une vraie victime
    score_tout = np.full(len(tout), np.nan); score_tout[ctx.idx_tr] = score
    victime_tout = np.zeros(len(tout), bool); victime_tout[ctx.idx_tr] = victime

    # --- Flux : tous les transferts du premier jour de test, à leurs vraies proportions.
    t0, t1 = config.JOUR_TEST * JOUR, (config.JOUR_TEST + 1) * JOUR
    dans_flux = ev["est_tr"] & (t >= t0) & (t < t1)
    comptes = np.union1d(src[dans_flux], dst[dans_flux])
    concerne = np.isin(src, comptes) | np.isin(dst, comptes)
    extrait = tout.assign(victime=victime_tout, score_lot=score_tout)
    extrait[concerne & (t < t0)][donnees.COLONNES].to_csv(dossier / "demo_historique.csv", index=False)
    extrait[concerne & (t >= t0) & (t < t1)].to_csv(dossier / "demo_flux.csv", index=False)

    # --- Cas choisis dans la période de test, chacun avec l'historique de ses deux comptes.
    scen, alerte = meta["scen"].to_numpy(), score >= seuil_alerte
    col = {n: X[n].to_numpy() for n in NOMS}

    def choisir(masque, cle):
        idx = np.flatnonzero(masque & ctx.test)
        return None if len(idx) == 0 else int(idx[np.argmax(cle[idx])])

    choix = {
        "arnaque": choisir((scen == "S1_erreur") & victime & alerte & (col["dst_sorties_rapides"] >= 1), score),
        "collecteur": choisir((scen == "S3_collecteur") & victime & alerte, col["dst_nouveaux_exp_24h"]),
        "tontine": choisir((scen == "L_tontine") & ~alerte, col["dst_nb_recus_24h"]),
        "commerce": choisir((scen == "L_commerce") & ~alerte, col["dst_nouveaux_exp_72h"]),
        "limite": choisir(victime & ~alerte & (col["dst_nb_recus"] == 0), (scen == "S1_erreur") * 1.0),
    }
    cas = []
    for ident, i in choix.items():
        if i is None:
            continue
        ligne = int(ctx.idx_tr[i])
        s, d, tc = src[ligne], dst[ligne], t[ligne]
        avant = np.flatnonzero(((src == s) | (dst == s) | (src == d) | (dst == d)) & (t < tc))
        # Suite de l'histoire : où part l'argent dans les 3 heures, s'il s'agit d'une arnaque.
        suite, atteints = [], {int(d)}
        if ctx.y[i] == 1:
            apres = np.flatnonzero((t > tc) & (t <= tc + 3 * 3600) & (tout["y"].to_numpy() == 1)
                                   & (tout["scen"].to_numpy() == scen[i]))
            for j in apres:
                if int(src[j]) in atteints:
                    suite.append(int(j))
                    if ev["est_tr"][j]:
                        atteints.add(int(dst[j]))
        cas.append({
            "id": ident, "scen": str(scen[i]), "fraude": int(ctx.y[i]), "t": int(tc),
            "src": str(tout["src"].iat[ligne]), "dst": str(tout["dst"].iat[ligne]),
            "montant": float(tout["montant"].iat[ligne]), "score_lot": round(float(score[i]), 4),
            "historique": _operations(tout, avant), "suite": _operations(tout, suite),
        })
    (dossier / "demo_cas.json").write_text(json.dumps(cas, ensure_ascii=False), encoding="utf-8")
    return {"transferts_flux": int(dans_flux.sum()), "comptes_flux": int(len(comptes)), "cas": [c["id"] for c in cas]}


def integrer(dossier=None, ctx=None, paysim=None, origine=None, journal=print):
    import xgboost as xgb
    dossier = Path(dossier or config.MODELES)
    fichier, fichier_meta = dossier / config.FICHIER_MODELE, dossier / config.FICHIER_META
    if not fichier.is_file():
        raise FileNotFoundError(f"Déposer d'abord le modèle dans {fichier}")
    booster = xgb.Booster(); booster.load_model(str(fichier))
    ctx = ctx or Contexte(paysim, journal=journal)
    score = noter_tout(booster, ctx.X)
    resultat = mesurer(ctx, score)
    ancien = json.loads(fichier_meta.read_text(encoding="utf-8")) if fichier_meta.is_file() else {}
    meta = {
        "signaux": NOMS, **resultat, "montant_eleve": ctx.montant_eleve,
        "scenario_cache": config.SCENARIO_CACHE, "seed": ctx.seed, "n_par_scenario": ctx.n,
        "origine": origine or ancien.get("origine") or "modèle déposé dans modeles/ (téléchargé)",
        "temps_s": {**ancien.get("temps_s", {}), "signaux_cpu_local": round(ctx.temps_signaux, 2)},
        "integre_le": datetime.datetime.now().isoformat(timespec="seconds"),
        "versions": {"xgboost": xgb.__version__, "pandas": pd.__version__, "numpy": np.__version__},
        "demo": exporter_demo(ctx, score, resultat["seuil_alerte"], dossier),
    }
    fichier_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    m = meta["mesures"]
    journal(f"Seuils : alerte {meta['seuil_alerte']:.3f}, blocage {meta['seuil_blocage']:.3f}")
    if "seuil_alerte" in ancien:
        # Si les données reconstruites ici sont bien celles du notebook, les deux seuils coïncident.
        meta["seuil_alerte_du_notebook"] = ancien.get("seuil_alerte_du_notebook", ancien["seuil_alerte"])
        ecart = abs(meta["seuil_alerte_du_notebook"] - meta["seuil_alerte"])
        journal(f"Seuil d'alerte du notebook : {meta['seuil_alerte_du_notebook']:.4f} ; recalculé ici : "
                f"{meta['seuil_alerte']:.4f}" + ("" if ecart < 0.01 else "  <-- ÉCART : les données diffèrent de celles du notebook"))
        fichier_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    journal(f"Test : précision moyenne {m['precision_moyenne']:.3f} (hasard {m['hasard']:.3f}) ; "
            f"fraudes signalées {m['fraudes_signalees']:.1%} ; fausses alertes {m['fausses_alertes']:.2%}")
    journal(f"Scénario caché {config.SCENARIO_CACHE} : {m['scenario_cache']['part_alertee']:.1%} alerté")
    v = m["premier_transfert_mule_vierge"]
    journal(f"Premier transfert vers une mule vierge : {v['alertes']} alertés sur {v['total']}")
    if m["precision_moyenne"] > 0.99:
        journal("ATTENTION : score > 0,99. Soupçonner une fuite ou des scénarios trop faciles.")
    journal(f"Démo prête : {meta['demo']['transferts_flux']:,} transferts dans le flux, cas {meta['demo']['cas']}")
    return meta


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--paysim", help="chemin du CSV PaySim (sinon cherché dans data/)")
    p.add_argument("--modeles", help="dossier du modèle (défaut : modeles/)")
    a = p.parse_args(argv)
    integrer(a.modeles, paysim=a.paysim)


if __name__ == "__main__":
    main()
