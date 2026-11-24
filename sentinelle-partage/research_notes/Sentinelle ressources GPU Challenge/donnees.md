# Jeux de données publics pour la fraude mobile money / détection de réseaux de mules

Notes de recherche, état au 2026-11-19. Convention utilisée partout :
- **[VÉRIFIÉ]** = j'ai ouvert la page / l'API / le fichier moi-même aujourd'hui (la source liée est celle que j'ai lue).
- **[SECONDAIRE]** = chiffre repris d'une source tierce (README GitHub d'un tiers, etc.), non recalculé.
- **[NON VÉRIFIÉ]** = pas pu confirmer ; à traiter comme hypothèse.

Méthode : les pages HTML Kaggle sont peu lisibles par un robot, mais l'API publique Kaggle (`/api/v1/datasets/view|list|download/...`) répond **sans authentification** ; c'est elle qui fournit tailles, licences et listes de fichiers ci-dessous. Aucun gros jeu de données n'a été téléchargé : seulement des métadonnées, des requêtes HTTP `Range` de quelques centaines d'octets (en-têtes CSV) et un fichier `HI-Small_Patterns.txt` de 324 Ko.

---

## 1. PaySim (Kaggle `ealaxi/paysim1`, simulateur GitHub, article EMSS 2016)

### Takeaway
PaySim est le seul jeu « mobile money africain » massivement utilisé (6 362 620 lignes, 11 colonnes, 0,129 % de fraude, CC BY-SA 4.0, 471 Mo), mais il est mal adapté à un scoring **du compte destinataire** : presque chaque émetteur n'apparaît qu'une fois (6 353 307 `nameOrig` uniques), les destinataires n'ont en moyenne que ~2,3 transactions, et l'auteur lui-même interdit d'utiliser les 4 colonnes de solde. À utiliser comme base tabulaire/XGBoost et démonstration, pas comme graphe de mules crédible.

### Cited Findings

**Identité, taille, licence, accès**
- [VÉRIFIÉ] Titre « Synthetic Financial Datasets For Fraud Detection », auteur Edgar Lopez-Rojas, licence **CC BY-SA 4.0**, `totalBytes` = 493 534 783 octets (≈ 471 Mio), version 2 du 2017-04-03, 166 105 téléchargements, 380 notebooks — [API Kaggle view](https://www.kaggle.com/api/v1/datasets/view/ealaxi/paysim1) (page humaine : [kaggle.com/datasets/ealaxi/paysim1](https://www.kaggle.com/datasets/ealaxi/paysim1))
- [VÉRIFIÉ] Un seul fichier : `PS_20174392719_1491204439457_log.csv`, 493 534 783 octets — [API Kaggle list](https://www.kaggle.com/api/v1/datasets/list/ealaxi/paysim1)
- [VÉRIFIÉ] L'archive servie au téléchargement est un zip de **186 385 561 octets** (en-tête `content-range: bytes 0-99/186385561`, `content-type: application/zip`) — [endpoint download](https://www.kaggle.com/api/v1/datasets/download/ealaxi/paysim1)
- [VÉRIFIÉ] **6 362 620 lignes, 11 colonnes** : compté par le serveur de datasets HuggingFace sur un miroir dont le fichier d'origine fait exactement 493 534 783 octets (même taille que le fichier Kaggle) — [datasets-server size, miroir theman10/paysim](https://datasets-server.huggingface.co/size?dataset=theman10/paysim)

**Schéma (description officielle de l'auteur)** — [API Kaggle view](https://www.kaggle.com/api/v1/datasets/view/ealaxi/paysim1)
- [VÉRIFIÉ] Ligne d'exemple : `1,PAYMENT,1060.31,C429214117,1089.0,28.69,M1591654462,0.0,0.0,0,0`
- [VÉRIFIÉ] `step` : « 1 step is 1 hour of time. Total steps 744 (30 days simulation) ».
- [VÉRIFIÉ] `type` : CASH-IN, CASH-OUT, DEBIT, PAYMENT, TRANSFER (dans le CSV : `CASH_IN`, `CASH_OUT`, avec underscore).
- [VÉRIFIÉ] `amount` : « amount of the transaction in local currency » (devise non nommée).
- [VÉRIFIÉ] `nameOrig`, `oldbalanceOrg`, `newbalanceOrig`, `nameDest`, `oldbalanceDest`, `newbalanceDest` ; pour les destinataires commençant par **M (Merchants)** : « there is not information » sur les soldes.
- [VÉRIFIÉ] `isFraud` : « transactions made by the fraudulent agents inside the simulation. […] the fraudulent behavior of the agents aims to profit by taking control or customers accounts and try to empty the funds by transferring to another account and then cashing out of the system ».
- [VÉRIFIÉ] `isFlaggedFraud` : règle métier, « an attempt to transfer more than 200.000 in a single transaction ».
- [VÉRIFIÉ] Attention au nom incohérent des colonnes : `oldbalanceOrg` (sans « i ») mais `newbalanceOrig`.

**Statistiques de colonnes lues sur la page Kaggle** — [page Kaggle via r.jina.ai](https://r.jina.ai/https://www.kaggle.com/datasets/ealaxi/paysim1)
- [VÉRIFIÉ] `step` va de 1 à **743** dans l'histogramme Kaggle (la description dit 744).
- [VÉRIFIÉ] `type` : CASH_OUT 35 %, PAYMENT 34 %, autres 31 % (1 973 625 lignes).
- [VÉRIFIÉ] `nameOrig` : **6 353 307 valeurs uniques** ; `nameDest` : **2 722 362 valeurs uniques**.
- [VÉRIFIÉ] `amount` max ≈ 92,4 M ; soldes destinataires jusqu'à ≈ 356 M.
- [VÉRIFIÉ] Deux premières lignes frauduleuses de l'aperçu : `TRANSFER 181.0 C1305486145 181.0 0.0 C553264065 0.0 0.0 1` puis `CASH_OUT 181.0 C840083671 181.0 0.0 C38997010 21182.0 0.0 1` : le compte qui encaisse (C840083671) n'est **pas** le destinataire du transfert (C553264065).

**Taux de fraude et répartition**
- [SECONDAIRE] 8 213 fraudes sur 6 362 620 = **0,129 %** ; fraude « exclusive to TRANSFER and CASH_OUT » — [README GitHub VishnujanNarayanan/fraud_detection](https://github.com/VishnujanNarayanan/fraud_detection)
- [SECONDAIRE] 4 097 fraudes en TRANSFER (taux 0,77 %) et 4 116 en CASH_OUT (0,18 %) ; zéro en CASH_IN, PAYMENT, DEBIT ; `isFlaggedFraud` = 1 sur **16 lignes seulement** — [README AnukratiR/aml-transaction-risk-dashboard](https://github.com/AnukratiR/aml-transaction-risk-dashboard) ; mêmes chiffres dans [README Vraj-Data-Scientist/real-time-fraud-alert-system](https://github.com/Vraj-Data-Scientist/real-time-fraud-alert-system)
- [SECONDAIRE] Les 16 lignes `isFlaggedFraud` sont toutes des fraudes, soit 0,19 % des 8 213 cas — [README VishnujanNarayanan/fraud_detection](https://github.com/VishnujanNarayanan/fraud_detection)
- [SECONDAIRE, un seul auteur, non recalculé] Parmi les destinataires de fraude, « the vast majority […] were utilized only once » ; seuls 44 comptes sont touchés 2 à 5 fois — [README AnukratiR/aml-transaction-risk-dashboard](https://github.com/AnukratiR/aml-transaction-risk-dashboard)

**Piège n°1 : fuite par les colonnes de solde**
- [VÉRIFIÉ] Avertissement de l'auteur dans la description : « Transactions which are detected as fraud are cancelled, so for fraud detection these columns (oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest) must not be used. » — [API Kaggle view](https://www.kaggle.com/api/v1/datasets/view/ealaxi/paysim1)

**Origine des données réelles**
- [VÉRIFIÉ] « a sample of real transactions extracted from one month of financial logs from a mobile money service implemented in **an African country** », fournies par « a multinational company […] running in more than 14 countries » ; le pays n'est **pas nommé**. Le jeu Kaggle est « scaled down 1/4 of the original dataset ». — [API Kaggle view](https://www.kaggle.com/api/v1/datasets/view/ealaxi/paysim1)
- [VÉRIFIÉ] L'article EMSS 2016 dit que le simulateur doit reproduire « a batch of real transactional Data provided by **Ericsson** » et que les montants sont « in a currency that we can not disclose ». La Tanzanie n'est citée que comme exemple d'adoption du mobile money dans l'introduction, pas comme source des données. — [PDF EMSS 2016, msc-les.org](https://www.msc-les.org/proceedings/emss/2016/EMSS2016_249.pdf)
- [VÉRIFIÉ] Article : jeu de référence « PS41840 », « around 23 million records », 744 pas ; tableau 1 : CASH-IN 4 496 947, CASH-OUT 9 014 407, TRANSFER 2 030 969, PAYMENT 8 955 794, DEBIT 139 935. Cet article de 2016 décrit la génération des transactions normales ; il ne décrit pas le jeu Kaggle étiqueté de 2017. — [PDF EMSS 2016](https://www.msc-les.org/proceedings/emss/2016/EMSS2016_249.pdf)
- [VÉRIFIÉ] Référence à citer : E. A. Lopez-Rojas, A. Elmir, S. Axelsson, « PaySim: A financial mobile money simulator for fraud detection », 28th EMSS, Larnaca, 2016 ; thèse : http://urn.kb.se/resolve?urn=urn:nbn:se:bth-12932 — [README PaySim](https://github.com/EdgarLopezPhD/PaySim)

**Simulateur officiel** — [github.com/EdgarLopezPhD/PaySim](https://github.com/EdgarLopezPhD/PaySim)
- [VÉRIFIÉ] Licence **GPL-3.0**, 134 étoiles, dernier push 2021-05-30, dernier commit de code 2019-04-02, Java + Maven (`pom.xml`), basé sur MASON.
- [VÉRIFIÉ] `PaySim.properties` par défaut : `nbSteps=720`, `nbClients=20000`, `nbFraudsters=1000`, `nbMerchants=34749`, `nbBanks=5`, `fraudProbability=0.001`.
- [VÉRIFIÉ] Dans le code actuel (`Fraudster.java`, `Mule.java`), chaque fraude **crée un nouveau compte mule** (`new Mule(paysim.generateId(), …)`), y transfère le solde de la victime, puis la mule fait un `CASH_OUT` vers un marchand tiré au hasard. Une mule ne reçoit donc qu'une fois. Contribution 2019 de Camille Barneaud / Flaminem pour des cas de blanchiment (`paramFiles/typologies/DrugNetworkOne.graphml`).
- [VÉRIFIÉ] Le dépôt contient les fichiers de paramètres agrégés (`paramFiles/aggregatedTransactions.csv`, 104 Ko), pas de jeu de sortie.

### Inferences
- 6 362 620 transactions pour 6 353 307 émetteurs uniques : il n'y a **aucun historique émetteur** exploitable. Les features de vélocité côté émetteur sont impossibles sur ce jeu.
- 6 362 620 / 2 722 362 ≈ 2,3 transactions par destinataire en moyenne. Des features d'agrégat destinataire (nombre d'entrées, somme reçue, nombre d'émetteurs distincts dans une fenêtre) sont calculables, mais le signal « mule récurrente » est faible si les destinataires de fraude ne servent presque tous qu'une fois (chiffre secondaire). Un GNN n'aura presque rien à propager.
- Le code actuel du simulateur (mule neuve à chaque fraude, cash-out vers un marchand) ne correspond pas exactement au CSV Kaggle de 2017, où les CASH_OUT frauduleux vont vers des comptes `C…` : ne pas décrire le CSV à partir du code de 2019.
- Les soldes fuient l'étiquette parce que les fraudes « annulées » laissent des soldes incohérents ; un modèle qui les utilise obtient des scores quasi parfaits sans valeur. Pour un scoring temps réel honnête : n'utiliser que `step`, `type`, `amount` et des agrégats **passés** du destinataire, avec un découpage temporel sur `step`.
- `isFlaggedFraud` (16 lignes) est inutilisable comme feature ou comme baseline sérieuse ; au mieux un exemple de « règle métier qui ne voit rien ».
- Devise et pays étant masqués, PaySim ne peut pas être présenté comme « données d'Afrique de l'Ouest » ; seulement comme mobile money calibré sur un pays africain non divulgué.

### Gaps
- Je n'ai **pas recalculé** 8 213 / 4 097 / 4 116 / 16 : le serveur de requêtes HuggingFace renvoyait « the dataset index is loading » et la consigne interdisait de télécharger le CSV. Ces chiffres concordent entre trois README indépendants mais restent secondaires. À confirmer en 5 lignes de pandas après téléchargement.
- Distribution exacte du nombre de transactions par `nameDest` (hors marchands `M…`), et part des destinataires de fraude qui reçoivent aussi du trafic légitime : non mesurées. C'est la mesure à faire en premier pour décider si PaySim supporte des features destinataire.
- Affirmation classique « le `nameDest` d'un TRANSFER frauduleux n'apparaît jamais comme `nameOrig` d'un CASH_OUT » : illustrée par les deux lignes de l'aperçu, non vérifiée sur l'ensemble.
- Pays d'origine : non publié. Aucune source primaire ne le nomme.
- Un résultat de recherche non ouvert (l'API Zenodo n'a pas répondu) : « Do Graph-Derived Features Improve Fraud Detection? An Empirical Study on PaySim, Elliptic and IEEE-CIS », https://doi.org/10.5281/zenodo.17746238 — contenu non lu.

---

## 2. IBM AML-Data / « IBM Transactions for Anti Money Laundering (AML) » (AMLworld)

### Takeaway
C'est le meilleur jeu public pour la partie graphe : 6 jeux synthétiques indépendants (HI/LI × Small/Medium/Large, de ~5 M à ~180 M transactions), étiquette par transaction, fichiers `*_Patterns.txt` listant les tentatives de blanchiment par motif (fan-in, fan-out, cycle, etc.), licence CDLA-Sharing-1.0. Mais c'est de la banque multi-devises (ACH, chèque, carte), pas du mobile money, et le taux de positifs est très bas (≈ 1/1000 à 1/2000).

### Cited Findings

**Dépôt GitHub** — [github.com/IBM/AML-Data](https://github.com/IBM/AML-Data)
- [VÉRIFIÉ] Le dépôt ne contient **que** `LICENSE` et `README.md` (aucune donnée). Dépôt sous Apache-2.0 ; « the actual data is released under the CDLA-Sharing-1.0 license ». Dernier push 2025-09-17, 108 étoiles.
- [VÉRIFIÉ] Le README renvoie vers Kaggle (« NEW AND IMPROVED DATA ON KAGGLE ») et vers l'ancien jeu sur Box (https://ibm.box.com/v/AML-Anti-Money-Laundering-Data, non ouvert).

**Jeu Kaggle** — [API Kaggle view](https://www.kaggle.com/api/v1/datasets/view/ealtman2019/ibm-transactions-for-anti-money-laundering-aml) (page humaine : [kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml))
- [VÉRIFIÉ] Auteur Erik Altman, licence « Community Data License Agreement - Sharing - Version 1.0 », **41 608 549 656 octets au total (≈ 41,6 Go)**, version 8 du 2025-07-08, 62 337 téléchargements.
- [VÉRIFIÉ] Tableau officiel de la description :

| | HI-Small | LI-Small | HI-Medium | LI-Medium | HI-Large | LI-Large |
|---|---|---|---|---|---|---|
| Période (2022) | 1-10 sept. | 1-10 sept. | 1-16 sept. | 1-16 sept. | 1 août - 5 nov. | 1 août - 5 nov. |
| Jours | 10 | 10 | 16 | 16 | 97 | 97 |
| Comptes bancaires | 515 K | 705 K | 2 077 K | 2 028 K | 2 116 K | 2 064 K |
| Transactions | 5 M | 7 M | 32 M | 31 M | 180 M | 176 M |
| Transactions de blanchiment | 5,1 K | 4,0 K | 35 K | 16 K | 223 K | 100 K |
| Taux (1 pour N) | 981 | 1 942 | 905 | 1 948 | 807 | 1 750 |

- [VÉRIFIÉ] Les six jeux sont indépendants (« the small datasets are not a subset of the medium datasets ») ; découpage chronologique recommandé 60 % / 20 % / 20 %.
- [VÉRIFIÉ] Piège signalé par l'auteur : il existe des transactions après la période indiquée et « those transactions are all laundering » (discussion Kaggle 427517, citée dans la description ; la discussion elle-même n'a pas été ouverte).
- [VÉRIFIÉ] « not all laundering in the data follows one of these 8 patterns ».
- [VÉRIFIÉ] Le générateur modélise placement, layering et intégration, plusieurs banques et devises ; IBM dit disposer de jeux bien plus grands sur demande.

**Fichiers et tailles** — [API Kaggle list](https://www.kaggle.com/api/v1/datasets/list/ealtman2019/ibm-transactions-for-anti-money-laundering-aml)
- [VÉRIFIÉ] 18 fichiers (la description n'en annonce que 12 ; des `*_accounts.csv` ont été ajoutés) :

| Fichier | Octets | ≈ |
|---|---|---|
| HI-Small_Trans.csv | 475 664 283 | 0,48 Go |
| LI-Small_Trans.csv | 650 422 357 | 0,65 Go |
| HI-Medium_Trans.csv | 3 031 783 420 | 3,03 Go |
| LI-Medium_Trans.csv | 2 976 436 978 | 2,98 Go |
| HI-Large_Trans.csv | 17 052 760 651 | 17,05 Go |
| LI-Large_Trans.csv | 16 742 513 790 | 16,74 Go |
| HI-Small_accounts.csv | 34 053 187 | 34 Mo |
| LI-Small_accounts.csv | 47 248 016 | 47 Mo |
| HI/LI-Medium_accounts.csv | 145 008 642 / 141 781 157 | ~0,14 Go |
| HI/LI-Large_accounts.csv | 147 691 860 / 144 349 585 | ~0,14 Go |
| HI-Small_Patterns.txt | 323 844 | 0,3 Mo |
| LI-Small_Patterns.txt | 99 156 | 0,1 Mo |
| HI/LI-Medium_Patterns.txt | 2 279 574 / 390 893 | |
| HI/LI-Large_Patterns.txt | 13 807 473 / 1 934 790 | |

**Schéma (lu directement dans les fichiers par requête Range anonyme)**
- [VÉRIFIÉ] En-tête de `HI-Small_Trans.csv` : `Timestamp,From Bank,Account,To Bank,Account,Amount Received,Receiving Currency,Amount Paid,Payment Currency,Payment Format,Is Laundering`. Exemple : `2022/09/01 00:20,010,8000EBD30,010,8000EBD30,3697.34,US Dollar,3697.34,US Dollar,Reinvestment,0` — [download HI-Small_Trans.csv](https://www.kaggle.com/api/v1/datasets/download/ealtman2019/ibm-transactions-for-anti-money-laundering-aml/HI-Small_Trans.csv)
- [VÉRIFIÉ] **Deux colonnes portent le même nom `Account`** (émetteur puis destinataire) : pandas renomme la seconde en `Account.1`. Valeurs de `Payment Format` observées : Reinvestment, Cheque, Credit Card, ACH. Beaucoup de lignes « Reinvestment » sont des auto-transferts (même compte source et destination).
- [VÉRIFIÉ] En-tête de `HI-Small_accounts.csv` : `Bank Name,Bank ID,Account Number,Entity ID,Entity Name` (ex. `Portugal Bank #4507,331579,80B779D80,80062E240,Sole Proprietorship #50438`) : permet de regrouper les comptes par entité — [download HI-Small_accounts.csv](https://www.kaggle.com/api/v1/datasets/download/ealtman2019/ibm-transactions-for-anti-money-laundering-aml/HI-Small_accounts.csv)
- [VÉRIFIÉ] Format de `HI-Small_Patterns.txt` : blocs `BEGIN LAUNDERING ATTEMPT - FAN-OUT:  Max 16-degree Fan-Out` … lignes de transactions au même format CSV … `END LAUNDERING ATTEMPT - FAN-OUT`. J'ai compté dans ce fichier **370 tentatives et 3 209 transactions** : BIPARTITE 49, CYCLE 54, FAN-IN 40, FAN-OUT 48, GATHER-SCATTER 51, RANDOM 41, SCATTER-GATHER 44, STACK 43 — [download HI-Small_Patterns.txt](https://www.kaggle.com/api/v1/datasets/download/ealtman2019/ibm-transactions-for-anti-money-laundering-aml/HI-Small_Patterns.txt)

**Article NeurIPS 2023** — [arXiv 2306.16424v3](https://arxiv.org/pdf/2306.16424)
- [VÉRIFIÉ] Altman, Blanuša, von Niederhäusern, Egressy, Anghel, Atasu, « Realistic Synthetic Financial Transactions for Anti-Money Laundering Models » ; le générateur s'appelle **AMLworld**.
- [VÉRIFIÉ] Les 8 motifs viennent d'AMLSim (Suzumura & Kanezashi) : fan-out, fan-in, gather-scatter, scatter-gather, simple cycle, random, bipartite, stack.
- [VÉRIFIÉ] Tableau 1 de l'article : AMLSim = 1,32 M transactions, taux 1/762, transferts seulement ; AMLworld = 180 M, taux 1/807 et 1/1 750, multi-banques, multi-devises.
- [VÉRIFIÉ] Tableau 2, F1 de la classe minoritaire (%) : GFP + XGBoost = 63,23 (HI-Small), 27,30 (LI-Small), 65,70 (HI-Medium), 28,16 (LI-Medium), 42,68 (HI-Large), 24,23 (LI-Large) ; PNA = 56,77 / 16,45 / 59,71 / 27,73 ; GIN = 28,70 / 7,90 / 42,30 / 3,86 ; pas de résultat GNN sur Large.
- [VÉRIFIÉ] Les IDs de comptes source et destination ne sont pas utilisés comme features dans leurs expériences ; les GBT utilisent Graph Feature Preprocessor (GFP) ; versions LightGBM 3.1.1 et XGBoost 1.7.6.
- [VÉRIFIÉ] **Contradiction** : le tableau 4 de l'article donne 3,6 K transactions de blanchiment pour HI-Small, la page Kaggle 5,1 K. Seul 5,1 K est cohérent avec 5 M × 1/981. — [arXiv 2306.16424v3](https://arxiv.org/pdf/2306.16424) ; contredit par [API Kaggle view](https://www.kaggle.com/api/v1/datasets/view/ealtman2019/ibm-transactions-for-anti-money-laundering-aml)
- [VÉRIFIÉ] Code de référence GNN : [github.com/IBM/Multi-GNN](https://github.com/IBM/Multi-GNN), Apache-2.0, dernier push 2025-09-18.

### Inferences
- **HI-Small** (0,48 Go, ~5 M transactions, ~515 K comptes, ~0,1 % de positifs) est le seul format réaliste pour un hackathon : il tient en mémoire GPU, et il existe des scores publiés à battre (XGBoost + features de graphe : F1 ≈ 63 %).
- Le résultat le plus utile pour le projet : sur ce jeu, XGBoost avec features de graphe fait jeu égal ou mieux que les GNN. Cela justifie l'architecture « XGBoost d'abord, GNN optionnel ».
- Les fichiers `Patterns` ne couvrent qu'une partie des positifs (3 209 transactions listées dans HI-Small contre ~5,1 K positifs annoncés) : ils servent à étiqueter le **type** de motif et à illustrer une démo (fan-in = collecte vers une mule), pas à remplacer la colonne `Is Laundering`.
- Pour un score « compte destinataire », il faut agréger soi-même : un compte est positif s'il reçoit au moins une transaction `Is Laundering=1` dans la fenêtre. L'étiquette native est par transaction, pas par compte.
- La clé de compte doit être `(Bank, Account)` ; les auto-transferts « Reinvestment » sont à filtrer avant de construire le graphe.
- CDLA-Sharing-1.0 est une licence de partage à l'identique pour les **données** : redistribuer une version modifiée du jeu impose la même licence ; les modèles entraînés ne sont pas visés par cette obligation (lecture de la licence à confirmer par l'équipe si publication).
- Écart de domaine : virements bancaires en USD/EUR/Yuan avec ACH et chèques. Aucun agent de cash-in/cash-out, aucun montant en XOF.

### Gaps
- Nombres de lignes exacts (les sources officielles donnent 5 M, 7 M, etc., arrondis). Le chiffre souvent cité de 5 078 345 lignes pour HI-Small n'a pas été vérifié.
- Texte de la discussion Kaggle 427517 (comment traiter les transactions hors période) : non ouvert.
- Ancien jeu Box et sa documentation PDF : non ouverts.
- Je n'ai pas lu le texte intégral de la licence CDLA-Sharing-1.0.

---

## 3. IBM AMLSim

### Takeaway
AMLSim est un **simulateur** multi-agents (Python pour générer le graphe + Java/MASON pour simuler), sous Apache-2.0, à l'origine des 8 motifs de blanchiment. Il est pénible à faire tourner en 2026 (Java 8, Python 3.7, `networkx==1.11`) ; pour un hackathon, mieux vaut prendre les jeux IBM AML déjà générés que lancer le simulateur.

### Cited Findings
- [VÉRIFIÉ] Description : « multi-agent based simulator that generates synthetic banking transaction data together with a set of known money laundering patterns ». Licence **Apache-2.0**, 414 étoiles, dernier push 2025-09-17. — [github.com/IBM/AMLSim](https://github.com/IBM/AMLSim)
- [VÉRIFIÉ] Dépendances listées dans le README : Java 8 avec une quinzaine de jars à placer à la main dans `jars/` (MASON 20, Commons-Math 3.6.1, WebGraph 3.6.1, fastutil 8.2.3, MySQL Connector 5.1, JUnit5, Mockito…) ; Python 3.7 avec `networkx==1.11` (« We do not support version 2.* »), `matplotlib==2.2.3` (« The latest version is not compatible »), `pygraphviz`, `powerlaw`. Option Maven : seul le jar MASON reste à installer à la main. — [README AMLSim](https://github.com/IBM/AMLSim)
- [VÉRIFIÉ] Chaîne en 3 étapes : `python3 scripts/transaction_graph_generator.py conf.json` → `sh scripts/build_AMLSim.sh` + `sh scripts/run_AMLSim.sh conf.json` → `python3 scripts/convert_logs.py conf.json`. Sorties : `accounts.csv`, `transactions.csv`, `cash_tx.csv`, `alert_accounts.csv`, `alert_transactions.csv`, `sar_accounts.csv`. Paramètres d'exemple dans `paramFiles/1K`, `total_steps: 720`. — [README AMLSim](https://github.com/IBM/AMLSim)
- [VÉRIFIÉ] Le README prévient que le wiki est « still under construction » et que seule la branche `master` est à utiliser. — [README AMLSim](https://github.com/IBM/AMLSim)
- [VÉRIFIÉ] Jeux d'exemple annoncés sur le wiki, hébergés sur **Dropbox** : 100 comptes/10 K transactions, 1 K/100 K, 10 K/1 M, 100 K/10 M, 1 M/100 M ; dossier `banks` versions v1.1 à v2.1. Exemple v2.1 `bank_mixed` : 20 K comptes dont **753 comptes SAR**, 885 744 transactions dont 807 SAR (20 cycles, 30 scatter-gather, 50 gather-scatter). Des CSV de features de graphe par compte sont fournis (`in_count`, `in_amount`, PageRank, proportion de SAR dans l'egonet à 1 et 2 sauts, features de cycles). — [wiki Download-Example-Data-Set](https://github.com/IBM/AMLSim/wiki/Download-Example-Data-Set)
- [VÉRIFIÉ] Avertissement du wiki : « all the generated data do not reflect real data ». — [wiki Download-Example-Data-Set](https://github.com/IBM/AMLSim/wiki/Download-Example-Data-Set)
- [VÉRIFIÉ] Articles à citer : EvolveGCN (arXiv 1902.10191) et « Scalable Graph Learning for Anti-Money Laundering: A First Look » (arXiv 1812.00076). — [README AMLSim](https://github.com/IBM/AMLSim)

### Inferences
- AMLSim a une étiquette **au niveau du compte** (comptes SAR), ce qui colle mieux à un scoring de compte destinataire que l'étiquette par transaction d'AMLworld ; mais les jeux d'exemple sont petits et uniquement des transferts.
- Les versions épinglées (Python 3.7, networkx 1.11, matplotlib 2.2.3) ne s'installent pas proprement sur un Python récent : prévoir un conteneur dédié, donc plusieurs heures de mise en route. Mauvais rapport coût/bénéfice sur 24-48 h.
- La liste de features de graphe du wiki (degré entrant/sortant, montants, PageRank, egonet) est une bonne check-list de features destinataire pour XGBoost.

### Gaps
- Le lien Dropbox n'a pas été ouvert : je ne sais pas si les jeux d'exemple sont encore téléchargeables ni sous quelle licence précise (le dépôt est Apache-2.0, rien n'est dit pour les données).
- Je n'ai pas essayé d'exécuter AMLSim ; la difficulté est déduite du README.

---

## 4. Autres jeux pertinents (mobile money, mules, contexte africain)

### Takeaway
Deux jeux mobile money africains existent en accès direct sans compte et sous CC BY 4.0 : le jeu MoMTSim de Makerere (Ouganda, Mendeley Data, 1,72 M et 4,23 M lignes) et **MoMTSim-TZ** (Tanzanie, Zenodo, 19,6 M lignes, 0,105 % de fraude, 12 typologies dont « Mule Accounts »). Aucun jeu public ne couvre l'Afrique de l'Ouest / l'UEMOA ; les autres candidats sont soit hors domaine (bitcoin, carte bancaire, ouverture de compte), soit sous licence non commerciale, soit non redistribuables (Zindi/Xente).

### Cited Findings

**MoMTSim-TZ (Tanzanie) — le plus proche du sujet**
- [VÉRIFIÉ] Zenodo, publié le 2026-09-27, version 1.0, **CC BY 4.0**, accès ouvert ; auteurs Ndegese, Sinde, Mdegela (NM-AIST, Arusha). — [API Zenodo record 22997330](https://zenodo.org/api/records/22997330) (DOI concept : https://doi.org/10.5281/zenodo.22997329)
- [VÉRIFIÉ] **19 614 235 transactions**, 720 pas horaires (30 jours), 20 fichiers CSV chronologiques, **20 colonnes**, 3,45 Go décompressés, devise TZS ; **20 679 fraudes (0,1054 %)** ; 12 typologies : Social Engineering, SIM-Swap, Agent Collusion, Account Takeover, **Mule Accounts**, Phishing, Identity Theft, Reversal Fraud, OTC Direct Deposit, Merchant Fraud, System Lag Exploit, Internal Malicious Access. — [README Zenodo](https://zenodo.org/api/records/22997330/files/README.md/content)
- [VÉRIFIÉ] 4 archives zip de 329 169 275, 333 944 133, 334 707 838 et 309 714 990 octets (≈ 1,31 Go au total). — [API Zenodo record 22997330](https://zenodo.org/api/records/22997330)
- [VÉRIFIÉ] Audit de fuite publié par les auteurs : exclure `newBalanceOrig`, `newBalanceDest`, `isSuccessful` (« no fraud cases are marked successful »), `fraudTypeCode`, et les valeurs de `action` qui nomment une typologie (ex. PHISHING, SIM_SWAP). Montant moyen : 18 348 TZS toutes lignes contre 1 305 846 TZS pour les fraudes. — [README Zenodo](https://zenodo.org/api/records/22997330/files/README.md/content)
- [VÉRIFIÉ] Limites déclarées : « not yet been validated against real transaction data from a Tanzanian mobile money operator ». Le README contient encore des champs à compléter (« list specific sources here », « confirm exact name » pour la colonne `isFraud`, article « add once published ») et annonce un `checksums.md5` absent de la liste des fichiers de l'API. — [README Zenodo](https://zenodo.org/api/records/22997330/files/README.md/content)

**MoMTSim (Makerere, Ouganda)**
- [VÉRIFIÉ] Mendeley Data, v2 du 2024-10-29, DOI 10.17632/zhj366m53p.2, **CC BY 4.0**, deux CSV : `MoMTSim_20240722202413_1000_dataset.csv` (349 Mo) et `synthetic_mobile_money_transaction_dataset.csv` (149 Mo) ; zip « Download All 184 MB ». — [Mendeley Data](https://data.mendeley.com/datasets/zhj366m53p/2)
- [VÉRIFIÉ] En-tête lu dans le fichier de 149 Mo : `step,transactionType,amount,initiator,oldBalInitiator,newBalInitiator,recipient,oldBalRecipient,newBalRecipient,isFraud` ; première ligne `0,TRANSFER,19824.96,4537027967639631,187712.18,167887.22,4875702729424478,8.31,19833.27,1`. — [fichier Mendeley](https://data.mendeley.com/public-files/datasets/zhj366m53p/files/57c2ed32-a9b6-4af8-9510-9b064625d5d7/file_downloaded)
- [VÉRIFIÉ] Article de données (Data in Brief, 2025) : version 1 = **1 720 181 lignes, 10,20 % de fraude** (175 518) ; version 2 = **4 225 958 lignes, 52,84 % de fraude** (2 233 118) ; 720 pas d'une heure ; types deposit, withdrawal, transfer, payment, debit ; scénarios : prise de contrôle de compte (SIM swap, identifiants perdus), fraude au remboursement, faux identifiants ; montants en « virtual units ». Limite déclarée : le jeu « has not been evaluated for its utility in training or testing machine learning models ». — [PMC12036017](https://pmc.ncbi.nlm.nih.gov/articles/PMC12036017/)
- [VÉRIFIÉ] Copie Kaggle `denishazamuke/synthetic-mobile-money-transaction-dataset` : un seul fichier de 366 397 921 octets, licence affichée **CC BY-SA 3.0** (différente de Mendeley). — [API Kaggle view](https://www.kaggle.com/api/v1/datasets/view/denishazamuke/synthetic-mobile-money-transaction-dataset)
- [VÉRIFIÉ] Simulateur : [github.com/aiinfinancegroup/MoMTSim](https://github.com/aiinfinancegroup/MoMTSim), GPL-3.0, JDK 11 + Maven, dernier push 2024-08-20, 1 étoile ; calibré sur « a sample real mobile money transactions data from one of our stakeholders in the region » (Afrique subsaharienne). Article : IEEE Access 2024, DOI 10.1109/ACCESS.2024.3439012 (non ouvert).

**Xente Fraud Detection Challenge (Zindi, Ouganda) — données réelles mais verrouillées**
- [VÉRIFIÉ] Xente = application e-commerce et services financiers, « 10,000+ customers in Uganda » ; ~140 000 transactions du 15 nov. 2018 au 15 mars 2019 ; entraînement du 15 nov. 2018 au 13 fév. 2019 ; compétition close le 22 sept. 2019. — [Zindi data](https://zindi.world/competitions/xente-fraud-detection-challenge/data)
- [VÉRIFIÉ] Règles : « The data used in this competition is the sole property of Zindi and the competition host. You may not transmit, duplicate, publish, redistribute […] (this includes uploading the data to any public site such as Kaggle or GitHub) ». — [Zindi règles](https://zindi.world/competitions/xente-fraud-detection-challenge)
- [VÉRIFIÉ] Colonnes (fichier de définitions présent dans un miroir GitHub tiers) : TransactionId, BatchId, AccountId, SubscriptionId, CustomerId, CurrencyCode, CountryCode, ProviderId, ProductId, ProductCategory, ChannelId, Amount, Value, TransactionStartTime, PricingStrategy, FraudResult. Ce miroir contient `training.csv` (17 Mo) sans licence. — [github.com/Paulvinc/Xente-Fraud-Detection](https://github.com/Paulvinc/Xente-Fraud-Detection)
- [SECONDAIRE] ~96 000 transactions d'entraînement, ~0,2 % de fraude. — [Kipu Quantum Hub](https://hub.kipu-quantum.com/marketplace/use-cases/9a61aa06-fb8e-4a81-b4eb-e9a54b3e2942)

**SAML-D**
- [VÉRIFIÉ] Kaggle `berkanoztas/synthetic-transaction-monitoring-dataset-aml` : un fichier `SAML-D.csv` de 996 168 850 octets, **9 504 852 transactions, 0,1039 % suspectes**, 12 features, 28 typologies (11 normales, 17 suspectes), 15 structures de graphe ; colonnes : date/heure, comptes émetteur et receveur, montant, type de paiement, localisation des banques, devises, `Is Suspicious`, `Type`. Licence **CC BY-NC-SA 4.0** (non commercial). Article : Oztas et al., IEEE ICEBE 2023. — [API Kaggle view](https://www.kaggle.com/api/v1/datasets/view/berkanoztas/synthetic-transaction-monitoring-dataset-aml)

**Elliptic et Elliptic++ (bitcoin)**
- [VÉRIFIÉ] Elliptic : 203 769 nœuds (transactions), 234 355 arêtes, 4 545 illicites (2 %), 42 019 licites, reste inconnu ; 166 features anonymisées ; 49 pas de temps ; 697 459 499 octets ; licence **CC BY-NC-ND 4.0**. — [API Kaggle view](https://www.kaggle.com/api/v1/datasets/view/ellipticco/elliptic-data-set)
- [VÉRIFIÉ] Elliptic++ : ajoute 822 942 adresses de portefeuilles dont 14 266 illicites, 251 088 licites, 557 588 inconnues ; 56 features par acteur ; 2 868 964 arêtes adresse-adresse. Données sur **Google Drive** ; le dépôt GitHub n'a **pas de licence déclarée**. — [github.com/git-disl/EllipticPlusPlus](https://github.com/git-disl/EllipticPlusPlus)

**BAF — Bank Account Fraud (NeurIPS 2022, Feedzai)**
- [VÉRIFIÉ] 6 CSV (`Base.csv` 213 Mo + 5 variantes), 1 million de lignes chacun, 30 features, colonne `month`, généré par CTGAN à partir de données réelles de fraude à l'**ouverture de compte** ; licence **CC BY-NC-SA 4.0** ; 1,36 Go. — [API Kaggle view](https://www.kaggle.com/api/v1/datasets/view/sgpjesus/bank-account-fraud-dataset-neurips-2022)
- [SECONDAIRE] `Base.csv` : 11 029 fraudes, soit 1,1029 %. — [rodinKaradeniz/sentinel, dataset_version.md](https://github.com/rodinKaradeniz/sentinel/blob/main/reports/dataset_version.md)

**TabFormer / IBM Credit Card Transactions**
- [VÉRIFIÉ] Kaggle `ealtman2019/credit-card-transactions` : « more than 20 million transactions », 2 000 consommateurs synthétiques américains, `credit_card_transactions-ibm_v2.csv` de 2 350 744 057 octets, plus `sd254_users.csv` et `sd254_cards.csv` ; licence Apache 2.0 (texte dans la description). — [API Kaggle view](https://www.kaggle.com/api/v1/datasets/view/ealtman2019/credit-card-transactions)
- [VÉRIFIÉ] Dépôt [github.com/IBM/TabFormer](https://github.com/IBM/TabFormer) (Apache-2.0) : « 24M records with 12 fields », données via git-lfs (`data/credit_card/transactions.tgz`) ou lien Box direct https://ibm.box.com/v/tabformer-data (non ouvert).

**Sparkov (carte bancaire simulée)**
- [VÉRIFIÉ] Kaggle `kartik2112/fraud-detection` : `fraudTrain.csv` (351 Mo) et `fraudTest.csv` (150 Mo), 1 000 clients, 800 marchands, du 1er janv. 2019 au 31 déc. 2020, licence **CC0**. Générateur : [namebrandon/Sparkov_Data_Generation](https://github.com/namebrandon/Sparkov_Data_Generation), MIT. — [API Kaggle view](https://www.kaggle.com/api/v1/datasets/view/kartik2112/fraud-detection)

**HuggingFace**
- [VÉRIFIÉ] Miroirs PaySim non restreints : `theman10/paysim` (un `paysim.csv`, étiqueté MIT alors que l'original est CC BY-SA 4.0), `flwrlabs/fed-fraud-paysim-banks` (Flower Labs, parquet, 5 726 358 train + 636 262 test, colonne `BankID` ajoutée, étiqueté CC BY 4.0), `LordNR/AMLGraphX-Paysim` (CC BY-SA 4.0). — [API HF search paysim](https://huggingface.co/api/datasets?search=paysim&sort=downloads&direction=-1&limit=6) ; [carte flwrlabs](https://huggingface.co/datasets/flwrlabs/fed-fraud-paysim-banks)
- [VÉRIFIÉ] Miroirs IBM AML : `OsamaMIT/IBM-AML-HI-Small` (contient `HI-Small_Trans.csv`, `HI-Small_accounts.csv`, `HI-Small_Patterns.txt`, étiqueté cdla-sharing-1.0), `OsamaMIT/IBM-AML-HI`, `eexzzm/IBM-Transactions-for-Anti-Money-Laundering-HI-Small-Trans`. — [API HF search IBM AML](https://huggingface.co/api/datasets?search=IBM%20AML&sort=downloads&direction=-1&limit=6)
- [VÉRIFIÉ] `electricsheepafrica/africa-mobile-money-fraud-dataset` : non restreint, 64 téléchargements, carte générée automatiquement ; « Rows: 10,000 (balanced 50/50) » ; licence incohérente (`other` dans les métadonnées, « mit » dans le texte) ; la carte dit elle-même que schéma et sources sont à vérifier. — [README HF](https://huggingface.co/datasets/electricsheepafrica/africa-mobile-money-fraud-dataset/raw/main/README.md)

### Inferences
- **Classement d'utilité pour le projet** (score du compte destinataire, virements instantanés, XGBoost + GNN optionnel) :
  1. IBM AML HI-Small : graphe riche, motifs étiquetés, scores publiés. Meilleur support pour les features de réseau et le GNN.
  2. MoMTSim-TZ : seul jeu mobile money africain avec un taux de fraude réaliste (0,105 %) et une typologie « Mule Accounts ». Très récent, non relu par des pairs, documentation inachevée : prendre un seul zip (parts 1-5, 5 M lignes) et vérifier d'abord le schéma et la répétition des destinataires.
  3. PaySim : référence connue de tous les jurys, bon pour une baseline tabulaire, faible pour le graphe.
  4. MoMTSim Makerere : schéma quasi identique à PaySim avec contexte est-africain, mais taux de fraude de 10 % et 53 %, irréalistes ; utile surtout comme second jeu de test de robustesse.
- Les jeux carte bancaire (Sparkov, TabFormer) et BAF n'ont pas de compte destinataire au sens P2P (le destinataire est un marchand, ou il n'y a pas de transaction du tout dans BAF) : hors sujet pour le score destinataire.
- Elliptic est un graphe de transactions bitcoin à features anonymes et licence ND (pas de dérivés) : utile seulement comme banc d'essai GNN, pas pour une démo mobile money. Elliptic++ (niveau portefeuille) est conceptuellement plus proche d'un score de compte, mais sans licence claire.
- SAML-D et BAF sont en licence NC : acceptables pour un hackathon étudiant, à écarter si le projet doit devenir un produit.
- Xente est le seul jeu **réel** africain repéré, mais c'est de la fraude e-commerce sans graphe émetteur-destinataire, et sa redistribution est interdite : ne pas l'intégrer au dépôt du projet, ne pas s'appuyer sur le miroir GitHub.
- Aucun jeu ne contient de données UEMOA/XOF. Le discours honnête : « entraîné sur des simulations calibrées sur l'Afrique de l'Est et sur des données bancaires synthétiques ; à recalibrer sur des données opérateur ».
- Les étiquettes de licence des miroirs HuggingFace ne font pas foi (ex. PaySim marqué MIT) : citer la licence de la source d'origine.

### Gaps
- MoMTSim-TZ : noms exacts des 20 colonnes non lus (le README n'en nomme que quelques-unes) ; nombre de comptes, répétition des destinataires et part de la typologie « Mule Accounts » inconnus. À inspecter après téléchargement d'une archive.
- MoMTSim Makerere : correspondance entre les deux fichiers (149 Mo / 349 Mo) et les versions 1,72 M / 4,23 M lignes non confirmée ; article IEEE Access non ouvert.
- Xente : nombre de lignes exact et taux de fraude non vérifiés à la source (Zindi exige un compte pour télécharger).
- Sparkov et TabFormer : nombre de lignes exact et taux de fraude non vérifiés. BAF : taux de fraude de source tierce uniquement.
- Elliptic++ : accessibilité actuelle du Google Drive non testée.
- Je n'ai trouvé **aucun** jeu public étiqueté « comptes mules » sur du mobile money réel, ni aucun jeu ouest-africain. Recherche faite sur Kaggle, Zenodo, HuggingFace et moteur de recherche ; absence de résultat, pas preuve d'inexistence.

---

## 5. Téléchargement : sans compte ou avec jeton Kaggle, commandes exactes

### Takeaway
Tout ce qui est utile se télécharge aujourd'hui **sans aucun compte** : Zenodo et Mendeley par URL directe, et, constat vérifié ce jour, l'endpoint public de Kaggle redirige vers une URL de stockage signée même sans authentification. La voie officielle Kaggle reste un jeton : variable `KAGGLE_API_TOKEN` ou fichier `~/.kaggle/access_token` (nouveau format), `~/.kaggle/kaggle.json` étant désormais « legacy ».

### Cited Findings

**Authentification Kaggle, état de la documentation officielle**
- [VÉRIFIÉ] Le dépôt `Kaggle/kaggle-api` a été renommé **`Kaggle/kaggle-cli`** (« Official Kaggle CLI »), Apache-2.0, dernier push 2026-11-18, dernière version **v2.2.5** du 2026-10-22. — [github.com/Kaggle/kaggle-cli](https://github.com/Kaggle/kaggle-cli)
- [VÉRIFIÉ] Quatre options documentées : (1) OAuth `kaggle auth login` ; (2) `export KAGGLE_API_TOKEN=xxxxxxxxxxxxxx` (« Copied from the settings UI ») ; (3) jeton dans le fichier `~/.kaggle/access_token` ; (4) « Legacy API credentials file » : bouton « Create Legacy API Key » qui génère `kaggle.json`, à placer dans `~/.kaggle/kaggle.json`. Le jeton se crée sur https://www.kaggle.com/settings/api, bouton « Generate New Token ». — [docs/README.md de kaggle-cli](https://github.com/Kaggle/kaggle-cli/blob/main/docs/README.md)
- [VÉRIFIÉ] `kagglehub` v1.0.3 (2026-10-21) : « Authenticating is **only** needed to access public resources requiring user consent or private resources. » Options : `kagglehub.login()`, `KAGGLE_API_TOKEN`, `~/.kaggle/access_token`, secret Colab `KAGGLE_API_TOKEN`, ou `kaggle.json` legacy. — [README kagglehub](https://github.com/Kaggle/kagglehub)
- [VÉRIFIÉ] Syntaxe CLI : `kaggle datasets download <DATASET> [-f FILE] [-p PATH] [--unzip] [-o] [-q]` ; avec `-f`, les gros fichiers arrivent dans un zip du même nom, que `--unzip` extrait. — [docs/datasets.md de kaggle-cli](https://github.com/Kaggle/kaggle-cli/blob/main/docs/datasets.md)
- [VÉRIFIÉ] Syntaxe kagglehub : `kagglehub.dataset_download('owner/dataset')`, `path='fichier.csv'` pour un seul fichier, `output_dir='./data'`, `force_download=True`. — [README kagglehub](https://github.com/Kaggle/kagglehub)

**Test d'accès anonyme réalisé le 2026-11-19 (sans cookie, sans jeton)**
- [VÉRIFIÉ] `GET https://www.kaggle.com/api/v1/datasets/download/ealaxi/paysim1` → HTTP 302 vers `storage.googleapis.com/kaggle-data-sets/1069/1940/bundle/archive.zip?...X-Goog-Expires=259200...` ; avec `-L` et `Range: 0-99` → HTTP 206, `application/zip`, taille totale 186 385 561. — [endpoint download PaySim](https://www.kaggle.com/api/v1/datasets/download/ealaxi/paysim1)
- [VÉRIFIÉ] Même comportement fichier par fichier pour IBM AML : `HI-Small_Patterns.txt` téléchargé en entier (HTTP 200, 323 844 octets, texte brut), en-têtes de `HI-Small_Trans.csv` et `HI-Small_accounts.csv` lus en clair (CSV non zippé). — [endpoint download IBM AML](https://www.kaggle.com/api/v1/datasets/download/ealtman2019/ibm-transactions-for-anti-money-laundering-aml/HI-Small_Patterns.txt)
- [VÉRIFIÉ] Mendeley : URL de fichier public → HTTP 206, `text/csv`, servi depuis S3 sans connexion. — [fichier Mendeley](https://data.mendeley.com/public-files/datasets/zhj366m53p/files/57c2ed32-a9b6-4af8-9510-9b064625d5d7/file_downloaded)
- [VÉRIFIÉ] Zenodo : `…/files/MoMTSim-TZ_raw_logs_part01-05.zip/content` → HTTP 206 sans connexion. — [API Zenodo record 22997330](https://zenodo.org/api/records/22997330)

**Tableau d'accès**

| Jeu | Sans compte ? | Source | Licence des données |
|---|---|---|---|
| PaySim | Oui (endpoint Kaggle anonyme testé ; miroirs HF) | Kaggle | CC BY-SA 4.0 |
| IBM AML (HI/LI) | Oui (endpoint Kaggle anonyme testé ; miroirs HF pour HI-Small) | Kaggle | CDLA-Sharing-1.0 |
| MoMTSim-TZ | Oui | Zenodo | CC BY 4.0 |
| MoMTSim Makerere | Oui | Mendeley Data | CC BY 4.0 |
| SAML-D, BAF, Elliptic, Sparkov, IBM Credit Card | Endpoint Kaggle anonyme probable, **non testé** pour ces jeux | Kaggle | NC-SA / NC-SA / NC-ND / CC0 / Apache-2.0 |
| AMLSim (exemples) | Non testé | Dropbox | non précisée |
| Elliptic++ | Non testé | Google Drive | aucune déclarée |
| Xente | **Non** : compte Zindi + acceptation des règles | Zindi | propriétaire, redistribution interdite |

**Commandes**

Sans compte (curl), testées en requête partielle seulement :
```bash
# PaySim (zip de 186 Mo, contient un CSV de 471 Mo)
curl -L -o paysim1.zip "https://www.kaggle.com/api/v1/datasets/download/ealaxi/paysim1"
unzip paysim1.zip

# IBM AML, HI-Small uniquement (0,48 Go + 34 Mo + 0,3 Mo), fichier par fichier
B="https://www.kaggle.com/api/v1/datasets/download/ealtman2019/ibm-transactions-for-anti-money-laundering-aml"
curl -L -o HI-Small_Trans.csv    "$B/HI-Small_Trans.csv"
curl -L -o HI-Small_accounts.csv "$B/HI-Small_accounts.csv"
curl -L -o HI-Small_Patterns.txt "$B/HI-Small_Patterns.txt"

# MoMTSim-TZ (Zenodo), première archive = parts 1 à 5, 329 Mo
curl -L -o MoMTSim-TZ_part01-05.zip \
  "https://zenodo.org/api/records/22997330/files/MoMTSim-TZ_raw_logs_part01-05.zip/content"
curl -L -o MoMTSim-TZ_README.md \
  "https://zenodo.org/api/records/22997330/files/README.md/content"

# MoMTSim Makerere (Mendeley), fichier de 149 Mo, ou tout le zip de 184 Mo
curl -L -o synthetic_mobile_money_transaction_dataset.csv \
  "https://data.mendeley.com/public-files/datasets/zhj366m53p/files/57c2ed32-a9b6-4af8-9510-9b064625d5d7/file_downloaded"
curl -L -o momtsim_all.zip "https://data.mendeley.com/public-api/zip/zhj366m53p/download/2"
```

Voie officielle Kaggle (avec jeton) :
```bash
pip install kaggle kagglehub
export KAGGLE_API_TOKEN=xxxxxxxxxxxxxx        # ou : echo -n "<token>" > ~/.kaggle/access_token ; ou : kaggle auth login

kaggle datasets download ealaxi/paysim1 -p data/paysim --unzip
kaggle datasets download ealtman2019/ibm-transactions-for-anti-money-laundering-aml \
  -f HI-Small_Trans.csv -p data/ibm_aml --unzip
kaggle datasets download ealtman2019/ibm-transactions-for-anti-money-laundering-aml \
  -f HI-Small_Patterns.txt -p data/ibm_aml
```
```python
import kagglehub
p = kagglehub.dataset_download("ealaxi/paysim1")
f = kagglehub.dataset_download(
    "ealtman2019/ibm-transactions-for-anti-money-laundering-aml",
    path="HI-Small_Trans.csv", output_dir="./data/ibm_aml")
```

HuggingFace (miroirs, sans compte) :
```python
from datasets import load_dataset
ds = load_dataset("flwrlabs/fed-fraud-paysim-banks")   # PaySim + colonne BankID, splits train/test
```

### Inferences
- **Ne jamais lancer `kaggle datasets download` sans `-f` sur le jeu IBM AML** : cela tire les 41,6 Go. Toujours cibler `HI-Small_*`.
- Le téléchargement anonyme Kaggle n'est documenté nulle part comme garanti ; il est cohérent avec la phrase de kagglehub (« only needed for […] user consent or private resources ») mais peut être limité ou retiré. Prévoir un jeton `KAGGLE_API_TOKEN` en secours, ou les miroirs HuggingFace.
- Pour un environnement GPU éphémère (Colab, instance de hackathon), la variable `KAGGLE_API_TOKEN` est la configuration la plus simple ; `kaggle.json` (identifiant + clé) fonctionne encore mais est présenté comme hérité.
- Les URL signées Google Storage expirent (`X-Goog-Expires=259200`, soit 3 jours) : conserver l'URL `kaggle.com/api/v1/...`, pas l'URL de redirection.

### Gaps
- Aucun téléchargement complet n'a été fait (consigne) : je n'ai testé que des plages d'octets. Un quota ou une limite de débit sur les gros fichiers en anonyme reste possible.
- Je n'ai pas testé `kaggle` CLI ni `kagglehub` **sans** identifiants ; la doc du CLI dit qu'un compte est nécessaire, celle de kagglehub dit le contraire pour les ressources publiques.
- Les variables héritées `KAGGLE_USERNAME` / `KAGGLE_KEY` ne figurent pas dans les pages de documentation lues ; leur prise en charge actuelle n'est pas confirmée.
- Le zip Mendeley « Download All » (`/public-api/zip/...`) n'a pas été testé, seulement le lien fichier.
