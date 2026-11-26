"""Le service HTTP, appelé comme le ferait l'établissement de l'expéditeur."""
import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")


@pytest.fixture()
def client(monde):
    from fastapi.testclient import TestClient
    from sentinelle import api
    api._etat.clear()
    return TestClient(api.app)


def test_sante(client):
    r = client.get("/sante").json()
    assert r["etat"] == "ok" and r["signaux"] == 17 and r["comptes_connus"] > 0


def test_noter_puis_enregistrer(client):
    op = {"expediteur": "essai-victime", "destinataire": "essai-compte", "montant": 150000}
    v = client.post("/noter", json=op).json()
    assert v["decision"] in ("laisser_passer", "alerter", "bloquer") and 0 <= v["score"] <= 1
    assert client.get("/comptes/essai-compte").json()["connu"] is False       # noter n'enregistre rien
    assert client.post("/transferts", json=op).json()["enregistre"] is True
    assert client.get("/comptes/essai-compte").json()["transferts_recus"] == 1
    assert client.post("/retraits", json={"expediteur": "essai-compte", "destinataire": "agent", "montant": 149000}).status_code == 200
    apres = client.post("/noter", json={**op, "expediteur": "essai-victime-2"}).json()
    assert apres["signaux"]["dst_nb_recus"] == 1 and apres["signaux"]["dst_nb_sorties"] == 1


def test_montant_invalide_refuse(client):
    assert client.post("/noter", json={"expediteur": "a", "destinataire": "b", "montant": -5}).status_code == 422


def test_console_institution(client):
    assert "Sentinelle" in client.get("/demo").text and client.get("/demo/sans").status_code == 200
    d = client.get("/demo/donnees").json()
    t = d["transferts"]
    assert len(t) > 0 and 0 < d["seuils"]["avertir"] <= d["seuils"]["bloquer"]
    assert all(0 <= x["score"] <= 1 and {"src", "dst", "montant", "raisons", "victime", "apercu"} <= set(x) for x in t)
    assert all(x["raisons"] for x in t if x["score"] >= d["seuils"]["avertir"])      # toute alerte a sa raison
    v = client.post("/demo/noter", json={"expediteur": "essai", "destinataire": "jamais-vu", "montant": 150000}).json()
    assert 0 <= v["score"] <= 1 and v["raisons"] and v["apercu"]["dst_nb_recus"] == 0
    assert client.post("/demo/noter", json={"expediteur": "a", "destinataire": "b", "montant": 0}).status_code == 422


def test_reinitialiser(client):
    client.post("/transferts", json={"expediteur": "x1", "destinataire": "x2", "montant": 1000})
    avant = client.post("/reinitialiser").json()["operations_connues"]
    assert client.get("/comptes/x2").json()["connu"] is False and avant > 0
