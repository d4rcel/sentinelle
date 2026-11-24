# PI-SPI (BCEAO / UEMOA) — notes vérifiées pour un pitch « scoring anti-fraude avant confirmation d'un transfert instantané »

Recherche effectuée le 2026-11-19. Toutes les URL ci-dessous ont été réellement ouvertes ce jour-là (lecture via r.jina.ai ou téléchargement direct ; les deux PDF scannés de la BCEAO du 2 octobre 2026 ont été lus par OCR tesseract).

Légende de fiabilité utilisée dans chaque puce :
- **[OFFICIEL]** = lu dans un document ou une page de la BCEAO (bceao.int, pispi.bceao.int, developer.pispi.bceao.int).
- **[OFFICIEL-HÉBERGÉ-TIERS]** = document à en-tête BCEAO, mais lu sur un site tiers (version et statut à confirmer).
- **[SECONDAIRE]** = presse, blog, post LinkedIn, rapport indépendant.
- Les pages pispi.bceao.int et developer.pispi.bceao.int ne portent pas de date de publication : « consulté le 2026-11-19 ».

---

## 1. Qu'est-ce que PI-SPI (opérateur, lancement, participants, services, disponibilité, délai, tarifs, marque)

### Takeaway
PI-SPI est le système de paiement instantané interopérable conçu et opéré par la BCEAO, lancé officiellement le 30 septembre 2025 à Dakar, ouvert 24h/24 7j/7 aux banques, EME, SFD et établissements de paiement des 8 pays ; au 2 octobre 2026 la BCEAO annonce 175 participants connectés et plus de 38 millions de personnes ayant accès au service. Attention : la « gratuité pour les particuliers » n'est plus vraie telle quelle depuis le 2 novembre 2026 (gratuit seulement jusqu'à 8 000 FCFA cumulés par jour à l'envoi).

### Cited Findings

**Nature, opérateur, lancement**
- [OFFICIEL] PI-SPI = « infrastructure régionale de paiement conçue et opérée par la BCEAO » ; elle permet d'envoyer et recevoir des fonds instantanément entre banques, émetteurs de monnaie électronique, institutions de microfinance et établissements de paiement ; « en quelques secondes, 24h/24, 7j/7 ». — [pispi.bceao.int, page d'accueil, consultée 2026-11-19](https://pispi.bceao.int)
- [OFFICIEL] Lancement officiel le 30 septembre 2025 à Dakar, cérémonie présidée par le ministre sénégalais des Finances Cheikh Diba ; infrastructure développée « intégralement en interne » par la BCEAO ; « accessible en continu dans les huit pays de l'UEMOA ». — [BCEAO, « Lancement officiel de la PI-SPI », 30 sept. 2025](https://www.bceao.int/fr/content/lancement-officiel-de-la-plateforme-interoperable-du-systeme-de-paiement-instantane-pi-spi)
- [OFFICIEL] Annonce préalable : communiqué daté du 1er août 2025 fixant le lancement au mardi 30 septembre 2025 ; tests en conditions réelles démarrés le 5 juin 2025 ; annexe au 31 juillet 2025 : 86 participants à l'étape 2 du pilote (70 banques, 10 SFD, 6 EME). — [BCEAO, communiqué + annexe, 1er août 2025](https://www.bceao.int/sites/default/files/2025-08/Communique%2BAnnexe-Lancement_du_Syste%CC%80me_de_paiement_instantane%CC%81_31_Juillet_2025.pdf)
- [OFFICIEL] Monnaie : franc CFA uniquement ; pas de transactions hors UEMOA. — [FAQ PI-SPI, consultée 2026-11-19](https://pispi.bceao.int/foire-aux-questions) et [FAQ Transferts](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=5)

**Participants : nombre et chronologie (tous chiffres BCEAO)**
- [OFFICIEL] Au 2 avril 2026 : 80 participants connectés (59 banques, 9 EME, 11 institutions de microfinance, 1 établissement de paiement) + 42 institutions en tests réels. — [BCEAO, communiqué du 2 avril 2026](https://www.bceao.int/sites/default/files/2026-04/Communiqu%C3%A9_Connexion_%C3%A0_PI-SPI_2_avril_2026.pdf)
- [OFFICIEL] Au 24 juin 2026 : 80 participants connectés + 74 institutions en phase de test réel. — [BCEAO, « Prolongation du délai de connexion à PI-SPI », PDF daté 25/06/2026](https://www.bceao.int/fr/communique-presse/prolongation-du-delai-de-connexion-a-pi-spi)
- [OFFICIEL] Au 30 septembre 2026 : « Liste des participants autorisés à ouvrir les services de PI-SPI au public (175) » (ex. Bénin 18, Burkina Faso 20, Côte d'Ivoire 38). — [BCEAO, liste des participants, mise à jour 30 sept. 2026](https://www.bceao.int/sites/default/files/inline-files/Liste%20des%20participants_PI-SPI_30_sept_2026_0.pdf)
- [OFFICIEL] Au 2 octobre 2026 : « 175 participants connectés » et « plus de 38 millions de personnes » ayant accès aux services. — [BCEAO, communiqué du 2 octobre 2026 (PDF scanné, lu par OCR)](https://www.bceao.int/sites/default/files/2026-10/Communiqu%C3%A9%20du%202%20octobre%202026.pdf)
- [OFFICIEL] La page « Chiffres clés » du site PI-SPI affiche encore « 70+ institutions financières participantes » : chiffre non daté et manifestement antérieur, à ne pas citer. — [pispi.bceao.int/chiffres-cles, consultée 2026-11-19](https://pispi.bceao.int/chiffres-cles)

**Catégories de clients et vocabulaire**
- [OFFICIEL] 4 types de clients : P (personne physique), C (personne physique commerçante), B (personne morale), G (administration publique). Un « transfert » = virement vers un client P tant qu'il a reçu au plus 30 transferts dans le mois calendaire ; un « paiement » = virement vers B, C, G (ou vers un P à partir du 31e reçu dans le mois). — [FAQ PI-SPI](https://pispi.bceao.int/foire-aux-questions)

**Services**
- [OFFICIEL] Modes d'envoi : par alias, par QR code, par acceptation d'une demande de paiement, ou par saisie directe (établissement + numéro de compte) si le bénéficiaire n'a pas d'alias. Paiements programmés et abonnements possibles (modifiables jusqu'à la veille). — [FAQ Transferts](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=5)
- [OFFICIEL] Services de base listés pour les intégrateurs : alias de compte, QR code interopérable, envoi de fonds (transfert/paiement), demande de paiement (Request To Pay), retour de fonds, demande d'annulation ; paiements en masse via API Business. — [Portail développeurs, guide « Vue d'ensemble », consulté 2026-11-19](https://developer.pispi.bceao.int/guides/vue-ensemble)
- [OFFICIEL] Alias = identifiant unique dans l'UEMOA associé à un compte : soit le numéro de téléphone, soit une « adresse de paiement » générée par PI-SPI. Un seul alias par compte pour une personne physique (si elle choisit le téléphone, une adresse de paiement est créée en plus). Seule l'adresse de paiement figure dans le QR code, jamais le numéro de téléphone. Procédure de « revendication » d'un numéro déjà utilisé comme alias : jusqu'à 2 semaines. — [pispi.bceao.int/lalias, consultée 2026-11-19](https://pispi.bceao.int/lalias)
- [OFFICIEL] QR code standardisé unique, reconnaissable au logo PI-SPI en forme d'octogone (8 pays). — [pispi.bceao.int/lalias](https://pispi.bceao.int/lalias)
- [OFFICIEL] Retraits chez un commerçant : PICO (retrait avec achat) et PICASH (retrait sans achat). Débit différé et paiement en plusieurs mensualités possibles si le teneur de compte l'offre. — [FAQ Retraits](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=6) et [FAQ Demande de paiement](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=4)
- [OFFICIEL] Canaux : application mobile que le participant « a l'obligation de mettre à votre disposition » ; USSD ou web possibles selon le participant, à ses conditions tarifaires. — [FAQ PI-SPI](https://pispi.bceao.int/foire-aux-questions) et [FAQ Transferts](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=5)

**Délai d'exécution — deux chiffres officiels différents**
- [OFFICIEL] Site public : « le paiement est traité en moins de 10 secondes », expéditeur et bénéficiaire notifiés instantanément ; encaissement « de 48h à moins de 10 secondes ». — [pispi.bceao.int accueil](https://pispi.bceao.int) et [pispi.bceao.int/propos](https://pispi.bceao.int/propos)
- [OFFICIEL] Portail développeurs : « Chaque transaction dispose d'un temps maximum de traitement de 20 secondes. Les fonds doivent être crédités immédiatement sur le compte du bénéficiaire dès l'irrévocabilité. » — [guide « Vue d'ensemble »](https://developer.pispi.bceao.int/guides/vue-ensemble)

**Tarification (état au 2026-11-19)**
- [OFFICIEL] Depuis le 2 novembre 2026 (Avis n°0019) : à l'émission, transferts nationaux gratuits tant que le cumul quotidien est ≤ 8 000 FCFA « par utilisateur et par participant », sans limite de nombre ; au-delà, frais possibles de 0 à 0,8 % du montant hors taxes ; à la réception, gratuité sans limite de nombre ni de montant ; mêmes conditions pour l'intra-UEMOA à partir du 1er juin 2027. — [Avis n°0019, PDF scanné lu par OCR, signé le 2 oct. 2026](https://www.bceao.int/sites/default/files/2026-10/AVIS%20N%C2%B0%200019%20%20DU%202%20OCTOBRE%202026%20%281%29.pdf)
- [OFFICIEL] Selon le communiqué, le seuil de 8 000 FCFA « couvre 75 % des transactions de monnaie électronique dans l'UEMOA ». — [communiqué du 2 oct. 2026](https://www.bceao.int/sites/default/files/2026-10/Communiqu%C3%A9%20du%202%20octobre%202026.pdf)
- [OFFICIEL] Retours de fonds, demandes de paiement et demandes d'annulation gratuits ; envoi transfrontalier facturable selon le participant (jusqu'au 1er juin 2027) ; réception pour clients C et autres services librement tarifés. — [FAQ Frais](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=3)
- [OFFICIEL-HÉBERGÉ-TIERS] Règles initiales (document « BCEAO-PI-TARIFICATION » v1.0.0 du 20/06/2024, marqué « réservé à l'usage exclusif des participants ») : via l'application mobile, paiement et transfert national gratuits à l'émission pour les personnes physiques ; en réception, gratuité jusqu'à 30 transferts nationaux par mois puis frais plafonnés à 1 % ; recherche d'alias gratuite. Ces règles sont antérieures à l'Avis n°0019 et en partie remplacées. — [copie hébergée par MicroSave, mise en ligne 4 nov. 2024](https://www.microsave.net/fr/wp-content/uploads/2024/11/Tarification-des-services-interope%CC%81rables.pdf)

**Marque**
- [OFFICIEL] Nom complet « Plateforme Interopérable du Système de Paiement Instantané », sigle PI-SPI, nom d'usage « PI » / « Pi » ; slogan affiché « PI c'est pour tout le monde, surtout pour moi » ; logo octogonal. — [pispi.bceao.int](https://pispi.bceao.int) et [pispi.bceao.int/lalias](https://pispi.bceao.int/lalias)

**Description indépendante**
- [SECONDAIRE] SIIPS 2025 (AfricaNenda) : le système régional UEMOA était « in the pilot phase with 90 participants » (1re cohorte de 25 institutions, 2e cohorte de 65 en août 2024, dont 9 EME et 14 institutions de microfinance) ; le lancement de septembre 2025 étant hors période de collecte, il n'est pas compté comme « live » dans cette édition. — [AfricaNenda, SIIPS 2025 main report (PDF)](https://www.africanenda.org/uploads/files/siips2025/SIIPS2025-mainreport_en.pdf)

### Inferences
- Pour le pitch, dire « traité en moins de 10 secondes (promesse publique) dans une enveloppe technique maximale de 20 secondes » ; un service de scoring doit donc répondre en quelques centaines de millisecondes pour rester invisible.
- Le passage de 80 à 175 participants entre juin et fin septembre 2026 montre que beaucoup d'établissements viennent juste d'ouvrir le service : leurs dispositifs anti-fraude « instantanés » sont récents.

### Gaps
- Aucun plafond de montant par transaction PI-SPI trouvé dans une source officielle. Un site commercial (Cauris) avance « jusqu'à 100 millions FCFA entre entreprises et 5 millions vers un particulier » sans citer de texte : [cauris.ci/guide/faq](https://cauris.ci/guide/faq/) — non vérifié, à ne pas utiliser.
- Plafonds de monnaie électronique : la BCEAO a pris l'Instruction n°020 du 8 octobre 2026 modifiant l'Instruction n°008-05-2015 (page officielle vue : [bceao.int](https://www.bceao.int/fr/reglementations/instruction-ndeg-020-portant-modification-de-linstruction-ndeg-008-05-2015-du-21)), mais je n'ai pas lu le PDF. Les montants (avoirs 4 millions FCFA, rechargements mensuels 15 millions FCFA, entrée en vigueur 2 nov. 2026) ne viennent que d'une source secondaire : [doingbuzz.com, 21 oct. 2026, corrigé le 29 oct.](https://doingbuzz.com/pi-spi-plafonds-2-millions-10-millions-fcfa/). Ce sont des plafonds de solde et de rechargement, pas des plafonds de transfert PI-SPI.
- La Convention de participation à PI-SPI et les règles de fonctionnement du système ne sont pas publiques (non trouvées).
- Le Rapport annuel 2025 de la BCEAO contient un encadré 3 sur PI-SPI ([PDF](https://www.bceao.int/sites/default/files/2026-07/Rapport_Annuel_2025_BCEAO_vf.pdf)) ; l'extraction de texte était trop désordonnée (mise en page multi-colonnes) pour en tirer des chiffres fiables.

---

## 2. L'affirmation de l'équipe : « Depuis le 2 novembre 2026, les transactions de monnaie électronique entre établissements différents doivent passer par PI-SPI »

### Takeaway
L'affirmation est CONFIRMÉE sur la date et sur le fond : c'est l'Avis n°0019 du Gouverneur de la BCEAO, signé à Dakar le 2 octobre 2026 et entré en vigueur le 2 novembre 2026. La formulation exacte porte sur les « transactions de monnaie électronique interopérables au sein de l'UEMOA », et le champ d'application de l'avis est limité aux transferts entre personnes physiques. Il s'agit bien d'une obligation d'acheminement, distincte de l'obligation de connexion (échéance du 30 septembre 2026).

### Cited Findings
- [OFFICIEL] Titre et date : « Avis N°0019 relatif aux transactions de monnaie électronique entre personnes physiques par l'intermédiaire de la PI-SPI de l'UEMOA », daté du 02 octobre 2026, adressé aux établissements de crédit, EME, établissements de paiement et institutions de microfinance soumises au contrôle de la Commission Bancaire. — [page BCEAO de l'Avis n°0019](https://www.bceao.int/fr/reglementations/avis-ndeg0019-relatif-aux-transactions-de-monnaie-electronique-entre-personnes)
- [OFFICIEL] Texte exact (OCR du PDF de 2 pages) :
  - Point 1, champ d'application : « Le présent Avis s'applique aux transferts de monnaie électronique entre personnes physiques, tels que définis par la Convention de participation à PI-SPI, au plan national et à l'échelle de l'UEMOA et entre toutes les catégories de participants. »
  - Point 2 : « Toutes les transactions de monnaie électronique interopérables, au sein de l'UEMOA, sont obligatoirement réalisées par l'intermédiaire de PI-SPI. »
  - Point 3 : tarification (8 000 FCFA cumulés par jour gratuits à l'émission ; 0 à 0,8 % au-delà ; réception gratuite).
  - Point 4 : égalité tarifaire nationale / intra-UEMOA « à partir du 1er juin 2027 ».
  - Point 6 : « Le présent Avis entre en vigueur le 2 novembre 2026 ». « Fait à Dakar, le 2 octobre 2026 », signé Jean-Claude Kassi BROU.
  — [PDF de l'Avis n°0019](https://www.bceao.int/sites/default/files/2026-10/AVIS%20N%C2%B0%200019%20%20DU%202%20OCTOBRE%202026%20%281%29.pdf)
- [OFFICIEL] Le communiqué du même jour reprend : « à compter du 2 novembre 2026 : 1. Les transactions de monnaie électronique interopérables au sein de l'UEMOA sont obligatoirement réalisées par l'intermédiaire de la Plateforme interopérable PI-SPI ». Il précise le périmètre : transferts « entre un compte détenu dans les livres d'une banque ou d'une institution de microfinance et […] un compte ouvert auprès d'un établissement de monnaie électronique ou d'un établissement de paiement », ainsi que « les transferts réalisés entre les établissements de monnaie électronique et les établissements de paiement ». Objectif affiché : « asseoir PI-SPI comme infrastructure centrale pour les paiements instantanés dans l'UEMOA ». — [communiqué BCEAO du 2 oct. 2026](https://www.bceao.int/sites/default/files/2026-10/Communiqu%C3%A9%20du%202%20octobre%202026.pdf)
- [OFFICIEL] Obligation de connexion (texte distinct, antérieur) : le communiqué du 2 avril 2026 demande aux banques, EME, établissements de paiement et institutions de microfinance supervisées par la Commission Bancaire d'être connectés et d'assurer un service effectif « au plus tard, le 30 juin 2026 ». — [communiqué du 2 avril 2026](https://www.bceao.int/sites/default/files/2026-04/Communiqu%C3%A9_Connexion_%C3%A0_PI-SPI_2_avril_2026.pdf)
- [OFFICIEL] Prolongation : nouvelles échéances d'ouverture effective des services = 30 septembre 2026 pour banques, EME et établissements de paiement ; 30 juin 2027 pour les institutions de microfinance supervisées par la Commission Bancaire. — [BCEAO, prolongation du délai, 25 juin 2026](https://www.bceao.int/fr/communique-presse/prolongation-du-delai-de-connexion-a-pi-spi)
- [SECONDAIRE] Reprise presse le jour J : « Les transferts de monnaie électronique dans l'espace UEMOA doivent désormais passer [par] la PI-SPI […] dès ce lundi 2 novembre 2026 ». — [Banouto, 2 nov. 2026](https://banouto.bj/economie/article/20261102-pi-spi-de-la-bceao-ce-qui-change-des-le-2-novembre-dans-les-tranferts-de-monnaie-electronique)
- [SECONDAIRE] Chronologie des échéances confirmée par la presse (30 juin 2026 puis report). — [Agence Ecofin, 24 juil. 2026](https://www.agenceecofin.com/actualites-finance/2407-140469-pi-spi-30-millions-de-personnes-connectees-et-190-millions-de-transactions-en-moins-dun-an)

### Inferences
- Formulation sûre pour le pitch : « Depuis le 2 novembre 2026 (Avis BCEAO n°0019 du 2 octobre 2026), toutes les transactions de monnaie électronique interopérables dans l'UEMOA passent obligatoirement par PI-SPI. » Éviter « tous les virements » : l'avis vise la monnaie électronique entre personnes physiques.
- Le mot du texte est « interopérables », pas « entre établissements différents » ; le communiqué montre que cela recouvre banque/SFD vers EME/EP et EME vers EP. Les virements banque à banque ne sont pas visés par cet avis (lecture du périmètre, non confirmée par un texte explicite).
- L'instrument est un « Avis » et non une « Instruction » : ne pas écrire « instruction n°0019 ».
- Les SFD ont jusqu'au 30 juin 2027 pour ouvrir le service : la couverture n'est pas encore totale côté microfinance.

### Gaps
- L'en-tête « AVIS N° 0019 » n'est pas sorti à l'OCR (tampon/en-tête) ; le numéro provient du titre de la page BCEAO et du nom du fichier PDF.
- Sanctions en cas de non-respect : rien dans l'avis ni dans les communiqués lus. Un article de cabinet d'avocats évoque « sanctions pécuniaires ou suspension d'agrément » sans citer d'article : [Legal 500](https://www.legal500.com/intelligence/senegal/finance-and-banking/j-21-interop%C3%A9rabilit%C3%A9-pi-spi-dans-l%E2%80%99uemoa-%C3%8Ates-vous-en-conformit%C3%A9-avant-le-30-juin-2026) — non vérifié.
- La « Convention de participation à PI-SPI », qui définit les « transferts de monnaie électronique entre personnes physiques », n'est pas publique.

---

## 3. Irrévocabilité : quel texte, quels mots

### Takeaway
L'irrévocabilité est affirmée noir sur blanc par la BCEAO pour PI-SPI (« Une fois confirmée, l'opération d'envoi est irrévocable ») et repose en droit sur l'article 75 de l'Instruction n°001-01-2024 et sur l'article 6 du Règlement n°15/2002/CM/UEMOA, qui renvoie aux règles de fonctionnement du système pour fixer le moment d'irrévocabilité. Les règles de fonctionnement propres à PI-SPI ne sont pas publiques.

### Cited Findings
- [OFFICIEL] FAQ grand public : « Et si je me trompe ? Puis-je annuler un envoi ? Non. Une fois confirmée, l'opération d'envoi est irrévocable. Il n'est plus possible pour l'établissement teneur de votre compte de l'annuler. Vous pouvez toutefois envoyer une demande d'annulation au bénéficiaire. » — [FAQ Transferts, consultée 2026-11-19](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=5)
- [OFFICIEL] Portail développeurs, « choix structurants » : « Principe d'irrévocabilité des transactions — Une fois confirmée par le client payeur et traitée par PI-SPI, l'opération est irrévocable : elle ne peut plus être annulée ni modifiée unilatéralement ». — [guide « Vue d'ensemble »](https://developer.pispi.bceao.int/guides/vue-ensemble)
- [OFFICIEL] L'API Business expose un statut `IRREVOCABLE` et un filtre `dateIrrevocabilite` sur les paiements. — [API Business, introduction, consultée 2026-11-19](https://developer.pispi.bceao.int/api-business)
- [OFFICIEL] Instruction n°001-01-2024 relative aux services de paiement dans l'UMOA, article 75 « Irrévocabilité d'un ordre de paiement » : « Un ordre de paiement ne peut pas être révoqué dans les cas suivants : 1. lorsqu'il a été reçu par le prestataire de services de paiement du payeur ; 2. dans le cadre d'une opération de paiement initiée par ou via le bénéficiaire, lorsque le payeur a transmis l'ordre de paiement au bénéficiaire ou a donné son consentement […] ; 3. […] initiée par un prestataire de services d'initiation de paiement, lorsque le payeur a donné son consentement ». Article 76 : exceptions limitées au prélèvement automatique et aux ordres à exécution différée (révocables jusqu'à la fin du jour ouvrable précédent). — [BCEAO, Instruction n°001-01-2024 (PDF, 44 pages)](https://www.bceao.int/sites/default/files/inline-files/Instruction-No001-01-2024_relative_aux_services_de_paiement_dans_l-UMOA.pdf)
- [OFFICIEL] Règlement n°15/2002/CM/UEMOA, article 6 : les ordres de transfert introduits dans un système de paiement interbancaire conformément à ses règles « sont opposables aux tiers et à la masse et ne peuvent être annulés » ; « Le moment auquel un ordre de transfert devient irrévocable dans le système est défini par les règles de fonctionnement dudit système. » Article 142 : « L'ordre ou l'engagement de paiement donné au moyen d'une carte ou d'un autre instrument et procédé électronique de paiement est irrévocable », avec opposition possible en cas de perte, vol ou utilisation frauduleuse de la carte ou du porte-monnaie. — [BCEAO, Règlement n°15/2002/CM/UEMOA (PDF)](https://www.bceao.int/sites/default/files/inline-files/Reglement_n_15_2002_CM_UEMOA_relatif_aux_systemes_de_paiement_dans_les_Etats_membres_de_l_UEMOA.pdf)
- [OFFICIEL-HÉBERGÉ-TIERS] Présentation BCEAO au séminaire FRATEL (Lomé, 21-22 mai 2024) : fonctionnalité principale « Paiement instantané et irrévocable ». — [fratel.org, PDF mis en ligne 22 mai 2024](https://www.fratel.org/documents/2024/05/14.-TR3-BCEAO.pdf)

### Inferences
- Argument central du pitch : comme l'établissement du payeur ne peut plus annuler après confirmation, la seule fenêtre de prévention de la fraude est AVANT la confirmation du client ; après, tout dépend de la bonne volonté du bénéficiaire (voir section 4).

### Gaps
- Date de signature de l'Instruction n°001-01-2024 : le champ date est vide dans le texte extrait du PDF (fichier mis en ligne le 25 nov. 2024 ; la numérotation indique janvier 2024). À vérifier sur l'original avant de citer un jour précis.
- Numérotation des articles du Règlement 15/2002 (6 et 142) relevée par repérage de l'intitulé d'article précédant le passage dans le texte extrait ; à recontrôler sur le PDF si l'article est cité dans une diapositive.
- Je n'ai pas vérifié si le Règlement 15/2002 a été remplacé par un nouveau règlement sur les systèmes de paiement (l'Instruction 001-01-2024 vise « le Règlement relatif aux systèmes de paiement » sans numéro).

---

## 4. Fraude et erreurs : recours du client, obligations des participants

### Takeaway
Dans PI-SPI, le seul recours « système » du payeur est la demande d'annulation, qui n'aboutit que si le bénéficiaire l'accepte ; un fraudeur ne l'acceptera pas. Le droit commun des services de paiement impose en revanche aux prestataires l'authentification forte avec lien dynamique, la prévention de la fraude, le remboursement immédiat des opérations non autorisées et un traitement des réclamations en 7 jours ouvrables, mais ce régime protège mal la victime d'une arnaque qui a elle-même validé le transfert.

### Cited Findings

**Mécanismes PI-SPI après un envoi**
- [OFFICIEL] Demande d'annulation : envoyée par le payeur au payé après un envoi irrévocable ; cas d'usage listés : erreur de destinataire, erreur de montant, double paiement, produit non livré, « suspicion ou confirmation de fraude » ; « Le Payé doit obligatoirement valider pour que l'annulation soit effective […] Sans cette validation, aucun retour de fonds n'est effectué. » — [Portail développeurs, « Retours & annulations — vue d'ensemble », consulté 2026-11-19](https://developer.pispi.bceao.int/guides/retour-overview)
- [OFFICIEL] Retour de fonds : initié par le bénéficiaire, sans validation du payeur, exécution immédiate. Côté grand public : sélectionner la transaction reçue par erreur et choisir « retourner », sans frais. — [guide retours](https://developer.pispi.bceao.int/guides/retour-overview) et [FAQ Transferts](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=5)
- [OFFICIEL] Retours de fonds et demandes d'annulation sont gratuits. — [FAQ Frais](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=3)

**Garde-fous de conception imposés par la BCEAO**
- [OFFICIEL] Affichage du bénéficiaire avant validation : « l'application mobile affiche systématiquement les nom, prénom et pays du propriétaire de l'alias ou du QR Code » ; le payeur doit vérifier avant de confirmer, sinon annuler. — [FAQ Transferts](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=5)
- [OFFICIEL] « Double confirmation du destinataire — Lors d'un envoi de fonds, le payeur doit systématiquement valider l'identité du bénéficiaire avant l'exécution, afin d'éviter les erreurs et fraudes. » — [guide « Vue d'ensemble »](https://developer.pispi.bceao.int/guides/vue-ensemble)
- [OFFICIEL-HÉBERGÉ-TIERS] La recherche d'alias ou vérification d'identité (ACMT.023 / ACMT.024) est « obligatoire avant toute transaction ». — [BCEAO-PI-TARIFICATION v1.0.0, 20/06/2024](https://www.microsave.net/fr/wp-content/uploads/2024/11/Tarification-des-services-interope%CC%81rables.pdf)
- [OFFICIEL] Pas de prélèvement : « seuls les parcours de demande de paiement (RTP) sont autorisés lorsqu'une initiative vient du bénéficiaire ». — [guide « Vue d'ensemble »](https://developer.pispi.bceao.int/guides/vue-ensemble)
- [OFFICIEL] Demandes de paiement : « Pour réduire le risque de fraude, seules les demandes de paiement émises par vos contacts ou par une entreprise peuvent être acceptées. » — [FAQ Demande de paiement](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=4)
- [OFFICIEL] QR code interdit pour le paiement en ligne ou à distance (réservé au point de présence physique), « restriction [qui] vise à protéger les utilisateurs contre la fraude » ; mention « Site e-commerce vérifié » affichée pour les paiements en ligne par RTP. — [Centre d'aide développeurs](https://developer.pispi.bceao.int/centre-aide) et [FAQ Transferts](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=5)
- [OFFICIEL] Authentification préalable de l'utilisateur « (code PIN, mot de passe ou biométrie), selon les modalités de l'institution ». — [pispi.bceao.int accueil](https://pispi.bceao.int)

**Obligations générales des prestataires (Instruction n°001-01-2024)** — source unique pour toutes les puces ci-dessous : [Instruction n°001-01-2024 (PDF)](https://www.bceao.int/sites/default/files/inline-files/Instruction-No001-01-2024_relative_aux_services_de_paiement_dans_l-UMOA.pdf)
- [OFFICIEL] Art. 85 : authentification forte obligatoire quand le payeur accède à son compte en ligne, initie une opération de paiement électronique ou exécute une action à risque de fraude ; pour l'initiation d'un paiement, elle doit comprendre « des éléments qui établissent un lien dynamique entre l'opération, le montant et le bénéficiaire ». Définition (art. 3, point 5) : au moins deux des trois facteurs connaissance / possession / inhérence.
- [OFFICIEL] Art. 83 : le système d'information doit permettre « de prévenir […] les risques liés à la fraude moyennant des mesures organisationnelles et des outils de prévention appropriés » et « d'enregistrer et de traiter des opérations de paiement en temps réel » ; tests d'intrusion au moins annuels.
- [OFFICIEL] Art. 84 : notification sans délai de tout incident opérationnel majeur à la BCEAO et à la Commission Bancaire, rapport détaillé sous 72 heures.
- [OFFICIEL] Art. 67 : le client notifie une opération non autorisée ou mal exécutée « au plus tard dans les neuf (9) mois suivant la date de débit ».
- [OFFICIEL] Art. 68 : charge de la preuve sur le prestataire (opération authentifiée, enregistrée, sans défaillance technique) ; la seule utilisation de l'instrument ne prouve pas l'autorisation ; au prestataire de prouver la fraude ou la négligence grave du client.
- [OFFICIEL] Art. 69 : en cas d'opération non autorisée, le prestataire du payeur « doit rembourser immédiatement » le montant. Art. 70 : le payeur supporte les pertes s'il a agi frauduleusement ou manqué à ses obligations de l'art. 65.
- [OFFICIEL] Art. 51 (établissements de paiement) : dispositif interne de réclamation obligatoire ; réponse « au plus tard, dans les sept (7) jours ouvrables » ; à défaut, saisine de la Commission Bancaire ou médiation (Observatoire de la Qualité des Services Financiers du pays).
- [OFFICIEL] Art. 71-72 : droit au remboursement pour une opération initiée par le bénéficiaire, demande dans les 8 semaines, réponse du prestataire sous 10 jours ouvrés (peu pertinent pour PI-SPI, qui n'autorise pas le prélèvement).

### Inferences
- Trou de protection exploitable dans le pitch : l'arnaque par manipulation (le client valide lui-même, avec son PIN, un transfert vers un escroc) est une opération « autorisée » ; les articles 69-70 sur les opérations non autorisées ne garantissent donc pas de remboursement, et la demande d'annulation dépend de l'escroc. C'est une lecture juridique, non une affirmation de la BCEAO.
- L'article 83 (outils de prévention de la fraude, traitement temps réel) fournit l'accroche réglementaire d'un scoring pré-confirmation : c'est une obligation de moyens déjà à la charge de chaque participant.
- L'affichage du nom du bénéficiaire existe déjà dans PI-SPI ; un service de scoring doit donc se présenter comme complément (détection de comptes mules, comportements anormaux), pas comme « confirmation du bénéficiaire ».

### Gaps
- Aucun délai officiel trouvé pour la réponse du bénéficiaire à une demande d'annulation, ni de procédure d'arbitrage entre participants en cas de refus (les guides « Demander une annulation » et « Répondre à une annulation » du portail affichent « Contenu en cours de rédaction » : [guide](https://developer.pispi.bceao.int/guides/annulation-demander)).
- Aucune obligation explicite de surveillance des transactions ou de scoring propre à PI-SPI trouvée dans un texte public ; les exigences de sécurité imposées aux participants pour être admis ne sont pas publiées.
- L'article 51 vise les établissements de paiement ; je n'ai pas vérifié les textes équivalents pour banques, EME et SFD.
- Aucun dispositif BCEAO de traitement centralisé des réclamations des usagers de PI-SPI trouvé.

---

## 5. Recommandations de sécurité et sensibilisation du public

### Takeaway
La communication officielle de sécurité de PI-SPI est mince : la FAQ « Sécurité » renvoie essentiellement aux consignes des participants. Aucune campagne BCEAO spécifique contre les arnaques via PI-SPI n'a été trouvée.

### Cited Findings
- [OFFICIEL] « Comment éviter les fraudes liées à PI-SPI ? Pour éviter les fraudes, vous devez respecter les règles d'utilisation des services et suivre les recommandations et consignes diffusées par les participants teneurs de vos comptes. » — [FAQ Sécurité, consultée 2026-11-19](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=7)
- [OFFICIEL] « Il ne faut jamais scanner un QR Code sur un site e-commerce pour effectuer un paiement. » — [FAQ Sécurité](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=7)
- [OFFICIEL] Vérifier nom, prénom et pays affichés avant de confirmer ; sinon annuler. — [FAQ Transferts](https://pispi.bceao.int/foire-aux-questions?field_categorie_faq_target_id=5)
- [OFFICIEL] Arguments de sécurité affichés : « chiffrement AES-256 et surveillance continue 24/7 », « authentification renforcée ». Le site reconnaît que les paiements numériques de l'Union sont « souvent exposé[s] aux erreurs et à la fraude ». — [pispi.bceao.int/propos](https://pispi.bceao.int/propos) et [pispi.bceao.int](https://pispi.bceao.int)
- [OFFICIEL] Mise en garde générale (non spécifique à PI-SPI, non datée sur la page) contre les messages, sites et documents usurpant l'identité de la BCEAO pour extorquer de l'argent. — [BCEAO, « Attention aux messages frauduleux »](https://www.bceao.int/fr/communique-presse/attention-aux-messages-frauduleux-se-rapportant-la-bceao)
- [SECONDAIRE] Propos rapporté de la cheffe du projet PI-SPI (séminaire presse du 21 juillet 2026) : « Pour PI, la sécurité de connexion prime sur tout ». — [Agence Ecofin, 24 juil. 2026](https://www.agenceecofin.com/actualites-finance/2407-140469-pi-spi-30-millions-de-personnes-connectees-et-190-millions-de-transactions-en-moins-dun-an)

### Inferences
- La BCEAO délègue explicitement la prévention de la fraude côté client aux participants : c'est exactement l'endroit où se place un service de scoring vendu aux banques et fintechs.

### Gaps
- Aucune statistique officielle de fraude sur PI-SPI ou sur la monnaie électronique récente trouvée. Le rapport SFN 2024 ne contient qu'une occurrence du mot « fraude ». Des articles anciens (2021, 2023) évoquent des chiffres de fraude sur la monnaie électronique mais n'ont pas été ouverts : ne pas les citer.
- Aucun guide de sécurité BCEAO destiné aux participants PI-SPI n'est public.

---

## 6. Format des messages, API, et où loger un score de risque

### Takeaway
PI-SPI repose sur ISO 20022 entre participants et plateforme (officiel), avec les messages pacs.008, pacs.002, pacs.004, pacs.028, pain.013/014, camt.056/029 et acmt.023/024 nommés dans un document tarifaire BCEAO de 2024. Les spécifications détaillées de l'interface participant ne sont pas publiques ; seule l'API Business (participant vers client entreprise) est documentée. Aucun champ « score de risque » n'a été trouvé.

### Cited Findings
- [OFFICIEL] « Norme ISO 20022 comme langage commun — Toutes les interactions entre les participants et PI-SPI s'appuient sur ce standard international ». Architecture en étoile (« hub-and-spoke ») : chaque participant se connecte une seule fois au hub de la BCEAO. — [guide « Vue d'ensemble »](https://developer.pispi.bceao.int/guides/vue-ensemble)
- [OFFICIEL-HÉBERGÉ-TIERS] Messages nommés par la BCEAO : PACS.008 (émission/réception de transferts et paiements, avec notion de « PACS.008 confirmé irrévocable »), PACS.002, PACS.004 (retour de fonds), PACS.028, PAIN.013 et PAIN.014 (demande de paiement et réponse), CAMT.056 et CAMT.029 (demande de remboursement et réponse), ACMT.023 et ACMT.024 (recherche d'alias / vérification d'identité), familles ADMI et REDA. Le document renvoie à des spécifications « BCEAO-PI-SPI-SPECS-MESSAGES-GENERAL » et « BCEAO-PI-RAC ». — [BCEAO-PI-TARIFICATION v1.0.0 du 20/06/2024, copie MicroSave](https://www.microsave.net/fr/wp-content/uploads/2024/11/Tarification-des-services-interope%CC%81rables.pdf)
- [OFFICIEL-HÉBERGÉ-TIERS] Caractéristiques présentées par la BCEAO en mai 2024 : format ISO 20022, disponibilité 24*7*365, alias de types MBNO, SHID, MCOD, QR statique/dynamique, infrastructure PKI pour participants et clients business. — [présentation FRATEL, mai 2024](https://www.fratel.org/documents/2024/05/14.-TR3-BCEAO.pdf)
- [OFFICIEL] Rôle de la plateforme dans un flux : « valide les signatures et contrôles fonctionnels », « route les messages entre participants », « gère le Répertoire des Alias Centralisé (RAC) ». Le participant génère l'`EndToEndId` au moment de la recherche d'alias. — [guide RTP](https://developer.pispi.bceao.int/guides/rtp-overview) et [guide paiements](https://developer.pispi.bceao.int/guides/paiements-overview)
- [OFFICIEL] API Business : interface standardisée que chaque participant doit exposer à ses clients entreprises (type B) ; fonctions : alias, réception/envoi/retour de paiements, paiements en masse, demandes d'annulation, demandes de paiement, consultation d'opérations ; erreurs au format RFC 7807 ; sécurité OAuth 2.0 et mTLS ; webhooks (ex. événements `PAIEMENT_REJETE`, `RTP_REJETE`) ; sandbox public. — [API Business](https://developer.pispi.bceao.int/api-business), [guide sécurité](https://developer.pispi.bceao.int/guides/securite-overview), [guide webhooks](https://developer.pispi.bceao.int/guides/webhooks-overview)
- [OFFICIEL] La BCEAO homologue les API Business des participants et publie la liste (mise à jour au 9 novembre 2026 annoncée sur bceao.int). — [BCEAO, liste des API Business homologuées au 9 nov. 2026](https://www.bceao.int/fr/communique-presse/liste-actualisee-des-api-business-pi-spi-homologuees-par-la-bceao-au-9-11-2026)
- [OFFICIEL] Les exemples de retour de fonds de l'API utilisent un champ `motif` avec des codes de type ISO (`AM04`, `CUST`). — [guide « Retourner les fonds »](https://developer.pispi.bceao.int/guides/retour-envoyer)
- [SECONDAIRE] Un intégrateur décrit le raccordement comme « un dialogue ISO 20022 bidirectionnel » via un middleware qui émet et reçoit : pacs.008/pacs.002, pain.013/pain.014, acmt.023/acmt.024, camt.056/camt.029, pacs.004 ; il insiste sur le risque de timeout. — [post LinkedIn, 14 août 2026](https://fr.linkedin.com/posts/a-dera_banques-eme-pispi-activity-7493999784878546944-lvk6)
- [SECONDAIRE] Autre description : les participants passent par une « AIP (Application d'Interfaçage Participant) » ; pacs.002 = confirmation d'irrévocabilité ; statuts ACTC / ACCP / RJCT. — [post LinkedIn, 24 mai 2026](https://fr.linkedin.com/posts/malick-gueye-a6a16852_pispi-bceao-uemoa-activity-7464422711528927232-VPvU)

### Inferences
- Point d'insertion naturel du scoring (déduction, non documentée par la BCEAO) : dans le système du participant payeur, entre la réponse à la recherche d'alias (nom, pays, participant du bénéficiaire connus) et l'émission du pacs.008, c'est-à-dire pendant l'écran de confirmation. Le score reste interne au participant ; rien n'indique qu'il puisse ou doive être transporté dans le message.
- Côté participant payé, un second point d'insertion existe à la réception du pacs.008 (accepter ou rejeter), mais dans une enveloppe de 20 secondes au total.
- La standardisation ISO 20022 est un argument de vente : un même connecteur de scoring est réutilisable chez les 175 participants.

### Gaps
- Spécifications ISO 20022 détaillées de PI-SPI (profils, XSD, champs) non publiques : le site référencé [pi-bceao.com/publications](https://pi-bceao.com/publications) a renvoyé une page vide à l'extraction (probablement réservée aux participants).
- Aucun champ ni mécanisme prévu pour un score de risque ou un signalement de fraude entre participants n'a été trouvé (ni dans l'API Business, ni ailleurs). Ne pas affirmer qu'il en existe un.
- La page « Directives BCEAO » du portail développeurs affiche « Bientôt disponible » : [developer.pispi.bceao.int/directives](https://developer.pispi.bceao.int/directives).
- La liste nominative des messages vient d'un document de juin 2024 (avant lancement) et de posts LinkedIn ; elle a pu évoluer.

---

## 7. Statistiques clés

### Takeaway
Dernière édition du rapport BCEAO sur les services financiers numériques : année 2024 (daté janvier 2026, publié en mars 2026) : 248,7 millions de comptes de monnaie électronique, 76,9 millions actifs, 160 415 milliards FCFA de transactions. Pour PI-SPI lui-même, le seul bilan chiffré trouvé est rapporté par la presse : environ 1 million de transactions et 110 milliards FCFA au 20 juillet 2026, soit un usage encore très faible avant l'obligation du 2 novembre 2026.

### Cited Findings

**Monnaie électronique UEMOA, année 2024** — source unique : [BCEAO, Rapport annuel sur l'évolution des services financiers numériques dans l'UEMOA, année 2024 (PDF, daté janvier 2026, mis en ligne 13 mars 2026)](https://www.bceao.int/sites/default/files/2026-03/Rapport%20annuel%20sur%20les%20services%20financiers%20num%C3%A9riques%20dans%20l'UEMOA%20-%202024.pdf) ; page de présentation : [bceao.int](https://www.bceao.int/fr/publications/rapport-annuel-sur-les-services-financiers-numeriques-dans-luemoa-2024)
- [OFFICIEL] Comptes de monnaie électronique ouverts : 248 710 918 en 2024 contre 209 025 380 en 2023 (+18,99 %) ; 70,88 % détenus par les EME, 28,36 % par les banques.
- [OFFICIEL] Comptes actifs (au moins une transaction en 90 jours) : 76 863 533 (+11,62 %) ; taux d'activité 30,9 %.
- [OFFICIEL] Transactions 2024 : valeur 160 415 milliards FCFA ; volume 11 921 750 329 selon le tableau annexe (le texte dit « 11 milliards ») ; +27 % en volume ; valeur = 118,94 % du PIB de l'Union ; valeur moyenne journalière 436 milliards FCFA selon le texte (445,60 selon le tableau annexe).
- [OFFICIEL] Transferts de personne à personne : 2 346 903 141 opérations pour 42 763 milliards FCFA (+44 % en volume, +31 % en valeur) ; montant moyen d'un transfert 18 220 FCFA.
- [OFFICIEL] Paiements : 5 378 672 826 opérations pour 15 424 milliards FCFA ; paiements marchands environ 1,2 milliard d'opérations.
- [OFFICIEL] Transactions intra-UEMOA : 102 millions d'opérations, 5 661 milliards FCFA (+33,46 % en valeur).
- [OFFICIEL] Parts de marché des comptes ouverts 2024 : Orange 23 %, Wave 22,1 %, Moov 18,4 %, MTN 16,6 %, YAS 5,1 %.
- [OFFICIEL] Répartition par pays des comptes ouverts : Côte d'Ivoire 99 649 204 (40,07 %), Sénégal 42 579 300 (17,12 %), Bénin 37 524 005 (15,09 %), Burkina Faso 23 708 070, Mali 18 129 935, Togo 12 553 441, Niger 9 746 822, Guinée-Bissau 4 820 141.
- [OFFICIEL] Environ 88 % des dépôts sur comptes de monnaie électronique sont retirés en espèces ; ratio de digitalisation nette 7,52 %.

**PI-SPI depuis le lancement**
- [OFFICIEL] 175 participants connectés et plus de 38 millions de personnes ayant accès aux services au 2 octobre 2026. — [communiqué BCEAO du 2 oct. 2026](https://www.bceao.int/sites/default/files/2026-10/Communiqu%C3%A9%20du%202%20octobre%202026.pdf)
- [SECONDAIRE] Au 20 juillet 2026 (bilan présenté par la BCEAO lors de la présentation de son rapport annuel 2025) : 30 millions de personnes connectées, 1 million de transactions, 110 milliards FCFA échangés (environ 190 millions USD). — [Agence Ecofin, 24 juil. 2026](https://www.agenceecofin.com/actualites-finance/2407-140469-pi-spi-30-millions-de-personnes-connectees-et-190-millions-de-transactions-en-moins-dun-an) ; concordant avec [Financial Afrik, 23 juil. 2026](https://www.financialafrik.com/2026/07/23/bceao-pi-spi-franchit-le-cap-des-30-millions-dutilisateurs-et-accelere-linclusion-financiere-dans-luemoa/)
- [SECONDAIRE] Ces 30 millions représentent « près de 40 % de la population adulte de l'Union, estimée entre 75 et 80 millions » et correspondent à la clientèle des établissements raccordés (population joignable), pas à des utilisateurs actifs. — [Agence Ecofin, 24 juil. 2026](https://www.agenceecofin.com/actualites-finance/2407-140469-pi-spi-30-millions-de-personnes-connectees-et-190-millions-de-transactions-en-moins-dun-an)
- [OFFICIEL] Objectif affiché : inclusion financière d'au moins 90 % de la population adulte de l'UEMOA à l'horizon 2030. — [pispi.bceao.int/propos](https://pispi.bceao.int/propos)
- [OFFICIEL-HÉBERGÉ-TIERS] Repère fin 2023 (présentation BCEAO) : plus de 193 millions de comptes de monnaie électronique, 10,5 milliards de transactions pour 130 041 milliards FCFA. — [présentation FRATEL, mai 2024](https://www.fratel.org/documents/2024/05/14.-TR3-BCEAO.pdf)

### Inferences
- Ordre de grandeur utile : environ 1 million de transactions PI-SPI en près de 10 mois, contre plus de 2,3 milliards de transferts P2P de monnaie électronique par an. L'obligation du 2 novembre 2026 devrait faire basculer vers PI-SPI la part interopérable de ces flux ; le volume exposé au risque « instantané et irrévocable » change d'échelle. La part exacte concernée n'est publiée nulle part.
- « 38 millions de personnes » = personnes ayant accès (clients des participants connectés), à ne pas présenter comme « utilisateurs actifs ».

### Gaps
- Aucune statistique officielle de volume PI-SPI postérieure au 20 juillet 2026, et aucune depuis l'entrée en vigueur du 2 novembre 2026.
- Pas d'édition 2025 du rapport sur les services financiers numériques trouvée ; l'édition 2024 est la plus récente identifiée.
- Le rapport 2024 présente de petites incohérences internes (11 milliards contre 11,9 milliards d'opérations ; 436 contre 445,6 milliards par jour ; une phrase écrit « 12 milliards FCFA à 15 milliards FCFA » pour la valeur des paiements alors que le tableau donne 12 759 et 15 424 milliards) : citer les chiffres du tableau annexe.
- Aucune statistique de fraude (nombre de cas, montants) propre à PI-SPI ou récente pour la monnaie électronique UEMOA.
