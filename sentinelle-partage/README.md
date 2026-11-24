# Sentinelle

Projet de l'équipe ImpactBoyz pour le GPU Challenge 2026 (Epitech Bénin, Fintech Academia,
Next Fintech Forum 2026, Cotonou).

## Le projet en dix lignes

1. Depuis le 2 novembre 2026, toutes les transactions de monnaie électronique interopérables
   de l'UEMOA passent par PI-SPI, la plateforme de paiement instantané de la BCEAO.
2. Un transfert y arrive en quelques secondes et il est irrévocable une fois confirmé.
3. Dans une arnaque par manipulation, la victime confirme elle-même : l'argent est perdu.
4. Il file ensuite par des comptes complices, les « mules », avant un retrait en espèces.
5. Le seul moment pour agir se situe avant la confirmation.
6. Sentinelle est un service de score placé chez la banque ou la fintech de l'expéditeur.
7. Il évalue le compte destinataire et renvoie un score de risque avec une raison lisible.
8. Trois issues : laisser passer, alerter l'expéditeur, bloquer.
9. Version 1 : XGBoost entraîné sur GPU. Version 2, si le temps le permet : un réseau de
   neurones sur graphe qui alimente XGBoost.
10. Limites assumées : données simulées, pas de connexion à la vraie PI-SPI.

## État du dépôt

Phase de préparation. Le dépôt contient la recherche et le script de données. Aucun code de
modèle n'est écrit tant que la roadmap n'est pas validée par l'équipe.

| Fichier | Contenu |
|---|---|
| `docs/guide-ressources.html` | Guide expliqué de toutes les ressources, à ouvrir dans un navigateur |
| `docs/ressources.md` | Données, code de référence, partenaires, versions compatibles |
| `docs/contexte-pispi.md` | PI-SPI et les règles utiles au pitch, avec les sources |
| `docs/scenarios-fraude.md` | Cinq scénarios d'arnaque à injecter dans les données |
| `docs/roadmap-proposition.md` | Proposition de roadmap, à valider |
| `scripts/telecharger_donnees.sh` | Téléchargement des jeux de données |
| `research_notes/` | Notes de recherche détaillées, avec chaque source |

## Démarrer

Il faut Linux ou macOS, `curl` et `unzip`. Aucun compte n'est nécessaire aujourd'hui.

```bash
# 1. Vérifier que les liens répondent, sans rien télécharger
scripts/telecharger_donnees.sh --test

# 2. Télécharger PaySim et IBM AML HI-Small (environ 700 Mo, 1 Go sur disque)
scripts/telecharger_donnees.sh

# 3. Un seul jeu, ou les jeux optionnels
scripts/telecharger_donnees.sh paysim
scripts/telecharger_donnees.sh momtsim-tz
```

Les fichiers arrivent dans `data/`, qui n'est pas suivi par Git.

Si Kaggle refuse le téléchargement anonyme, l'en-tête du script explique comment créer et
configurer un jeton Kaggle.

## À lire en premier

- `docs/ressources.md`, partie 1 : PaySim ne contient pas de compte mule. C'est le premier
  risque du projet.
- `docs/contexte-pispi.md`, partie 8 : ce qu'il ne faut pas dire devant le jury.
- `docs/roadmap-proposition.md` : qui fait quoi, et ce qu'on coupe si le temps manque.
