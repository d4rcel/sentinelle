# Sentinelle : lancer, tester, présenter

Ce dossier contient maintenant le système complet : le modèle entraîné, le service de score,
l'écran de démonstration et les tests.

## En une commande

```bash
bash lancer.sh
```

La première fois, la commande :

1. crée un environnement Python dans `.venv/` et installe les paquets (Internet nécessaire) ;
2. intègre le modèle déposé dans `modeles/` : elle reconstruit les données simulées, note tous
   les transferts, règle les seuils et prépare les données de la démo. Aucun entraînement ;
3. vérifie que le service rend les mêmes scores que l'évaluation ;
4. lance le service sur http://127.0.0.1:8000/docs et la démo sur http://localhost:8501.

Il faut PaySim sur la machine. Le fichier est cherché dans `data/`, `../data/` et `../../data/`
(donc dans `Projects/data/paysim/`), ou à l'adresse donnée par la variable `SENTINELLE_PAYSIM`.
L'intégration lit les 6,3 millions de lignes : prévoir quelques gigaoctets de mémoire libre.

## D'où vient le modèle

`modeles/sentinelle_v1.ubj` a été entraîné sur CPU le 25 novembre 2026 avec `bash lancer.sh entrainer`
(17 signaux, découpage sur les jours pleins). Le notebook `notebooks/sentinelle_v1_kaggle.ipynb` décrit
la version précédente (19 signaux, test sur les jours 24 à 30) et reste à réaligner. Le service ne l'entraîne jamais : il le
charge, et il tourne sans GPU.

Pour le remplacer par un modèle entraîné sur GPU (Kaggle ou machine du hackathon) :

```bash
cp ~/Téléchargements/sentinelle_v1.ubj modeles/     # le nouveau fichier
bash lancer.sh integrer                             # recalcule seuils, mesures et données de démo
bash lancer.sh                                      # relance
```

Sur la machine GPU du hackathon, le dépôt sait aussi entraîner et chronométrer :

```bash
bash lancer.sh entrainer --volume 20     # XGBoost sur GPU s'il y en a un, temps CPU et GPU notés
```

## Tester

| Commande | Ce qu'elle vérifie |
|---|---|
| `bash lancer.sh tests` | Aucun signal ne lit le futur ni les soldes ; le calcul en ligne égale le calcul par lot ; les verdicts, les raisons et les routes du service. Utilise un petit jeu fabriqué, sans PaySim. |
| `bash lancer.sh verifier` | Rejoue le flux de démo par le service et compare chaque score à l'évaluation. |
| `python scripts/essai_api.py 1000` | Temps de réponse du service sur 1 000 appels (le service doit tourner). |

Essai à la main du service :

```bash
curl -s -X POST http://127.0.0.1:8000/noter -H 'Content-Type: application/json' \
  -d '{"expediteur": "VICTIME-1", "destinataire": "COMPTE-X", "montant": 180000}'
```

Routes : `POST /noter` (verdict, sans rien enregistrer), `POST /transferts` et `POST /retraits`
(opérations confirmées), `GET /comptes/{id}`, `GET /sante`, `POST /reinitialiser`.

## La console institution

Ouvrir http://127.0.0.1:8000/demo une fois le service lancé (`bash lancer.sh`, ou `bash lancer.sh console`
pour elle seule). Elle s'adresse à un établissement : banque, opérateur, prestataire de paiement.

| Vue | Ce qu'elle montre |
|---|---|
| Flux en direct | Les 7 432 transferts du flux traversent Sentinelle. Chacun passe ou est bloqué avant l'envoi. Un curseur règle le seuil de blocage de l'établissement et reclasse aussitôt le trafic : arnaques arrêtées d'un côté, clients honnêtes bloqués à tort de l'autre. |
| Risque et conformité | La file des transferts bloqués et des transactions envoyées à la main. L'analyste confirme la fraude (le compte passe sous surveillance, ses prochains transferts sont bloqués), déclare une fausse alerte (le compte est déclaré de confiance), ou ouvre une analyse approfondie (ticket interne). |
| Transaction unique | Choisir une transaction préparée dans une liste (les champs se remplissent), ou saisir la sienne, puis l'envoyer. Elle est notée et transmise à la file du département risque. |

Déroulé conseillé en deux minutes : lancer le flux en vitesse « Rapide », passer de « Recommandé » à
« Bloquer tôt » pour montrer le prix d'un seuil trop bas, ouvrir « Risque et conformité », confirmer une
fraude, libérer une fausse alerte, puis envoyer une transaction préparée.

Si le jury demande « et sans votre solution ? » : ouvrir http://127.0.0.1:8000/demo/sans. La page rejoue
le même flux sans Sentinelle : rien n'est noté, tout passe, et un compteur suit les arnaques parties. Elle
est indépendante de la console. À dire : « sans contrôle sur le comportement du compte destinataire », car
un établissement a déjà d'autres règles, comme des plafonds de montant.

Présentation sur deux fenêtres : ouvrir http://127.0.0.1:8000/demo#flux d'un côté et
http://127.0.0.1:8000/demo#risque de l'autre, dans le même navigateur. Les fenêtres partagent leur état :
un transfert bloqué à gauche apparaît aussitôt dans la file à droite, et une décision de l'analyste est
prise en compte par le flux.

À dire : la décision automatique tombe avant l'envoi, parce qu'un transfert confirmé est irrévocable. L'analyste
intervient ensuite. Le seuil, les tickets et les listes de surveillance et de confiance vivent dans le
navigateur : rien n'est relié à un outil interne réel. Les montants suivent PaySim, pas le franc CFA.

## L'écran de démo

| Onglet | Ce qu'il montre |
|---|---|
| L'arnaque en direct | Cinq situations tirées de la période de test : deux arnaques signalées, deux cas légitimes qui passent, et la limite (une mule toute neuve, non détectée). L'interrupteur « Sentinelle activée » montre la différence avec et sans. |
| Trois heures rejouées | Tous les transferts de trois heures du premier jour de test, notés un par un. Compteurs d'alertes, de fausses alertes et d'argent envoyé à des fraudeurs, avec et sans Sentinelle. |
| Bac à sable | Un monde vide pour inventer des comptes, enregistrer des transferts et des retraits, et voir le score réagir. |
| Mesures et limites | Les mesures du modèle chargé, par scénario, et le contrôle « le modèle intégré est-il celui évalué ? ». |

Déroulé conseillé en trois minutes : situation 1 avec Sentinelle coupée (confirmer, voir l'argent
partir), puis la même avec Sentinelle activée ; situation 3 pour montrer qu'une tontine passe ;
situation 5 pour dire la limite ; puis « Jouer tout le flux » pour les chiffres.

## Ce qu'il ne faut pas faire dire à cette démo

- Les données sont simulées : PaySim comme trafic de fond, plus nos scénarios injectés. Délais,
  montants et nombre de mules sont nos hypothèses. Aucune connexion à la vraie PI-SPI.
- Les montants suivent PaySim, dont la monnaie est masquée. Le « F » de l'écran est une commodité.
- « Avec Sentinelle » suppose que chaque expéditeur alerté renonce à son transfert.
- Le premier transfert vers une mule qui n'a encore rien fait est rarement détecté.
- Sur 100 alertes, environ un tiers visent une vraie fraude : ne jamais dire « compte frauduleux »,
  dire « transaction à risque ». Le modèle signale, le prestataire de paiement décide.
- Une chaîne de mules jamais vue à l'entraînement lui échappe presque entièrement.
- Tant qu'aucun entraînement n'a tourné sur GPU, il n'y a pas de gain GPU à annoncer.

## Où est quoi

| Fichier | Rôle |
|---|---|
| `sentinelle/donnees.py` | PaySim et injection des scénarios (même code et même graine que le notebook) |
| `sentinelle/signaux.py` | Les 17 signaux, calculés par lot (numpy sur CPU, cupy sur GPU) |
| `sentinelle/magasin.py` | L'historique des comptes en mémoire et les mêmes signaux, un transfert à la fois |
| `sentinelle/moteur.py` | Charge le modèle, rend score, décision et raisons |
| `sentinelle/raisons.py` | Les phrases de la raison lisible |
| `sentinelle/integrer.py` | Intègre un modèle déposé : seuils, mesures, données de démo |
| `sentinelle/entrainer.py` | Entraînement, sur GPU s'il y en a un |
| `sentinelle/api.py` | Le service FastAPI |
| `demo/app.py` | L'écran Streamlit |
| `tests/` | Les tests automatiques |
| `modeles/` | Le modèle et, après intégration, ses mesures et les données de démo |
