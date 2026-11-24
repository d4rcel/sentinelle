#!/usr/bin/env bash
# Sentinelle - téléchargement des jeux de données librement accessibles.
#
# Usage :
#   scripts/telecharger_donnees.sh                 # PaySim + IBM AML HI-Small (l'essentiel)
#   scripts/telecharger_donnees.sh paysim          # un seul jeu
#   scripts/telecharger_donnees.sh paysim ibm momtsim-tz momtsim-ug
#   scripts/telecharger_donnees.sh tout            # les quatre jeux
#   scripts/telecharger_donnees.sh --test          # vérifie que les liens répondent, sans rien télécharger
#
# Jeux disponibles :
#   paysim      PaySim (Kaggle ealaxi/paysim1)            186 Mo à télécharger, 471 Mo sur disque
#   ibm         IBM AML, fichiers HI-Small uniquement     environ 510 Mo
#   momtsim-tz  MoMTSim-TZ (Zenodo), première archive     environ 330 Mo
#   momtsim-ug  MoMTSim Makerere (Mendeley), petit CSV    environ 150 Mo
#
# Les fichiers arrivent dans data/<jeu>/ à la racine du projet.
# Un fichier déjà présent n'est pas retéléchargé ; un téléchargement coupé reprend où il s'était arrêté.
#
# ---------------------------------------------------------------------------
# Clé Kaggle : à configurer en secours
# ---------------------------------------------------------------------------
# Au 19 novembre 2026, Kaggle sert PaySim et IBM AML sans compte. Ce comportement n'est
# garanti nulle part. Si le téléchargement anonyme échoue, le script passe par l'outil
# officiel `kaggle`, qui demande un jeton :
#
#   1. Créer un compte sur https://www.kaggle.com
#   2. Aller sur https://www.kaggle.com/settings/api et générer un jeton d'API
#   3. Installer l'outil :         pip install kaggle
#   4. Donner le jeton, au choix :
#        export KAGGLE_API_TOKEN=<le_jeton>                  (le plus simple, aussi sur Colab)
#        mkdir -p ~/.kaggle && echo -n "<le_jeton>" > ~/.kaggle/access_token && chmod 600 ~/.kaggle/access_token
#        kaggle auth login                                   (connexion par le navigateur)
#
# L'ancien fichier ~/.kaggle/kaggle.json fonctionne encore, mais Kaggle le présente comme hérité.
# Ne jamais mettre le jeton dans le dépôt Git.
# ---------------------------------------------------------------------------

set -euo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DONNEES="${SENTINELLE_DATA:-$RACINE/data}"

KAGGLE_API="https://www.kaggle.com/api/v1/datasets/download"
PAYSIM="ealaxi/paysim1"
IBM="ealtman2019/ibm-transactions-for-anti-money-laundering-aml"
ZENODO_TZ="https://zenodo.org/api/records/22997330/files"
MENDELEY_UG="https://data.mendeley.com/public-files/datasets/zhj366m53p/files/57c2ed32-a9b6-4af8-9510-9b064625d5d7/file_downloaded"

info()   { printf '\n==> %s\n' "$*"; }
note()   { printf '    %s\n' "$*"; }
erreur() { printf 'ERREUR : %s\n' "$*" >&2; }

besoin() {
  command -v "$1" >/dev/null 2>&1 || { erreur "la commande '$1' est introuvable, installe-la puis relance."; exit 1; }
}

# Vrai si le fichier commence par la signature d'une archive zip.
est_zip() {
  [ "$(head -c 2 "$1" 2>/dev/null)" = "PK" ]
}

# telecharger <url> <fichier de destination>
# Écrit d'abord dans <destination>.partiel pour pouvoir reprendre après une coupure.
telecharger() {
  local url="$1" dest="$2"
  if [ -s "$dest" ]; then
    note "déjà présent : $dest"
    return 0
  fi
  mkdir -p "$(dirname "$dest")"
  note "téléchargement vers $dest"
  if curl --fail --location --continue-at - --retry 5 --retry-delay 5 \
          --progress-bar --output "$dest.partiel" "$url"; then
    mv "$dest.partiel" "$dest"
    return 0
  fi
  return 1
}

# Secours : outil officiel Kaggle. kaggle_cli <jeu> <dossier> [fichier]
kaggle_cli() {
  local jeu="$1" dossier="$2" fichier="${3:-}"
  if ! command -v kaggle >/dev/null 2>&1; then
    erreur "téléchargement anonyme refusé et outil 'kaggle' absent."
    erreur "Suis les instructions « Clé Kaggle » en tête de ce script, puis relance."
    return 1
  fi
  note "passage par l'outil officiel kaggle"
  mkdir -p "$dossier"
  if [ -n "$fichier" ]; then
    kaggle datasets download "$jeu" -f "$fichier" -p "$dossier" --unzip
  else
    kaggle datasets download "$jeu" -p "$dossier" --unzip
  fi
}

# Si le fichier reçu est une archive zip, l'extraire dans son dossier.
extraire_si_zip() {
  local fichier="$1" dossier
  dossier="$(dirname "$fichier")"
  if est_zip "$fichier"; then
    besoin unzip
    note "extraction de $(basename "$fichier")"
    mv "$fichier" "$fichier.zip"
    unzip -o -q "$fichier.zip" -d "$dossier"
    rm -f "$fichier.zip"
  fi
}

jeu_paysim() {
  info "PaySim (CC BY-SA 4.0) - 6 362 620 transactions de mobile money simulées"
  local dossier="$DONNEES/paysim"
  local csv="$dossier/PS_20174392719_1491204439457_log.csv"
  if [ -s "$csv" ]; then note "déjà présent : $csv"; return 0; fi
  if telecharger "$KAGGLE_API/$PAYSIM" "$dossier/paysim1.zip" && est_zip "$dossier/paysim1.zip"; then
    besoin unzip
    note "extraction"
    unzip -o -q "$dossier/paysim1.zip" -d "$dossier"
    rm -f "$dossier/paysim1.zip"
  else
    rm -f "$dossier/paysim1.zip" "$dossier/paysim1.zip.partiel"
    kaggle_cli "$PAYSIM" "$dossier"
  fi
  note "attendu : un CSV de 493 534 783 octets"
}

jeu_ibm() {
  info "IBM AML, HI-Small (CDLA-Sharing-1.0) - environ 5 millions de virements, schémas de blanchiment étiquetés"
  note "seuls les fichiers HI-Small sont pris : le jeu complet pèse 41,6 Go"
  local dossier="$DONNEES/ibm_aml" f
  for f in HI-Small_Trans.csv HI-Small_accounts.csv HI-Small_Patterns.txt; do
    if telecharger "$KAGGLE_API/$IBM/$f" "$dossier/$f"; then
      extraire_si_zip "$dossier/$f"
    else
      rm -f "$dossier/$f.partiel"
      kaggle_cli "$IBM" "$dossier" "$f"
    fi
  done
  note "attendu : HI-Small_Trans.csv de 475 664 283 octets"
}

jeu_momtsim_tz() {
  info "MoMTSim-TZ (CC BY 4.0) - mobile money simulé, Tanzanie, 12 types de fraude dont les comptes mules"
  note "première archive seulement (fichiers 1 à 5 sur 20) ; les autres sont listées sur https://doi.org/10.5281/zenodo.22997329"
  local dossier="$DONNEES/momtsim_tz"
  telecharger "$ZENODO_TZ/README.md/content" "$dossier/README.md"
  if [ -n "$(find "$dossier" -maxdepth 2 -name '*.csv' -print -quit 2>/dev/null)" ]; then
    note "CSV déjà extraits dans $dossier"
    return 0
  fi
  telecharger "$ZENODO_TZ/MoMTSim-TZ_raw_logs_part01-05.zip/content" "$dossier/part01-05.zip"
  besoin unzip
  note "extraction"
  unzip -o -q "$dossier/part01-05.zip" -d "$dossier"
  rm -f "$dossier/part01-05.zip"
}

jeu_momtsim_ug() {
  info "MoMTSim Makerere (CC BY 4.0) - mobile money simulé, Ouganda, même schéma que PaySim"
  note "attention : 52,8 % de fraude dans ce fichier, ce qui n'est pas réaliste"
  telecharger "$MENDELEY_UG" "$DONNEES/momtsim_ug/synthetic_mobile_money_transaction_dataset.csv"
}

# Vérifie qu'un lien répond en ne demandant que ses 100 premiers octets.
tester_lien() {
  local nom="$1" url="$2" code
  code="$(curl --silent --location --range 0-99 --output /dev/null --write-out '%{http_code}' --max-time 60 "$url" || true)"
  case "$code" in
    200|206) printf '    OK      %s (HTTP %s)\n' "$nom" "$code" ;;
    *)       printf '    ÉCHEC   %s (HTTP %s)\n' "$nom" "$code"; return 1 ;;
  esac
}

mode_test() {
  info "Test des liens, sans téléchargement"
  local echecs=0
  tester_lien "PaySim (Kaggle, anonyme)"         "$KAGGLE_API/$PAYSIM"                              || echecs=$((echecs + 1))
  tester_lien "IBM AML HI-Small_Trans.csv"       "$KAGGLE_API/$IBM/HI-Small_Trans.csv"              || echecs=$((echecs + 1))
  tester_lien "IBM AML HI-Small_accounts.csv"    "$KAGGLE_API/$IBM/HI-Small_accounts.csv"           || echecs=$((echecs + 1))
  tester_lien "IBM AML HI-Small_Patterns.txt"    "$KAGGLE_API/$IBM/HI-Small_Patterns.txt"           || echecs=$((echecs + 1))
  tester_lien "MoMTSim-TZ (Zenodo)"              "$ZENODO_TZ/MoMTSim-TZ_raw_logs_part01-05.zip/content" || echecs=$((echecs + 1))
  tester_lien "MoMTSim Makerere (Mendeley)"      "$MENDELEY_UG"                                     || echecs=$((echecs + 1))
  if [ "$echecs" -gt 0 ]; then
    erreur "$echecs lien(s) en échec. Pour Kaggle, configure le jeton (voir l'en-tête du script)."
    exit 1
  fi
  note "tous les liens répondent"
}

besoin curl

if [ "$#" -eq 0 ]; then
  set -- paysim ibm
fi

for cible in "$@"; do
  case "$cible" in
    --test)      mode_test ;;
    paysim)      jeu_paysim ;;
    ibm)         jeu_ibm ;;
    momtsim-tz)  jeu_momtsim_tz ;;
    momtsim-ug)  jeu_momtsim_ug ;;
    tout)        jeu_paysim; jeu_ibm; jeu_momtsim_tz; jeu_momtsim_ug ;;
    -h|--help)   sed -n '2,36p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//' ;;
    *)           erreur "jeu inconnu : $cible (choix : paysim, ibm, momtsim-tz, momtsim-ug, tout, --test)"; exit 1 ;;
  esac
done

if [ -d "$DONNEES" ]; then
  info "Contenu de $DONNEES"
  du -sh "$DONNEES"/* 2>/dev/null | sed 's/^/    /' || true
fi
