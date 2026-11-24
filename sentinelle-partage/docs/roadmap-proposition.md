# Proposition de roadmap — à valider

Rédigée le 19 novembre 2026. **Ce document est une proposition.** Rien n'est engagé, et aucun
code de modèle n'est écrit tant que l'équipe ne l'a pas validé.

Calendrier retenu : préparation du vendredi 20 au mardi 24 novembre, hackathon les mercredi 25
et jeudi 26 novembre.

## Trois décisions à prendre avant de commencer

### Décision 1 — Les données

Constat mesuré : PaySim ne contient pas de compte mule. Aucun compte n'y reçoit plus de deux
fraudes, et l'argent ne ressort pas par le compte qui l'a reçu. Tout le signal « mule » viendra
de nos propres scénarios injectés.

Le risque : un juré demande « votre modèle retrouve les fraudes que vous avez écrites
vous-mêmes, qu'est-ce que cela prouve ? ».

Proposition :

1. Garder PaySim comme trafic de fond et y injecter nos scénarios. C'est ce que la démo montre.
2. Tirer les paramètres de chaque scénario au hasard (montants, délais, nombre de mules), et
   injecter les contre-exemples légitimes.
3. Cacher un scénario entier à l'entraînement, par exemple la chaîne de mules, et mesurer si le
   modèle le détecte quand même. C'est la réponse honnête à la question du juré.
4. En contrôle indépendant, mesurer les mêmes signaux sur IBM AML HI-Small, dont les schémas de
   réseau ont été étiquetés par d'autres que nous.
5. Examiner MoMTSim-TZ pendant deux heures, pas plus. S'il contient des comptes mules qui se
   répètent, il devient un meilleur jeu d'entraînement que PaySim.

### Décision 2 — La place du GPU

Le défi demande d'« exploiter pleinement la puissance des GPU ». Or XGBoost s'entraîne sur
PaySim en quelques minutes sans GPU (estimation, non mesurée). Avec la version 1 seule, le GPU
paraîtra décoratif.

Proposition : faire du gain mesuré un résultat du projet.

- Chronométrer la même chaîne sur CPU puis sur GPU : préparation des signaux avec pandas puis
  cuDF, entraînement XGBoost, calcul des raisons.
- Grossir le volume pour que la mesure ait un sens : plusieurs mois de trafic simulé, ou IBM
  AML HI-Medium (32 millions de transactions).
- Dire clairement que le service de score, lui, tourne sans GPU. C'est un argument de coût
  pour une banque, pas une faiblesse.

### Décision 3 — Le calendrier réel

Le programme officiel place Fintech Academia, avec les pitchs étudiants, le 25 novembre. Vos
dates sont les 25 et 26. Il faut savoir quand a lieu le pitch final : la roadmap ci-dessous
suppose un pitch le 26 après-midi. Si le pitch est le 25, le jour 2 disparaît et tout ce qui
est marqué « jour 2 » se coupe.

---

## Les quatre rôles

| Rôle | Responsabilité | Profil conseillé |
|---|---|---|
| **Données** | Jeux de données, injection des scénarios, calcul des signaux | À l'aise avec pandas |
| **Modèle** | XGBoost, évaluation, mesure CPU contre GPU, GNN | Le plus avancé en machine learning |
| **Service** | Environnements, API FastAPI, flux simulé, kit hors ligne | Le plus à l'aise en développement et en système |
| **Démo** | Écran Streamlit, pitch, sources, relation avec les organisateurs | Bon à l'oral, soigneux sur l'affichage |

Chaque rôle a un binôme de secours, pour qu'une absence ne bloque rien : Données avec Modèle,
Service avec Démo.

Pour la montée en compétences : les débutants prennent Données et Démo en préparation, et
chaque tâche se termine par dix minutes d'explication au reste de l'équipe.

---

## Préparation : du 20 au 24 novembre

Objectif : arriver le 25 avec une chaîne complète qui tourne déjà sans GPU, de la donnée à
l'écran de démo. Sur place, il ne reste qu'à passer sur GPU, mesurer et répéter.

| # | Tâche | Durée | Qui | Doit être prêt avant | Terminé quand |
|---|---|---|---|---|---|
| P1 | Envoyer aux organisateurs les sept questions de `docs/ressources.md`, partie 6 | 30 min | Démo | Rien | Message envoyé le 20 au matin, réponses notées dans le dépôt |
| P2 | Dépôt Git partagé, Python 3.12 isolé, comptes Kaggle | 2 h | Service, puis tous | Rien | Les quatre lancent le script de téléchargement avec succès |
| P3 | Exploration de PaySim et de MoMTSim-TZ, choix du jeu principal | 3 h | Données | P2 | Une page de constats et la décision 1 tranchée |
| P4 | Générateur de scénarios : les cinq scénarios et les contre-exemples, paramètres tirés au hasard | 6 h | Données et Service | P3 | Un fichier de transactions injectées, relu à la main sur dix cas |
| P5 | Calcul des signaux du compte destinataire, sur le passé uniquement | 6 h | Données et Modèle | P4 | Un tableau de signaux, avec un test qui prouve qu'aucun signal ne lit le futur ni les soldes |
| P6 | XGBoost sur CPU avec découpage temporel ; mesures : précision moyenne, rappel à 1 % de fausses alertes | 4 h | Modèle | P5 | Un modèle sauvegardé en `.ubj` et un tableau de résultats, scénario caché compris |
| P7 | Répétition sur Kaggle avec un T4 : même code avec `device="cuda"` et cuDF, premier chronométrage | 3 h | Modèle | P6 | Temps CPU et GPU notés, jeu de versions A ou B validé pour de vrai |
| P8 | API FastAPI : une route de score qui renvoie score, décision et raison en français | 5 h | Service | P6 pour le vrai modèle ; démarre avant avec un faux score | Réponse en moins de 200 ms sur l'ordinateur, mesurée sur 1 000 appels |
| P9 | Démo Streamlit : flux rejoué, bouton « lancer l'arnaque », alerte, comparaison avec et sans Sentinelle | 6 h | Démo | P8 avec faux score | Le scénario 1 se joue de bout en bout sans toucher au code |
| P10 | Kit hors ligne sur disque externe : données, paquets pip des jeux A et B, images Docker | 3 h | Service | P7 | Installation réussie sur une machine sans Internet |
| P11 | Trame du pitch, avec uniquement des chiffres sourcés | 4 h | Démo | `docs/contexte-pispi.md` | Dix diapositives en brouillon, relues par un autre membre |
| P12 | Apprentissage de PyTorch Geometric sur l'exemple Elliptic | 3 h | Modèle | P6 terminé au plus tard le 22 | GraphSAGE entraîné sur Elliptic dans Kaggle |
| P13 | Répétition générale et vidéo de secours de la démo | 2 h | Tous | P8, P9 | Démo jouée deux fois de suite sans erreur, vidéo enregistrée |

Total : environ 48 heures de travail, soit une douzaine d'heures par personne sur cinq jours.

Jalon de mi-parcours, dimanche 22 au soir : P1 à P6 terminés. Sinon, P12 est abandonné
tout de suite.

---

## Jour 1 — mercredi 25 novembre

Objectif : la version 1 tourne sur les GPU fournis et la démo est gelée le soir.

| # | Tâche | Durée | Qui | Doit être prêt avant | Terminé quand |
|---|---|---|---|---|---|
| J1-1 | Lire `nvidia-smi`, choisir le jeu A ou B, installer depuis le kit hors ligne | 1 h 30 | Service et Modèle | P10 | cuDF, XGBoost et PyTorch voient le GPU |
| J1-2 | Copier les données et recalculer les signaux avec cuDF sur le volume grossi | 2 h | Données | J1-1, P5 | Mêmes résultats qu'en pandas sur un échantillon, temps noté |
| J1-3 | Entraîner XGBoost sur GPU, chronométrer CPU contre GPU | 2 h | Modèle | J1-2 | Tableau des temps et des scores, modèle sauvegardé |
| J1-4 | Régler les deux seuils : alerte et blocage | 1 h | Modèle et Démo | J1-3 | Seuils fixés, avec le nombre de fausses alertes pour 1 000 transferts |
| J1-5 | Brancher le modèle final dans l'API, raisons calculées avec `pred_contribs` | 2 h | Service | J1-3 | Les cinq scénarios renvoient une raison juste et lisible |
| J1-6 | Démo de bout en bout avec le vrai modèle | 2 h | Démo et Service | J1-5 | Scénario 1 joué trois fois sans erreur, avec et sans Sentinelle |
| J1-7 | Intégrer les mesures au pitch | 1 h | Démo | J1-3, J1-4 | Diapositives de résultats à jour |
| J1-8 | Gel de la version 1 et décision sur le GNN | 30 min | Tous | J1-6 | Version étiquetée dans Git ; GNN lancé ou abandonné |

Règle du soir : le GNN n'est lancé au jour 2 que si J1-6 est terminé. Sinon, le jour 2 sert à
finir la version 1.

---

## Jour 2 — jeudi 26 novembre

Objectif : un pitch répété. Tout ce qui est nouveau s'arrête à midi.

| # | Tâche | Durée | Qui | Doit être prêt avant | Terminé quand |
|---|---|---|---|---|---|
| J2-1 | Version 2 : GraphSAGE sur le graphe des comptes, représentations données à XGBoost | 3 h, pas une minute de plus | Modèle et Données | J1-8, P12 | Comparaison chiffrée avec la version 1 sur le scénario de la chaîne de mules |
| J2-2 | Finitions de la démo : textes des alertes, lisibilité à distance | 2 h | Démo | J1-6 | Un membre extérieur à la démo comprend l'écran sans explication |
| J2-3 | Solidité : démo jouable sans réseau, nouvelle vidéo de secours | 1 h 30 | Service | J1-6 | Démo jouée Wi-Fi coupé ; vidéo sur deux ordinateurs |
| J2-4 | Gel complet à midi | — | Tous | — | Plus aucun changement de code ensuite |
| J2-5 | Deux répétitions chronométrées du pitch, questions du jury préparées | 2 h | Tous | J2-4 | Pitch dans le temps imparti, deux fois |
| J2-6 | Pitch et démo | — | Tous | J2-5 | — |

Si la version 2 ne bat pas la version 1 à midi, elle est présentée comme une piste, avec son
résultat réel. L'article de référence d'IBM rapporte lui aussi des signaux de graphe avec
XGBoost devant le meilleur GNN.

---

## Ce qu'on coupe, dans l'ordre

1. **La version 2 (GNN).** C'est la plus risquée et la moins nécessaire à la démo.
2. **Les scénarios 5 puis 4.** Les scénarios 1 à 3 suffisent à porter le message.
3. **Le contrôle sur IBM AML.** On garde seulement le scénario caché comme preuve.
4. **cuDF pour la préparation.** On garde pandas, et le GPU ne sert qu'à XGBoost.
5. **Le flux en direct.** On rejoue un flux enregistré.
6. **Les raisons calculées par le modèle.** On les remplace par des phrases tirées des deux
   signaux les plus élevés.

Ce qu'on ne coupe jamais : le scénario 1 joué de bout en bout, la comparaison avec et sans
Sentinelle, la diapositive des mesures avec ses limites, et la vidéo de secours.

---

## Risques qui menacent la démo

| Risque | Gravité | Parade |
|---|---|---|
| Le modèle n'est évalué que sur nos propres scénarios | Élevée | Décision 1 : scénario caché, contre-exemples, contrôle sur IBM AML |
| Le GPU paraît inutile | Élevée | Décision 2 : mesure CPU contre GPU sur un volume grossi |
| Environnement GPU inconnu, installation sur un réseau lent | Élevée | P1 pour savoir, P10 pour ne pas dépendre du réseau, P7 pour avoir déjà installé une fois |
| Le pitch a lieu le 25 et non le 26 | Élevée | P1 dès le 20 au matin ; la préparation vise déjà une démo complète le 24 |
| Le code écrit avant le hackathon est interdit par le règlement | Moyenne | P1. Si c'est interdit, la préparation devient des notebooks d'essai et des plans, et le jour 1 est réécrit |
| Résultats trop beaux à cause d'une fuite de données | Moyenne | Test de P5 : ni soldes, ni futur. Se méfier de tout score au-dessus de 0,99 |
| Fausses alertes sur les tontines et les commerçants | Moyenne | Contre-exemples injectés, taux de fausses alertes affiché dans le pitch |
| Panne en direct | Moyenne | Démo jouable sans réseau, vidéo de secours sur deux ordinateurs |
| Une affirmation fausse devant un juré de la BCEAO ou d'une fintech | Moyenne | Liste « à ne pas dire » de `docs/contexte-pispi.md` |
| Promettre l'usage du blueprint NVIDIA | Faible | Le citer comme inspiration : il demande un GPU de 32 Go et une clé NGC |
| Présenter Payfonte comme point de passage des arnaques entre particuliers | Faible | Parler du contrôle du bénéficiaire avant un décaissement |
