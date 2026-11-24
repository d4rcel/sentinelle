#!/usr/bin/env bash
# Sentinelle : installe les paquets, intègre le modèle, puis lance le service et la démo.
#
#   bash lancer.sh              service + écran de démo (par défaut)
#   bash lancer.sh tests        tests automatiques (petit jeu de données fabriqué, sans PaySim)
#   bash lancer.sh api          le service seul, sur http://127.0.0.1:8000
#   bash lancer.sh integrer     réintégrer le modèle déposé dans modeles/
#   bash lancer.sh entrainer    entraîner ici (ajouter --volume 20 pour chronométrer CPU contre GPU)
#   bash lancer.sh verifier     vérifier que le service rend les scores de l'évaluation
set -euo pipefail
cd "$(dirname "$0")"
PYTHON="${PYTHON:-python3}"
PORT_API="${PORT_API:-8000}"
PORT_DEMO="${PORT_DEMO:-8501}"

if [ ! -x .venv/bin/python ]; then
  echo "== Création de l'environnement Python (.venv)"
  "$PYTHON" -m venv .venv || { echo "Impossible de créer .venv. Sur Ubuntu : sudo apt install python3-venv"; exit 1; }
fi
# shellcheck disable=SC1091
source .venv/bin/activate
if [ ! -f .venv/.installe ] || [ requirements.txt -nt .venv/.installe ]; then
  echo "== Installation des paquets (plusieurs minutes la première fois, Internet nécessaire)"
  python -m pip install --quiet --upgrade pip
  python -m pip install --quiet -r requirements.txt
  touch .venv/.installe
fi

preparer() {
  if [ ! -f modeles/sentinelle_v1.ubj ]; then
    echo "== Aucun modèle dans modeles/ : entraînement sur cette machine"
    python -m sentinelle.entrainer
  elif [ ! -f modeles/demo_flux.csv ] || [ modeles/sentinelle_v1.ubj -nt modeles/demo_flux.csv ]; then
    echo "== Intégration du modèle déposé dans modeles/ (environ une minute, sans entraînement)"
    python -m sentinelle.integrer
  fi
}

case "${1:-demo}" in
  demo)
    preparer
    echo "== Vérification : le service rend-il les scores de l'évaluation ?"
    python -m sentinelle.verifier
    uvicorn sentinelle.api:app --port "$PORT_API" --log-level warning &
    API=$!
    trap 'kill $API 2>/dev/null || true' EXIT
    echo "== Service : http://127.0.0.1:$PORT_API/docs     Démo : http://localhost:$PORT_DEMO     (Ctrl+C pour arrêter)"
    streamlit run demo/app.py --server.port "$PORT_DEMO" --server.headless true --browser.gatherUsageStats false
    ;;
  api)       preparer; uvicorn sentinelle.api:app --port "$PORT_API" ;;
  tests)     python -m pytest -q tests ;;
  integrer)  python -m sentinelle.integrer ;;
  entrainer) shift; python -m sentinelle.entrainer "$@" ;;
  verifier)  python -m sentinelle.verifier ;;
  *)         sed -n '2,10p' "$0"; exit 1 ;;
esac
