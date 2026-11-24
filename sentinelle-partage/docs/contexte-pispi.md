# PI-SPI en bref : ce qu'il faut savoir pour le pitch

Synthèse rédigée le 19 novembre 2026. Toutes les pages citées ont été ouvertes ce jour-là.
Notes détaillées : `research_notes/Sentinelle ressources GPU Challenge/pispi_bceao.md`.

Niveau de preuve indiqué entre crochets :

- **[Officiel]** : lu sur un site de la BCEAO (bceao.int, pispi.bceao.int, developer.pispi.bceao.int).
- **[Officiel, copie tierce]** : document à en-tête BCEAO, mais lu sur un autre site.
- **[Presse]** : article de presse ou publication d'un tiers.
- **[Notre lecture]** : déduction de notre part, à présenter comme telle.

## 1. Ce qu'est PI-SPI

- PI-SPI est la Plateforme Interopérable du Système de Paiement Instantané, conçue et opérée par la BCEAO. Elle relie banques, émetteurs de monnaie électronique, institutions de microfinance et établissements de paiement des 8 pays de l'UEMOA, 24h/24 et 7j/7, en francs CFA uniquement. [Officiel] — [pispi.bceao.int](https://pispi.bceao.int)
- Elle a été lancée officiellement le 30 septembre 2025 à Dakar. [Officiel] — [annonce BCEAO](https://www.bceao.int/fr/content/lancement-officiel-de-la-plateforme-interoperable-du-systeme-de-paiement-instantane-pi-spi)
- Au 30 septembre 2026, 175 participants sont autorisés à ouvrir le service au public, dont 18 au Bénin. [Officiel] — [liste BCEAO](https://www.bceao.int/sites/default/files/inline-files/Liste%20des%20participants_PI-SPI_30_sept_2026_0.pdf)
- Plus de 38 millions de personnes ont accès au service au 2 octobre 2026. Ce sont les clients des établissements connectés, pas des utilisateurs actifs. [Officiel] — [communiqué du 2 octobre 2026](https://www.bceao.int/sites/default/files/2026-10/Communiqu%C3%A9%20du%202%20octobre%202026.pdf)
- Un envoi se fait par alias (numéro de téléphone ou « adresse de paiement »), par QR code, en acceptant une demande de paiement, ou par saisie du compte. [Officiel] — [FAQ Transferts](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=5)

## 2. La règle du 2 novembre 2026

Notre affirmation de départ est confirmée, avec une formulation à corriger.

- Le texte est l'**Avis n°0019** du Gouverneur de la BCEAO, signé le 2 octobre 2026, entré en vigueur le 2 novembre 2026. [Officiel] — [page de l'avis](https://www.bceao.int/fr/reglementations/avis-ndeg0019-relatif-aux-transactions-de-monnaie-electronique-entre-personnes), [PDF](https://www.bceao.int/sites/default/files/2026-10/AVIS%20N%C2%B0%200019%20%20DU%202%20OCTOBRE%202026%20%281%29.pdf)
- Phrase exacte (point 2) : « Toutes les transactions de monnaie électronique interopérables, au sein de l'UEMOA, sont obligatoirement réalisées par l'intermédiaire de PI-SPI. »
- Champ d'application (point 1) : les transferts de monnaie électronique **entre personnes physiques**, au plan national et dans l'UEMOA.
- Le communiqué du même jour précise que cela couvre les transferts entre un compte en banque ou en microfinance et un compte de monnaie électronique, et les transferts entre émetteurs de monnaie électronique et établissements de paiement. [Officiel] — [communiqué](https://www.bceao.int/sites/default/files/2026-10/Communiqu%C3%A9%20du%202%20octobre%202026.pdf)

Trois précautions de langage :

1. C'est un **Avis**, pas une Instruction.
2. Le texte dit « interopérables », pas « entre établissements différents ».
3. Les virements de banque à banque ne semblent pas visés. [Notre lecture]

Phrase sûre pour le pitch : « Depuis le 2 novembre 2026 (Avis BCEAO n°0019), toutes les transactions de monnaie électronique interopérables dans l'UEMOA passent obligatoirement par PI-SPI. »

Réserve : les deux PDF sont des documents scannés, lus par reconnaissance de caractères. Le numéro « 0019 » vient du titre de la page BCEAO et du nom du fichier.

## 3. Rapidité et irrévocabilité

- Le site public promet un paiement « traité en moins de 10 secondes ». Le portail développeurs fixe un temps maximum de traitement de 20 secondes. [Officiel] — [accueil](https://pispi.bceao.int), [vue d'ensemble développeurs](https://developer.pispi.bceao.int/guides/vue-ensemble)
- FAQ PI-SPI : « Une fois confirmée, l'opération d'envoi est irrévocable. Il n'est plus possible pour l'établissement teneur de votre compte de l'annuler. » [Officiel] — [FAQ Transferts](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=5)
- Base juridique : article 75 de l'Instruction n°001-01-2024 sur les services de paiement, et article 6 du Règlement n°15/2002/CM/UEMOA. [Officiel] — [Instruction](https://www.bceao.int/sites/default/files/inline-files/Instruction-No001-01-2024_relative_aux_services_de_paiement_dans_l-UMOA.pdf), [Règlement](https://www.bceao.int/sites/default/files/inline-files/Reglement_n_15_2002_CM_UEMOA_relatif_aux_systemes_de_paiement_dans_les_Etats_membres_de_l_UEMOA.pdf)

Conséquence pour Sentinelle : le score doit revenir en quelques centaines de millisecondes pour tenir dans l'écran de confirmation. [Notre lecture]

## 4. Que peut faire une victime après coup

- L'expéditeur peut seulement envoyer une **demande d'annulation**. Elle n'a d'effet que si le bénéficiaire la valide : « Sans cette validation, aucun retour de fonds n'est effectué. » La fraude figure parmi les cas d'usage prévus. [Officiel] — [guide retours et annulations](https://developer.pispi.bceao.int/guides/retour-overview)
- Le bénéficiaire peut renvoyer les fonds de lui-même (« retour de fonds »). Les deux opérations sont gratuites. [Officiel] — [FAQ Frais](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=3)
- L'Instruction n°001-01-2024 impose le remboursement immédiat des opérations **non autorisées** (art. 69) et laisse 9 mois au client pour les signaler (art. 67). [Officiel]
- Dans une arnaque par manipulation, la victime valide elle-même le transfert avec son code. L'opération est donc « autorisée » et ce remboursement ne s'applique pas automatiquement. [Notre lecture, pas une position de la BCEAO]

Non trouvé : aucun délai de réponse à une demande d'annulation, aucune procédure d'arbitrage entre participants. Les guides correspondants du portail affichent « Contenu en cours de rédaction ».

## 5. Ce que la BCEAO impose déjà contre la fraude

- Avant de confirmer, l'application affiche « systématiquement les nom, prénom et pays du propriétaire de l'alias ». [Officiel] — [FAQ Transferts](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=5)
- Authentification forte avec un lien entre l'opération, le montant et le bénéficiaire (Instruction n°001-01-2024, art. 85). [Officiel]
- Le système d'information du prestataire doit prévenir la fraude avec « des outils de prévention appropriés » et traiter les opérations en temps réel (art. 83). [Officiel]
- La FAQ Sécurité renvoie les clients vers les consignes de leur établissement. [Officiel] — [FAQ Sécurité](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=7)

Deux conséquences pour le pitch :

- Ne pas présenter Sentinelle comme « l'affichage du nom du bénéficiaire » : il existe déjà. Sentinelle ajoute ce que le nom ne dit pas : le compte se comporte-t-il comme un compte mule ?
- L'article 83 est notre accroche réglementaire : la prévention de la fraude est déjà à la charge de chaque participant. [Notre lecture]

Non trouvé : aucune statistique officielle de fraude sur PI-SPI, aucune campagne BCEAO spécifique contre les arnaques sur PI-SPI.

## 6. Messages ISO 20022 et place de Sentinelle

- « Toutes les interactions entre les participants et PI-SPI s'appuient sur » la norme ISO 20022. L'architecture est en étoile : chaque participant se connecte une fois au hub de la BCEAO. [Officiel] — [vue d'ensemble développeurs](https://developer.pispi.bceao.int/guides/vue-ensemble)
- Messages nommés dans un document tarifaire BCEAO de juin 2024 : acmt.023 et acmt.024 (recherche d'alias), pacs.008 (transfert), pacs.002 (statut), pacs.004 (retour de fonds), pain.013 et pain.014 (demande de paiement), camt.056 et camt.029 (demande d'annulation). [Officiel, copie tierce] — [copie MicroSave](https://www.microsave.net/fr/wp-content/uploads/2024/11/Tarification-des-services-interope%CC%81rables.pdf)
- Seule l'API Business (du participant vers ses clients entreprises) est documentée publiquement, avec un bac à sable. [Officiel] — [API Business](https://developer.pispi.bceao.int/api-business)

Place de Sentinelle : chez le participant de l'expéditeur, entre la réponse à la recherche d'alias et l'envoi du pacs.008, c'est-à-dire pendant l'écran de confirmation. [Notre lecture]

Non trouvé : les spécifications détaillées des messages ne sont pas publiques, et aucun champ n'est prévu pour transporter un score de risque. Ne pas affirmer le contraire devant le jury.

## 7. Chiffres utiles

Monnaie électronique dans l'UEMOA en 2024 [Officiel] — [rapport BCEAO sur les services financiers numériques 2024, publié en mars 2026](https://www.bceao.int/sites/default/files/2026-03/Rapport%20annuel%20sur%20les%20services%20financiers%20num%C3%A9riques%20dans%20l'UEMOA%20-%202024.pdf) :

| Indicateur | Valeur 2024 |
|---|---|
| Comptes de monnaie électronique ouverts | 248,7 millions |
| Comptes actifs | 76,9 millions |
| Comptes ouverts au Bénin | 37,5 millions |
| Transactions | 11,9 milliards, pour 160 415 milliards FCFA |
| Transferts de personne à personne | 2,35 milliards, pour 42 763 milliards FCFA |
| Montant moyen d'un transfert | 18 220 FCFA |

PI-SPI lui-même :

- Environ 1 million de transactions et 110 milliards FCFA au 20 juillet 2026. [Presse] — [Agence Ecofin, 24 juillet 2026](https://www.agenceecofin.com/actualites-finance/2407-140469-pi-spi-30-millions-de-personnes-connectees-et-190-millions-de-transactions-en-moins-dun-an)
- Aucun chiffre trouvé depuis le 2 novembre 2026.

Tarifs depuis le 2 novembre 2026 [Officiel, Avis n°0019] : l'envoi national est gratuit jusqu'à 8 000 FCFA cumulés par jour, puis coûte de 0 à 0,8 %. La réception est gratuite. Ne plus dire « gratuit pour les particuliers » sans cette précision.

## 8. À ne pas dire devant le jury

- « Tous les virements passent par PI-SPI » : l'avis vise la monnaie électronique entre personnes physiques.
- « 38 millions d'utilisateurs » : ce sont des personnes ayant accès au service.
- « PI-SPI prévoit un champ pour le score de risque » : rien de tel n'a été trouvé.
- Un plafond de montant par transaction : aucun chiffre officiel trouvé.
- Un chiffre de fraude sur PI-SPI : il n'en existe pas de public.
