"""Un petit monde complet (faux PaySim, modèle entraîné, démo exportée), construit une fois pour tous les tests."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))


@pytest.fixture(scope="session")
def monde(tmp_path_factory):
    pytest.importorskip("xgboost")
    import faux_paysim
    from sentinelle import config, entrainer
    dossier = tmp_path_factory.mktemp("monde")
    paysim = faux_paysim.ecrire(dossier / "PS_faux_log.csv")
    modeles = dossier / "modeles"
    entrainer.main(["--paysim", str(paysim), "--modeles", str(modeles), "--n", "40"])
    ancien = config.MODELES
    config.MODELES = modeles                # le service et la démo liront ce dossier
    yield {"paysim": paysim, "modeles": modeles}
    config.MODELES = ancien
