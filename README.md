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

Sentinelle est un service de score appelé par le **prestataire de paiement** de l'expéditeur
(banque, opérateur de mobile money, fintech). Au moment où un client s'apprête à envoyer de
l'argent, il évalue le comportement du **compte destinataire** et renvoie au prestataire :

- un **score de risque** entre 0 et 1 sur la transaction ;
- une **décision proposée** : `laisser_passer`, `alerter` ou `bloquer` ;
- une **raison lisible**, par exemple : « ce compte a reçu de l'argent de
  6 nouveaux expéditeurs en 24 heures » ou « ce compte ne garde presque rien de ce qu'il
  reçoit ».

Le modèle signale une **transaction à risque**, il ne désigne pas un « compte frauduleux » : c'est
le prestataire qui décide de laisser passer, d'avertir son client ou de bloquer.

```
 Client           Banque / fintech                Sentinelle
   │  envoyer 180 000 ──►  │                            │
   │                       │ ── POST /noter ──────────► │  17 signaux sur l'historique
   │                       │ ◄── score, décision, ──────│  du destinataire et de l'expéditeur
   │ ◄── alerte + raison ──│     raisons                │  + modèle XGBoost
   │  (renonce ou confirme)│                            │
```

## Résultats (version 1, XGBoost)

Mesures sur la période de test, jamais vue à l'entraînement : jours 14 à 17, 140 040 transferts
dont 951 frauduleux (0,68 %). Ce sont des journées pleines de PaySim, où la fraude a sa rareté
normale.

La mesure principale porte sur les **transferts de victimes** (684) : ce sont les seuls que l'on
peut encore arrêter. Les transferts entre comptes complices ont lieu après le vol.

| Méthode | Transferts de victimes signalés | Fausses alertes | Alertes justes |
|---|---|---|---|
| **Référence simple** : une règle, sans apprentissage | 50,3 % | 0,24 % | 52,3 % |
| **Modèle XGBoost**, 17 signaux | **71,9 %** | 0,97 % | 31,3 % |

La règle : alerter si le compte destinataire a déjà fait ressortir de l'argent moins de
30 minutes après l'avoir reçu. Le modèle trouve 21 points de transferts de victimes en plus,
au prix de quatre fois plus de fausses alertes. Sur 100 alertes du modèle, 31 visent une vraie
fraude.

| Autres mesures du modèle | Valeur |
|---|---|
| Transferts de victimes bloqués | 70,9 % |
| Faux blocages | 0,09 % |
| Tous transferts frauduleux signalés, complices compris | 64,4 % |
| Précision moyenne (hasard : 0,007) | 0,658 |

Fausses alertes sur les contre-exemples honnêtes : commerçants 0 %, tontines 0,3 %,
étudiants 5,0 %, comptes neufs ordinaires 8,6 %.

**Limites mesurées :**

- **Scénario « chaîne de mules », caché à l'entraînement : 3 transferts de victimes signalés
  sur 43.** Le premier compte de la chaîne a l'air propre ; ce sont ses voisins qui le
  trahissent, et le modèle ne les regarde pas encore.
- **Premier transfert vers une mule qui n'a encore rien reçu : 23 signalés sur 85.** Sentinelle
  repère un compte à son comportement ; un compte vierge n'en a pas encore.

## Comment ça marche

1. **Données.** [PaySim](https://www.kaggle.com/datasets/ealaxi/paysim1) (6,3 millions de
   transactions Mobile Money simulées) sert de trafic de fond. On y injecte quatre scénarios
   d'arnaque inspirés de cas béninois documentés, et des contre-exemples légitimes.
2. **Signaux.** 17 signaux calculés sans regarder le futur ni les soldes : ancienneté du
   destinataire, nombre de nouveaux expéditeurs en 24 h et 72 h, part de l'argent ressorti
   en quelques minutes, montant inhabituel, premier contact entre les deux comptes, etc.
   Calcul par lot avec numpy sur CPU ou cupy sur GPU, et calcul identique transfert par
   transfert dans le service.
3. **Modèle.** XGBoost, entraîné sur GPU quand il y en a un. Découpage dans le temps :
   entraînement sur les jours 1 à 11, validation sur les jours 12 et 13, test sur les jours 14
   à 17. Après le jour 17, PaySim est presque vide : la part de fraude y serait cinq fois trop
   élevée.
4. **Seuils.** Réglés sur la validation pour viser 1 % de fausses alertes et 0,1 % de faux
   blocages.

| Scénario injecté | Ce qui se passe |
|---|---|
| S1 : Transfert par erreur | « Je me suis trompé de numéro, renvoyez-moi l'argent » |
| S2 : Faux agent | Un faux service client obtient un transfert ou un code |
| S3 : Compte collecteur | Un compte reçoit de nombreuses victimes et vide aussitôt |
| S4 : Chaîne de mules | L'argent rebondit de compte en compte avant le retrait |

## Démarrer

Il faut Linux ou macOS, Python 3.10 ou plus récent (3.12 conseillé), et PaySim sur la machine.

```bash
cd app

# 1. Télécharger PaySim dans data/ (aucun compte nécessaire)
scripts/telecharger_donnees.sh paysim

# 2. Installer, intégrer le modèle, vérifier, puis lancer le service et la démo
bash lancer.sh
```

- **Console institution : http://127.0.0.1:8000/demo** (flux en direct, file du département risque et
  conformité, transaction unique)
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
| Trois heures rejouées | Tous les transferts de trois heures du test, avec et sans Sentinelle : alertes, fausses alertes, argent perdu |
| Bac à sable | Créer des comptes et des transferts, et voir le score réagir |
| Mesures et limites | Les mesures du modèle chargé, scénario par scénario |

## Organisation du dépôt

```
app/
├── sentinelle/        Le cœur : données, signaux, moteur de score, service FastAPI
├── demo/app.py        L'écran de démonstration (Streamlit)
├── modeles/           Le modèle entraîné, ses seuils, ses mesures et les données de démo
├── notebooks/         Le notebook Kaggle de la version précédente (à réaligner)
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
- Les quatre scénarios d'arnaque sont écrits par l'équipe : le modèle est évalué sur des fraudes
  que nous avons imaginées, pas sur de vraies fraudes.
- Deux signaux sur l'expéditeur (son ancienneté, et « il vient de recevoir de l'argent ») ont été
  retirés : dans PaySim, un expéditeur honnête n'a presque jamais de passé, et le modèle apprenait
  à se méfier de tout expéditeur déjà connu.
- Le modèle actuel a été entraîné sur CPU. Aucun gain GPU n'est annoncé tant qu'un
  entraînement GPU n'a pas été chronométré.

## Suite prévue

- Entraînement et mesure du temps sur la machine GPU du hackathon.
- Faire resservir les chaînes de mules pour plusieurs victimes dans le simulateur, et ajouter
  les plaintes comme signal.
- Sécuriser le service : authentification, et ne plus renvoyer le détail des signaux à l'appelant.
- Version 2 : un réseau de neurones sur graphe (GNN) qui produit des signaux pour XGBoost,
  pour mieux repérer les chaînes de mules.
- Scénario 5 (point de vente vidé), documenté dans `app/docs/scenarios-fraude.md`, pas encore
  injecté.
