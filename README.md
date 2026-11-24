# Sentinelle

**Détection des arnaques au Mobile Money avant que l'argent ne parte.**

Projet de l'équipe ImpactBoyz pour le GPU Challenge 2026 (Epitech Bénin, Fintech Academia,
Next Fintech Forum 2026, Cotonou).

---

## Le problème

Depuis le 2 novembre 2026, les transactions de monnaie électronique interopérables de l'UEMOA
passent par **PI-SPI**, la plateforme de paiement instantané de la BCEAO. Un transfert y arrive
en quelques secondes et devient **irrévocable** une fois confirmé.

Dans une arnaque par manipulation (faux « transfert par erreur », faux agent du service client),
c'est la victime elle-même qui confirme. L'argent file ensuite par des comptes complices, les
« mules », avant d'être retiré en espèces. Le seul moment où l'on peut encore agir, c'est
**avant la confirmation**.

## La solution

Sentinelle est un service de score installé chez la banque ou la fintech de l'expéditeur. Au
moment où un client s'apprête à envoyer de l'argent, il évalue le **compte destinataire** et
renvoie :

- un **score de risque** entre 0 et 1 ;
- une **décision** : `laisser_passer`, `alerter` ou `bloquer` ;
- une **raison lisible** à afficher au client, par exemple : « ce compte a reçu de l'argent de
  6 nouveaux expéditeurs en 24 heures » ou « ce compte ne garde presque rien de ce qu'il
  reçoit ».

```
 Client           Banque / fintech                Sentinelle
   │  envoyer 180 000 ──►  │                            │
   │                       │ ── POST /noter ──────────► │  19 signaux sur l'historique
   │                       │ ◄── score, décision, ──────│  du destinataire et de l'expéditeur
   │ ◄── alerte + raison ──│     raisons                │  + modèle XGBoost
   │  (renonce ou confirme)│                            │
```

## Résultats (version 1, XGBoost)

Mesures sur la période de test, jamais vue à l'entraînement (20 924 transferts, 722 fraudes) :

| Mesure | Valeur |
|---|---|
| Fraudes signalées (alerte ou blocage) | **86,4 %** |
| Fraudes bloquées | 84,8 % |
| Fausses alertes sur les transferts légitimes | 1,2 % |
| Faux blocages | 0,07 % |
| Précision moyenne (hasard : 0,035) | 0,903 |
| Scénario « chaîne de mules », **caché à l'entraînement** | 87,2 % signalés |

Les tontines, les paiements de commerçants et les envois d'étudiants injectés comme
contre-exemples ne déclenchent aucune alerte.

**Limite assumée :** le tout premier transfert vers une mule qui n'a encore rien fait est
presque jamais détecté (3 sur 39). Sentinelle repère un compte à son comportement ; un compte
vierge n'en a pas encore.

## Comment ça marche

1. **Données.** [PaySim](https://www.kaggle.com/datasets/ealaxi/paysim1) (6,3 millions de
   transactions Mobile Money simulées) sert de trafic de fond. On y injecte quatre scénarios
   d'arnaque inspirés de cas béninois documentés, et des contre-exemples légitimes.
2. **Signaux.** 19 signaux calculés sans regarder le futur ni les soldes : ancienneté du
   destinataire, nombre de nouveaux expéditeurs en 24 h et 72 h, part de l'argent ressorti
   en quelques minutes, montant inhabituel, premier contact entre les deux comptes, etc.
   Calcul par lot avec numpy sur CPU ou cupy sur GPU, et calcul identique transfert par
   transfert dans le service.
3. **Modèle.** XGBoost, entraîné sur GPU quand il y en a un. Découpage dans le temps :
   entraînement avant le jour 20, validation des jours 20 à 23, test à partir du jour 24.
4. **Seuils.** Réglés sur la validation pour viser 1 % de fausses alertes et 0,1 % de faux
   blocages.

| Scénario injecté | Ce qui se passe |
|---|---|
| S1 — Transfert par erreur | « Je me suis trompé de numéro, renvoyez-moi l'argent » |
| S2 — Faux agent | Un faux service client obtient un transfert ou un code |
| S3 — Compte collecteur | Un compte reçoit de nombreuses victimes et vide aussitôt |
| S4 — Chaîne de mules | L'argent rebondit de compte en compte avant le retrait |

## Démarrer

Il faut Linux ou macOS, Python 3.10 ou plus récent (3.12 conseillé), et PaySim sur la machine.

```bash
cd app

# 1. Télécharger PaySim dans data/ (aucun compte nécessaire)
scripts/telecharger_donnees.sh paysim

# 2. Installer, intégrer le modèle, vérifier, puis lancer le service et la démo
bash lancer.sh
```

- Service : http://127.0.0.1:8000/docs
- Écran de démonstration : http://localhost:8501

Autres commandes :

| Commande | Rôle |
|---|---|
| `bash lancer.sh tests` | Tests automatiques, sur un petit jeu fabriqué (sans PaySim) |
| `bash lancer.sh api` | Le service seul |
| `bash lancer.sh verifier` | Vérifie que le service rend les scores de l'évaluation |
| `bash lancer.sh integrer` | Intègre un nouveau modèle déposé dans `app/modeles/` |
| `bash lancer.sh entrainer --volume 20` | Entraîne ici et chronomètre CPU contre GPU |

Essai du service :

```bash
curl -s -X POST http://127.0.0.1:8000/noter -H 'Content-Type: application/json' \
  -d '{"expediteur": "VICTIME-1", "destinataire": "COMPTE-X", "montant": 180000}'
```

Le guide complet (déroulé de la démo, routes, ce qu'il ne faut pas faire dire au modèle) se
trouve dans [`app/LANCER-LA-DEMO.md`](app/LANCER-LA-DEMO.md).

## L'écran de démo

| Onglet | Ce qu'il montre |
|---|---|
| L'arnaque en direct | Cinq situations tirées de la période de test (simulée), avec un interrupteur « Sentinelle activée » |
| Une journée rejouée | Tous les transferts d'une journée, avec et sans Sentinelle : alertes, fausses alertes, argent perdu |
| Bac à sable | Créer des comptes et des transferts, et voir le score réagir |
| Mesures et limites | Les mesures du modèle chargé, scénario par scénario |

## Organisation du dépôt

```
app/
├── sentinelle/        Le cœur : données, signaux, moteur de score, service FastAPI
├── demo/app.py        L'écran de démonstration (Streamlit)
├── modeles/           Le modèle entraîné, ses seuils, ses mesures et les données de démo
├── notebooks/         Le notebook Kaggle qui a entraîné la version 1
├── tests/             Les tests automatiques (pytest)
├── scripts/           Téléchargement des données, essai de charge du service
├── docs/              Contexte PI-SPI, scénarios de fraude, ressources, roadmap
├── research_notes/    Notes de recherche détaillées, chaque affirmation sourcée
└── lancer.sh          Point d'entrée unique
```

## Pile technique

Python · XGBoost · numpy / cupy · pandas · scikit-learn · FastAPI · Streamlit · pytest ·
entraînement sur Kaggle et sur la machine GPU du hackathon.

## Limites

- Les données sont **simulées** : PaySim comme trafic de fond et nos scénarios injectés. Délais,
  montants et nombre de mules sont nos hypothèses. Aucune connexion à la vraie PI-SPI.
- La monnaie de PaySim est masquée : le « F » affiché par la démo est une commodité.
- Le gain « avec Sentinelle » suppose que chaque expéditeur alerté renonce à son transfert.
- Le modèle actuel a été entraîné sur CPU (Kaggle). Aucun gain GPU n'est annoncé tant qu'un
  entraînement GPU n'a pas été chronométré.

## Suite prévue

- Entraînement et mesure du temps sur la machine GPU du hackathon.
- Version 2 : un réseau de neurones sur graphe (GNN) qui produit des signaux pour XGBoost,
  pour mieux repérer les chaînes de mules.
- Scénario 5 (point de vente vidé), documenté dans `app/docs/scenarios-fraude.md`, pas encore
  injecté.
