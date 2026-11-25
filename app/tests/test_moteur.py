"""Le modèle intégré : fichiers produits, verdicts, raisons, et accord entre service et évaluation."""
import json

import pandas as pd

from sentinelle.magasin import Magasin
from sentinelle.moteur import DECISIONS, Moteur
from sentinelle.raisons import SANS_RAISON_DOMINANTE, expliquer
from sentinelle.signaux import NOMS
from sentinelle.verifier import verifier


def test_fichiers_produits(monde):
    d = monde["modeles"]
    for nom in ("sentinelle_v1.ubj", "sentinelle_v1.json", "demo_flux.csv", "demo_historique.csv", "demo_cas.json"):
        assert (d / nom).is_file(), nom
    meta = json.loads((d / "sentinelle_v1.json").read_text(encoding="utf-8"))
    assert meta["signaux"] == NOMS
    assert 0 < meta["seuil_alerte"] <= meta["seuil_blocage"]
    m = meta["mesures"]
    assert m["decoupage"]["test"]["transferts"] > 0
    assert "src_anciennete_j" not in NOMS and "src_recu_30min_vs_montant" not in NOMS
    # La référence simple et les mesures sur les seules victimes doivent toujours être publiées.
    assert 0 <= m["reference_simple"]["victimes_signalees"] <= 1 and m["victimes"]["transferts"] > 0
    assert m["scenario_cache"]["victimes"]["total"] <= m["scenario_cache"]["transferts"]


def test_verdict_complet(monde):
    moteur = Moteur(monde["modeles"])
    v = moteur.noter(Magasin(), "a", "b", 10_000, t=100)
    assert v["decision"] in DECISIONS and 0 <= v["score"] <= 1
    assert list(v["signaux"]) == NOMS and v["latence_ms"] >= 0
    assert (v["raisons"] == []) == (v["decision"] == "laisser_passer")


def test_noter_ne_modifie_pas_l_historique(monde):
    moteur, magasin = Moteur(monde["modeles"]), Magasin()
    magasin.ajouter(10, "TRANSFER", 5_000, "a", "b")
    premier = moteur.noter(magasin, "c", "b", 9_000)
    second = moteur.noter(magasin, "c", "b", 9_000)
    assert magasin.nb_evenements == 1 and premier["score"] == second["score"]
    assert premier["signaux"] == second["signaux"]


def test_le_service_rend_les_scores_de_l_evaluation(monde):
    r = verifier(monde["modeles"], journal=lambda *_: None)
    assert r["transferts"] > 0 and r["ecart_max"] < 0.01
    assert r["decisions_differentes"] <= max(1, r["transferts"] // 500)


def test_les_cas_de_demo_sont_coherents(monde):
    moteur = Moteur(monde["modeles"])
    for cas in json.loads((monde["modeles"] / "demo_cas.json").read_text(encoding="utf-8")):
        magasin = Magasin().charger(cas["historique"])
        v = moteur.noter(magasin, cas["src"], cas["dst"], cas["montant"], cas["t"])
        assert abs(v["score"] - cas["score_lot"]) < 0.01, cas["id"]
        if cas["id"] in ("arnaque", "collecteur"):
            assert v["decision"] != "laisser_passer" and v["raisons"], cas["id"]
        if cas["id"] in ("tontine", "commerce", "limite"):
            assert v["decision"] == "laisser_passer", cas["id"]


def test_les_raisons_ne_disent_que_des_choses_vraies():
    s = dict.fromkeys(NOMS, 0.0)
    s.update(premier_contact=1, dst_sorties_rapides=2, dst_anciennete_j=40)
    c = dict.fromkeys(NOMS, 0.0)
    c.update(dst_anciennete_j=3.0, dst_sorties_rapides=2.0, premier_contact=1.0)
    r = expliquer(s, c, k=2)
    assert len(r) == 2 and "30 minutes" in r[0] and "jamais envoyé" in r[1]   # 40 jours : pas « récent »
    assert expliquer(s, dict.fromkeys(NOMS, -1.0)) == [SANS_RAISON_DOMINANTE]


def test_flux_de_demo_lisible(monde):
    flux = pd.read_csv(monde["modeles"] / "demo_flux.csv")
    assert {"t", "type", "montant", "src", "dst", "y", "scen", "victime", "score_lot"} <= set(flux.columns)
    assert flux["t"].is_monotonic_increasing
