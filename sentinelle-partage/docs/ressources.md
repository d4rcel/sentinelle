# Ressources vérifiées pour Sentinelle

État au 19 novembre 2026. Notes détaillées, avec chaque citation et sa source, dans
`research_notes/Sentinelle ressources GPU Challenge/` (cinq fichiers).

## Comment lire ce document

La colonne « Preuve » dit d'où vient l'information :

| Marque | Sens |
|---|---|
| **Mesuré** | Nous avons téléchargé le fichier et compté nous-mêmes |
| **Lu** | Page ou fichier ouvert le 19 novembre 2026 |
| **Tiers** | Information lue chez un tiers, pas à la source |
| **Non testé** | Lien identifié, mais contenu non ouvert ou commande non exécutée |

Rien n'a été installé ni exécuté sur GPU pendant cette recherche. Les jeux de versions de la
partie 5 sont donc cohérents sur le papier, pas encore éprouvés.

---

## 1. Données

### Tableau

| Ressource | Contenu | Licence | Taille | Accès | Utilité pour Sentinelle | Preuve |
|---|---|---|---|---|---|---|
| [PaySim sur Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1) | 6 362 620 transactions de mobile money simulées sur 30 jours, 11 colonnes, 0,129 % de fraude | CC BY-SA 4.0 | 186 Mo compressé, 471 Mo en CSV | Sans compte aujourd'hui ; jeton Kaggle en secours | Trafic normal de fond pour la démo et la version 1 | Mesuré |
| [Simulateur PaySim](https://github.com/EdgarLopezPhD/PaySim) | Code Java du simulateur, dernier commit de code en 2019 | GPL-3.0 | Petit | Libre | Comprendre comment la fraude est générée. Inutile à faire tourner | Lu |
| [Article PaySim, EMSS 2016](https://www.msc-les.org/proceedings/emss/2016/EMSS2016_249.pdf) | Méthode de simulation ; données réelles fournies par Ericsson, pays africain non nommé | Article | PDF | Libre | Référence à citer | Lu |
| [IBM AML sur Kaggle](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml) | Virements bancaires simulés avec blanchiment étiqueté. Six jeux, de 5 à 180 millions de transactions | CDLA-Sharing-1.0 | 41,6 Go au total ; HI-Small : 0,48 Go | Sans compte aujourd'hui ; jeton en secours | Seul jeu avec de vrais schémas de réseau étiquetés. Sert à tester les signaux de graphe et le GNN | Lu |
| [IBM/AML-Data](https://github.com/IBM/AML-Data) | Un README et une licence. Aucune donnée : il renvoie vers Kaggle | Apache-2.0 pour le dépôt | Minuscule | Libre | Aucune, sauf la référence | Lu |
| [Article AMLworld, NeurIPS 2023](https://arxiv.org/pdf/2306.16424) | Décrit le jeu IBM AML et compare les modèles | Article | PDF | Libre | Argument pour notre ordre de travail (voir plus bas) | Lu |
| [IBM AMLSim](https://github.com/IBM/AMLSim) | Simulateur de blanchiment bancaire | Apache-2.0 | Petit | Libre | À écarter : Java 8, quinze bibliothèques à poser à la main, Python 3.7 | Lu |
| [MoMTSim-TZ sur Zenodo](https://doi.org/10.5281/zenodo.22997329) | 19 614 235 transactions de mobile money simulées, Tanzanie, 0,105 % de fraude, 12 types de fraude dont « Mule Accounts » | CC BY 4.0 | 1,31 Go compressé, 3,45 Go en CSV | Sans compte | Candidat sérieux : mobile money africain avec comptes mules étiquetés. À examiner avant de l'adopter | Lu, colonnes non testées |
| [MoMTSim Makerere sur Mendeley](https://data.mendeley.com/datasets/zhj366m53p/2) | Mobile money simulé, Ouganda, même schéma que PaySim. 1,72 et 4,23 millions de lignes | CC BY 4.0 | 149 et 349 Mo | Sans compte | Faible : 10 % et 53 % de fraude, ce qui n'est pas réaliste | Lu |
| Xente (Zindi, Ouganda) | Vraies transactions de commerce en ligne | Propriétaire, redistribution interdite | 17 Mo | Compte Zindi | Aucune : pas de lien expéditeur-destinataire | Tiers |
| [Elliptic dans PyTorch Geometric](https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.datasets.EllipticBitcoinDataset.html) | Graphe de 203 769 transactions bitcoin, 4 545 illicites | CC BY-NC-ND | Petit | Téléchargement automatique | Apprendre PyTorch Geometric sur un exemple qui marche. Pas pour le produit | Lu |

Écartés parce qu'ils ne contiennent pas de compte destinataire : Sparkov, TabFormer, BAF.
Écarté pour sa licence non commerciale : SAML-D.

**Non trouvé** : aucun jeu de données public pour l'Afrique de l'Ouest ou l'UEMOA, et aucun
jeu de données réel de mobile money étiqueté pour les comptes mules.

### Colonnes de PaySim

`step` (heure, de 1 à 743), `type` (`CASH_IN`, `CASH_OUT`, `DEBIT`, `PAYMENT`, `TRANSFER`),
`amount`, `nameOrig`, `oldbalanceOrg`, `newbalanceOrig`, `nameDest`, `oldbalanceDest`,
`newbalanceDest`, `isFraud`, `isFlaggedFraud`.

### Ce que nous avons mesuré sur PaySim

Fichier téléchargé avec `scripts/telecharger_donnees.sh`, puis compté ligne par ligne.

| Mesure | Résultat |
|---|---|
| Lignes | 6 362 620 |
| Fraudes | 8 213, soit 0,129 % |
| Fraudes par type | 4 097 en `TRANSFER`, 4 116 en `CASH_OUT`, aucune ailleurs |
| `isFlaggedFraud` | 16 lignes seulement |
| Expéditeurs distincts | 6 353 307 ; un expéditeur fait au plus 3 transactions |
| Destinataires clients (préfixe `C`) | 571 961 ; médiane de 4 transactions reçues, moyenne de 7,4 |
| Destinataires marchands (préfixe `M`) | 2 150 401 |
| Comptes ayant reçu une fraude | 8 169 ; 8 125 n'en reçoivent qu'une, 44 en reçoivent deux, aucun plus |
| Destinataires d'un transfert frauduleux qui font eux-mêmes un retrait dans le jeu | 3 sur 4 097 |
| Fraudes où le montant égale le solde de départ | 8 034 sur 8 213 |

### Pièges de PaySim

1. **Les colonnes de solde trichent.** L'auteur écrit qu'elles « must not be used » : les
   fraudes détectées sont annulées, ce qui laisse des soldes incohérents. Un modèle qui les
   lit obtient un score presque parfait et sans valeur. Même chose pour « montant égal au
   solde » : vrai pour 98 % des fraudes du jeu.
2. **Il n'y a pas de compte mule dans PaySim.** Un compte reçoit une fraude une fois, deux au
   maximum, et l'argent ne ressort pas par ce compte. Les signaux au cœur de Sentinelle
   (nombreux expéditeurs nouveaux, sortie rapide des fonds, liens avec des comptes signalés)
   n'existent pas dans ce jeu.
3. **Les expéditeurs n'ont pas d'historique.** Le signal « écart par rapport aux habitudes de
   l'expéditeur » est impossible à calculer sur PaySim tel quel.
4. `isFlaggedFraud` ne sert à rien : 16 lignes.
5. Le pays et la monnaie sont masqués. Ne pas présenter PaySim comme des données d'Afrique de
   l'Ouest.
6. Licence CC BY-SA 4.0 : citer l'auteur, et partager sous la même licence tout jeu dérivé
   que nous publierions.

**Conséquence.** Tout le signal « mule » de la démo viendra de nos scénarios injectés. Le
modèle sera donc évalué sur des schémas que nous avons écrits nous-mêmes : la mesure dira
qu'il retrouve nos scénarios, pas qu'il détecte la fraude réelle. C'est le premier risque du
projet. Voir la proposition de roadmap pour la réponse proposée.

### Pièges du jeu IBM AML

- Ne jamais télécharger le jeu entier : 41,6 Go. Le script ne prend que HI-Small.
- Deux colonnes s'appellent `Account`. La seconde devient `Account.1` à la lecture.
- Les transactions datées après la période annoncée sont toutes du blanchiment, selon
  l'auteur. Il faut les retirer avant d'entraîner.
- Ce sont des virements bancaires en plusieurs monnaies, pas du mobile money.
- Résultat utile de l'article : sur HI-Small, des signaux de graphe donnés à XGBoost
  atteignent 63,2 % de F1 sur la classe fraude, contre 56,8 % pour le meilleur GNN. Cela
  appuie notre ordre : XGBoost d'abord, GNN ensuite.

### Téléchargement

Le script `scripts/telecharger_donnees.sh` prend PaySim et IBM AML HI-Small par défaut. Testé
le 19 novembre 2026 : les six liens répondent sans compte, et PaySim a été téléchargé en
entier. Kaggle ne garantit nulle part ce téléchargement anonyme : le script explique comment
configurer un jeton en secours.

---

## 2. Code de référence

### Le blueprint NVIDIA Financial Fraud Detection

| Ressource | Contenu | Licence | Taille | Accès | Preuve |
|---|---|---|---|---|---|
| [Page du blueprint](https://build.nvidia.com/nvidia/financial-fraud-detection) | Présentation et schéma d'architecture | — | — | Libre | Lu |
| [Dépôt GitHub](https://github.com/NVIDIA-AI-Blueprints/financial-fraud-detection) | Deux notebooks, trois scripts de préparation en cuDF, un Dockerfile Triton. Dernier commit le 7 juillet 2026 | Apache-2.0 | 1,5 Mo | Libre | Lu |
| [Conteneur d'entraînement](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/cugraph/containers/financial-fraud-training) | Le code qui entraîne le GNN puis XGBoost. Version 3.0.0 | Licence NVIDIA, non lue | 13,27 Go compressé | Clé NGC, Docker, NVIDIA Container Toolkit | Lu, téléchargement non testé |
| [Documentation du conteneur](https://docs.nvidia.com/nim/financial-fraud-training/latest/index.html) | Format des données, configuration, prérequis | — | — | Libre | Lu |
| [Jeu TabFormer d'IBM](https://github.com/IBM/TabFormer) | 24 millions de paiements par carte simulés, utilisés par le blueprint | Apache-2.0 | 266 Mo | Libre | Lu |

**Architecture.** cuDF prépare les données et construit un graphe clients-marchands. Le
conteneur entraîne un GNN GraphSAGE, qui produit une représentation de chaque nœud. XGBoost
est ensuite entraîné sur ces représentations. Triton sert le modèle et renvoie la prédiction
avec ses valeurs de Shapley.

**Matériel.** La documentation demande un GPU d'au moins 32 Go de mémoire (A6000, A100, H100).
Une autre page NVIDIA cite le T4 comme acceptable : les deux se contredisent. Nous
considérons le T4 comme non supporté tant que ce n'est pas prouvé.

**Ce qui bloque.**

- Le dépôt ne contient aucun code d'entraînement. Tout se passe dans le conteneur fermé.
- Il faut une clé NGC. Le README parle d'une licence NVIDIA AI Enterprise ; la documentation
  dit qu'un compte gratuit suffit. Non tranché, non testé.
- Les notebooks du dépôt visent la version 2.0.0 du conteneur, incompatible avec la 3.0.0.
- Le jeu utilisé est de la fraude à la carte bancaire, sans compte destinataire.

**Ce que nous pouvons réutiliser tel quel.**

- L'idée en deux étages (représentation du graphe, puis XGBoost) et son explication.
- Les réglages publiés : GraphSAGE à 2 sauts, 32 dimensions ; XGBoost profondeur 6, 512 arbres.
- Les scripts de préparation cuDF comme modèle de code.
- Le découpage temporel des données et la cellule d'évaluation.

**Verdict.** Source d'inspiration à citer, pas une brique à faire tourner. Ne pas promettre au
jury que nous « utilisons le blueprint NVIDIA ».

Seul chiffre de gain trouvé : un [article NVIDIA de 2022](https://developer.nvidia.com/blog/optimizing-fraud-detection-in-financial-services-with-graph-neural-networks-and-nvidia-gpus/)
rapporte une précision moyenne passant de 0,79 à 0,90 en ajoutant les représentations du
graphe, sur TabFormer.

### PyTorch Geometric

| Ressource | Contenu | Licence | Accès | Utilité | Preuve |
|---|---|---|---|---|---|
| [PyTorch Geometric](https://github.com/pyg-team/pytorch_geometric) | Bibliothèque de GNN, version 2.8.1 | MIT | Libre | Base de la version 2 | Lu |
| [Tutoriel NeighborLoader](https://pytorch-geometric.readthedocs.io/en/latest/tutorial/neighbor_loader.html) | Entraîner un GNN sur un grand graphe par petits lots de voisins | MIT | Libre | Méthode à suivre pour GraphSAGE | Lu |
| [Notebooks Colab officiels](https://pytorch-geometric.readthedocs.io/en/latest/get_started/colabs.html) | Liste de tutoriels pas à pas | MIT | Compte Google | Montée en compétences de l'équipe | Liste lue, notebooks non testés |
| [IBM Multi-GNN](https://github.com/IBM/Multi-GNN) | GNN pour le jeu IBM AML (GIN, GAT, PNA, RGCN) | Apache-2.0 | Libre | Chargement du jeu IBM AML en graphe | Lu |
| [Exemples fraude de cugraph-gnn](https://github.com/rapidsai/cugraph-gnn/tree/main/python/cugraph-pyg/cugraph_pyg/examples/fraud) | Représentations d'Elliptic données à une forêt aléatoire sur GPU | Apache-2.0 | Libre | Exemple le plus proche de notre version 2 | Lu |
| [Exemple GNN de Morpheus](https://github.com/nv-morpheus/Morpheus/tree/branch-25.06/examples/gnn_fraud_detection_pipeline) | GNN puis XGBoost, avec modèles déjà entraînés | Apache-2.0 | Libre | Lecture seulement : utilise DGL, pas PyTorch Geometric | Lu |

**Non trouvé** : aucun tutoriel officiel PyTorch Geometric qui enchaîne représentations de
graphe et XGBoost. Le seul notebook communautaire trouvé n'a pas de licence, et XGBoost seul y
bat le GNN.

### XGBoost sur GPU et RAPIDS

| Ressource | Contenu | Licence | Utilité | Preuve |
|---|---|---|---|---|
| [XGBoost, page GPU](https://xgboost.readthedocs.io/en/stable/gpu/index.html) | `device="cuda"` avec `tree_method="hist"` | Apache-2.0 | Un seul paramètre sépare le CPU du GPU | Lu |
| [XGBoost, exemple de SHAP sur GPU](https://xgboost.readthedocs.io/en/stable/python/examples/gpu_tree_shap.html) | `pred_contribs=True` donne la contribution de chaque signal à un score | Apache-2.0 | La « raison lisible » de Sentinelle | Lu |
| [cudf.pandas](https://docs.rapids.ai/api/cudf/stable/cudf_pandas/) | Accélère du code pandas sur GPU sans le modifier, avec repli sur CPU | Apache-2.0 | Écrire en pandas maintenant, accélérer au hackathon | Lu |
| [Installation RAPIDS](https://docs.rapids.ai/install/) | Sélecteur de commandes conda, pip et Docker | Apache-2.0 | Commandes officielles | Lu |

Trois faits vérifiés dans la documentation XGBoost, importants pour nous :

- Un modèle entraîné sur GPU fonctionne sur une machine sans GPU, et inversement.
- La prédiction est sûre en accès concurrent, donc utilisable dans FastAPI.
- Le format à utiliser pour sauvegarder est `.ubj` ou `.json`, pas `pickle`.

---

## 3. Contexte métier et réglementaire

La synthèse est dans `docs/contexte-pispi.md`, les scénarios dans `docs/scenarios-fraude.md`.

| Ressource | Contenu | Utilité | Preuve |
|---|---|---|---|
| [Avis BCEAO n°0019 du 2 octobre 2026](https://www.bceao.int/fr/reglementations/avis-ndeg0019-relatif-aux-transactions-de-monnaie-electronique-entre-personnes) | Obligation de passer par PI-SPI à partir du 2 novembre 2026 | Le fait qui ouvre le pitch | Lu |
| [FAQ PI-SPI, transferts](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=5) | Irrévocabilité, affichage du nom du bénéficiaire | Citation exacte sur l'irrévocabilité | Lu |
| [Portail développeurs PI-SPI](https://developer.pispi.bceao.int/guides/vue-ensemble) | ISO 20022, délai maximum de 20 secondes, demande d'annulation | Où placer Sentinelle | Lu |
| [Instruction BCEAO n°001-01-2024](https://www.bceao.int/sites/default/files/inline-files/Instruction-No001-01-2024_relative_aux_services_de_paiement_dans_l-UMOA.pdf) | Obligations des prestataires de paiement | Article 83 : outils de prévention de la fraude | Lu |
| [Rapport BCEAO 2024 sur les services financiers numériques](https://www.bceao.int/sites/default/files/2026-03/Rapport%20annuel%20sur%20les%20services%20financiers%20num%C3%A9riques%20dans%20l'UEMOA%20-%202024.pdf) | Comptes, volumes, valeurs par pays | Chiffres de marché | Lu |
| [Alerte du CNIN, novembre 2026](https://linvestigateur.info/benin-le-cnin-alerte-sur-une-nouvelle-arnaque-au-mobile-money/) | Arnaque du faux agent d'opérateur au Bénin | Actualité toute récente pour le pitch | Lu |
| [Typologie GSMA des fraudes au mobile money](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-for-development/wp-content/uploads/2024/05/Mobile-Money-Fraud-Typologies-and-Mitigation-Strategies-20.05.24.pdf) | Classement des fraudes, rôle des mules et de la vitesse des fonds | Vocabulaire de référence | Lu |
| [Enquêtes CGAP dans l'UEMOA](https://www.cgap.org/blog/surveys-reveal-path-to-responsible-digital-finance-in-waemu) | Part des usagers exposés à une tentative de fraude | Seul chiffre d'ampleur fiable ; le Bénin n'y est pas | Lu |

**Non trouvé** : aucun chiffre public isolant la fraude au mobile money au Bénin ou dans
l'UEMOA, et aucune statistique de fraude sur PI-SPI.

### L'événement et les partenaires

| Ressource | Ce que nous avons appris | Preuve |
|---|---|---|
| [Programme du Next Fintech Forum 2026](https://nextfintechforum.com/programme) | Forum les 26 et 27 novembre au Sofitel de Cotonou. Fintech Academia le 25 novembre, journée complète, dans un lieu partenaire non nommé, avec « pitch d'étudiants devant un jury professionnel » | Lu |
| [Annonce de l'Alliance sur Epitech](https://fr.linkedin.com/posts/alliance-fintech-uemoa_nff2026-epitech-strategicpartner-activity-7525320467331563520-wvMe) | Le GPU Challenge est « intégré à Fintech Academia », coorganisé par l'Alliance, Epitech et Udu Technologies | Lu |
| [Udu Technologies](https://udutech.co/) et [AGH Cloud](https://aghcloud.ai/) | Entreprise d'infrastructure IA, bureaux au Texas et à Lagos. Son produit AGH Cloud loue des GPU et distribue des crédits GPU pour des challenges. D'autres programmes donnent des heures de RTX 5090 | Lu |
| [Documentation Payfonte](https://docs.payfonte.com/llms.txt) | Plateforme d'orchestration de paiements. Au Bénin : MTN MoMo et Moov, en encaissement et en décaissement. Bac à sable disponible | Lu |
| [Payfonte, mode d'autorisation des décaissements](https://docs.payfonte.com/en/guides/disbursements/authorization-mode.md) | Avant chaque décaissement, Payfonte appelle une adresse du marchand et ne continue que sur une réponse 200. La documentation le recommande pour les contrôles de risque | Lu |

**Comment Sentinelle s'intègre chez Payfonte.** Le marchand déclare comme adresse
d'autorisation un service qui interroge Sentinelle sur le compte bénéficiaire, puis répond 200
si le score est bas. Aucune modification n'est nécessaire côté Payfonte. Contrainte : si notre
service ne répond pas, le décaissement est bloqué.

**Comment Sentinelle s'intègre avec Udu Technologies.** Udu fournit le calcul : entraînement
sur ses GPU, puis hébergement du service.

Trois points à connaître avant le pitch :

- Aucune source publique ne lie Payfonte au GPU Challenge. Payfonte apparaît comme sponsor du
  forum. L'information vient donc de vos échanges avec les organisateurs.
- Les arnaques de nos scénarios sont des transferts entre particuliers, faits dans
  l'application de l'opérateur. Elles ne passent pas par un agrégateur comme Payfonte. Chez
  Payfonte, le cas d'usage honnête est le contrôle du bénéficiaire avant un décaissement.
- Le type de GPU, le quota, le règlement et les critères du jury ne sont publiés nulle part.

---

## 4. Faisabilité : ce qui tourne où

| Tâche | Ordinateur actuel (8 cœurs, 23 Go, pas de GPU) | Kaggle ou Colab gratuit | GPU du hackathon |
|---|---|---|---|
| Explorer PaySim, écrire les signaux en pandas | Oui | Oui | — |
| Injecter les scénarios | Oui | Oui | — |
| Entraîner XGBoost sur CPU | Oui, estimé à quelques minutes, non mesuré | Oui | — |
| Entraîner XGBoost sur GPU | Non | Oui, sur T4 | Oui |
| Accélérer la préparation avec cuDF | Non | Oui, cuDF est préinstallé | Oui |
| Service FastAPI et démo Streamlit | Oui, sans GPU | — | Oui |
| GNN sur un petit graphe | Oui, lentement | Oui | Oui |
| GNN sur le graphe complet | Non | Peut-être | Oui |
| Mesure du gain CPU contre GPU | Non | Oui, première mesure | Mesure finale |

### Options de GPU gratuites

| Service | Ce qui est offert | Limites | Preuve |
|---|---|---|---|
| [Kaggle Notebooks](https://www.kaggle.com/docs/efficient-gpu-usage) | 30 heures de GPU par semaine, deux T4 ou un P100, 29 Go de mémoire | Sessions de 12 heures. Choisir T4 : le P100 n'est plus supporté par RAPIDS | Lu |
| [Google Colab](https://research.google.com/colaboratory/faq.html) | GPU gratuit, cuDF préinstallé | Google ne publie ni les limites ni le type de GPU | Lu |
| [Lightning AI](https://lightning.ai/pricing) | Jusqu'à 50 heures de GPU gratuites | Redémarrage toutes les 4 heures | Lu |
| [Modal](https://modal.com/pricing) | 30 dollars de crédit par mois | Demande d'écrire du code spécifique | Lu |

Recommandation : Kaggle comme terrain d'entraînement, parce que le quota est écrit noir sur
blanc et que PaySim y est déjà hébergé.

Hugging Face Spaces n'héberge plus gratuitement une démo Streamlit : la création d'un espace
avec calcul demande un abonnement payant.

---

## 5. Versions compatibles

Versions lues sur PyPI et sur les pages officielles le 19 novembre 2026.

| Paquet | Version | Python requis |
|---|---|---|
| RAPIDS (cuDF, cuML, cuGraph) | 26.10 | 3.11 à 3.14 |
| XGBoost | 3.4.1 | 3.12 ou plus |
| PyTorch | 2.15.0 | 3.11 ou plus |
| PyTorch Geometric | 2.8.1 | 3.10 ou plus |
| SHAP | 0.54.1 | 3.12 ou plus |
| scikit-learn | 1.9.1 | 3.11 ou plus |
| FastAPI | 0.165.0 | 3.11 ou plus |
| Streamlit | 1.67.0 | 3.11 ou plus |
| kagglehub / kaggle | 1.0.3 / 2.2.5 | 3.11 ou plus |

RAPIDS 26.12 sort les 9 et 10 décembre 2026 : la version 26.10 reste la version stable pendant
le hackathon.

**Python.** Utiliser Python 3.12 dans un environnement isolé. C'est la plus petite version
acceptée par tous les paquets. Le Python 3.14 du système fonctionnerait d'après les
métadonnées, mais c'est le choix le moins éprouvé.

### Deux jeux de versions, selon le pilote NVIDIA trouvé sur place

La commande `nvidia-smi` affiche la version du pilote. Elle décide de tout.

**Jeu A, CUDA 13 : pilote 580 ou plus récent**

```bash
pip install --extra-index-url=https://pypi.nvidia.com "cudf-cu13==26.10.*" "cuml-cu13==26.10.*" "cugraph-cu13==26.10.*"
pip install torch==2.15.0 torch_geometric==2.8.1
pip install xgboost==3.4.1 shap==0.54.1 scikit-learn==1.9.1 fastapi==0.165.0 uvicorn streamlit==1.67.0
```

**Jeu B, CUDA 12 : pilote entre 535 et 579**

```bash
pip install --extra-index-url=https://pypi.nvidia.com "cudf-cu12==26.10.*" "cuml-cu12==26.10.*" "cugraph-cu12==26.10.*"
pip install torch==2.14.1 --index-url https://download.pytorch.org/whl/cu126
pip install torch_geometric==2.8.1
pip install xgboost-cu12==3.4.1 shap==0.54.1 scikit-learn==1.9.1 fastapi==0.165.0 uvicorn streamlit==1.67.0
```

Ces deux jeux sont assemblés à partir des contraintes déclarées par chaque paquet. **Aucun
n'a été installé.** Il faut les valider une fois sur Kaggle avant le hackathon.

### Conflits connus

- cuDF 26.10 impose pandas 3.0.x et numpy entre 2.0 et 2.4. Développer dès maintenant avec ces
  versions.
- Ne jamais installer `torch_geometric[full]` : cette variante exige une version de numba
  incompatible avec cuDF.
- Le paquet `xgboost` par défaut est compilé pour CUDA 13. Sur un pilote plus ancien, il faut
  `xgboost-cu12`.
- Jeu B : un conflit entre PyTorch pour CUDA 12.6 et RAPIDS pour CUDA 12 est plausible, non
  confirmé. Solution de repli : deux environnements séparés, un pour RAPIDS et XGBoost, un pour
  PyTorch, qui s'échangent des fichiers Parquet.
- Avec PyTorch 2.15, les extensions compilées de PyTorch Geometric (`pyg_lib`) n'existent pas
  encore. La bibliothèque de base suffit pour GraphSAGE.
- GPU minimum pour RAPIDS : génération Volta pour CUDA 12, génération Turing (T4) pour CUDA 13.

### Poids des téléchargements

| Élément | Taille compressée |
|---|---|
| Image Docker `rapidsai/base:26.10-cuda13-py3.12` | 4,16 Go |
| Image Docker `rapidsai/base:26.10-cuda12-py3.12` | 5,93 Go |
| Plus gros paquets pip | libcugraph 969 Mo, libcudf 667 Mo, PyTorch 539 Mo |

Les images Docker RAPIDS ne contiennent ni PyTorch, ni PyTorch Geometric, ni XGBoost. À
10 Mbit/s, une installation complète prend environ une heure : elle ne doit pas dépendre du
réseau de la salle.

---

## 6. Questions à poser aux organisateurs

Ces réponses ne sont publiées nulle part et conditionnent la préparation.

1. Quel GPU, avec combien de mémoire, et combien d'heures par équipe ?
2. Accès par notebook dans le navigateur, par SSH, ou sur une machine dans la salle ?
3. Quelle version du pilote NVIDIA ? Docker est-il disponible, avec les droits nécessaires ?
4. Quel débit Internet dans la salle ?
5. Le code écrit avant le hackathon est-il autorisé ?
6. Quand a lieu le pitch final, combien de temps dure-t-il, et quels sont les critères du jury ?
7. Le programme officiel place Fintech Academia le 25 novembre. Que se passe-t-il le 26 ?
