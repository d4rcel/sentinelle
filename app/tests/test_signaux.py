"""Les signaux : pas de fuite, et le calcul en ligne donne les mêmes valeurs que le calcul par lot."""
import numpy as np

import faux_paysim
from sentinelle import donnees
from sentinelle.config import JOUR
from sentinelle.magasin import Magasin
from sentinelle.signaux import NOMS, preparer_evenements, signaux


def _donnees(tmp_path):
    tout, _ = donnees.construire(faux_paysim.ecrire(tmp_path / "PS_faux_log.csv", n=40_000), seed=1, n=25)
    return tout, preparer_evenements(tout)


def test_aucune_colonne_de_solde(tmp_path):
    tout, _ = _donnees(tmp_path)
    assert not [c for c in tout.columns if "balance" in c.lower() or "solde" in c.lower()]
    assert not [n for n in NOMS if "solde" in n or "balance" in n]


def test_aucun_signal_ne_lit_le_futur(tmp_path):
    _, ev = _donnees(tmp_path)
    complet = signaux(np, **ev)
    coupe = ev["t"] < 15 * JOUR
    tronque = signaux(np, **{k: v[coupe] for k, v in ev.items()})
    avant = ev["t"][ev["est_tr"]] < 15 * JOUR
    assert np.allclose(complet[avant].to_numpy(), tronque.to_numpy(), rtol=1e-4, atol=1e-2)


def test_en_ligne_egale_par_lot(tmp_path):
    tout, ev = _donnees(tmp_path)
    lot = signaux(np, **ev).to_numpy()
    magasin, en_ligne = Magasin(), []
    for t, type_, montant, src, dst in tout[["t", "type", "montant", "src", "dst"]].itertuples(index=False, name=None):
        if type_ == "TRANSFER":
            en_ligne.append(list(magasin.signaux(t, src, dst, montant).values()))
        magasin.ajouter(t, type_, montant, src, dst)
    assert np.allclose(lot, np.array(en_ligne, dtype=np.float32), rtol=1e-4, atol=1e-2)


def test_un_compte_qui_vide_vite_est_marque():
    m = Magasin()
    m.ajouter(1000, "TRANSFER", 50_000, "victime1", "mule")
    m.ajouter(1300, "CASH_OUT", 49_000, "mule", "agent")          # 5 minutes après l'entrée
    s = m.signaux(5000, "victime2", "mule", 80_000)
    assert s["dst_sorties_rapides"] == 1 and s["dst_part_sorties_rapides"] == 1
    assert s["premier_contact"] == 1 and s["dst_nb_recus"] == 1 and s["dst_nouveaux_exp_24h"] == 1
    assert m.signaux(5000, "victime1", "mule", 80_000)["premier_contact"] == 0
