# Scénarios de fraude à injecter dans les données

Rédigé le 19 novembre 2026. Notes détaillées et sources complètes :
`research_notes/Sentinelle ressources GPU Challenge/arnaques_partenaires.md`.

## Comment lire ce document

Chaque scénario part d'une arnaque documentée au Bénin ou dans l'UEMOA, puis la traduit en
suite de transactions à ajouter aux données simulées.

Deux niveaux de certitude, à ne pas mélanger :

- **Documenté** : le déroulé de l'arnaque côté victime, tiré d'une alerte officielle ou d'une
  affaire jugée. La source est citée.
- **Hypothèse de simulation** : tout ce qui se passe après (nombre de mules, délais de retrait,
  montants exacts). Aucune source consultée ne chiffre le délai entre la fraude et le retrait
  en espèces au Bénin. Ces paramètres sont nos choix, à annoncer comme tels au jury.

Format des transactions (calqué sur PaySim, voir `docs/ressources.md`) :

| Champ | Sens |
|---|---|
| `t` | Moment de la transaction, en minutes depuis le début du scénario |
| `type` | `TRANSFER` (transfert entre comptes) ou `CASH_OUT` (retrait en espèces chez un agent) |
| `de` → `vers` | Compte débité → compte crédité |
| `montant` | En FCFA |
| `fraude` | 1 si la transaction fait partie de l'arnaque, 0 sinon |

Rôles des comptes : `V` = victime, `M` = mule (compte complice), `A` = agent de retrait,
`N` = client normal.

Point technique : dans PaySim, le temps avance par pas d'une heure. Nos scénarios se jouent en
minutes. Le script d'injection devra donc ajouter une colonne d'horodatage plus fine que la
colonne `step` de PaySim.

Repère de montant : un transfert de personne à personne vaut en moyenne 18 220 FCFA dans
l'UEMOA en 2024 ([rapport BCEAO](https://www.bceao.int/sites/default/files/2026-03/Rapport%20annuel%20sur%20les%20services%20financiers%20num%C3%A9riques%20dans%20l'UEMOA%20-%202024.pdf)).

---

## Scénario 1 — Le « transfert par erreur »

**Documenté.** Un inconnu appelle et dit avoir envoyé de l'argent par erreur. La victime voit un
faux SMS de dépôt, envoyé depuis un numéro ordinaire, pour un montant proche de son solde.
L'escroc lui demande de « rembourser ». La victime fait elle-même le transfert.

- Alerte de l'OCRC, avec un exemple de faux SMS de 830 100 FCFA : [Bénin Web TV, 6 décembre 2019](https://archives.beninwebtv.bj/2019/12/benin-locrc-lance-une-alerte-contre-larnaque-via-les-services-mobile-money/)
- Alerte du CNIN : [Dadjè Infos, 27 décembre 2024](https://www.dadje.info/2024/12/27/benin-ce-quil-faut-savoir-sur-les-arnaques-aux-transferts-mobiles-selon-le-cnin/)
- Fiche du gouvernement béninois : [pare.gouv.bj](https://www.pare.gouv.bj/pages/13/les-transferts-frauduleux)

C'est le scénario de la démo : la victime valide elle-même, donc seule une alerte avant
validation peut l'arrêter.

**Transactions à injecter** (hypothèse de simulation pour les lignes 2 à 4) :

| t | type | de → vers | montant | fraude |
|---|---|---|---|---|
| 0 | TRANSFER | V1 → M1 | 180 000 | 1 |
| 6 | TRANSFER | M1 → M2 | 100 000 | 1 |
| 9 | CASH_OUT | M1 → A1 | 78 000 | 1 |
| 15 | CASH_OUT | M2 → A2 | 98 000 | 1 |

Paramètres à faire varier : montant entre 60 % et 95 % du solde de la victime ; M1 créé depuis
moins de 15 jours ; V1 n'a jamais envoyé d'argent à M1.

**Signaux attendus sur le destinataire M1** : compte récent, premier contact avec l'expéditeur,
montant très supérieur aux habitudes de V1, fonds ressortis en quelques minutes.

---

## Scénario 2 — Le faux agent du service client

**Documenté.** L'appelant se présente comme agent de l'opérateur. Il cite le vrai nom de la
victime, annonce une « mise à jour du numéro Mobile Money » à faire le jour même sous peine de
blocage, puis demande le code de validation reçu par SMS. Avec ce code, il opère sur le compte.

- Alerte du CNIN : [L'Investigateur, 12 novembre 2026](https://linvestigateur.info/benin-le-cnin-alerte-sur-une-nouvelle-arnaque-au-mobile-money/)
- Même schéma au Sénégal avec de faux agents Sonatel, dont un envoi de 750 000 FCFA : [Senenews, 26 août 2025](https://www.senenews.com/actualites/kaolack-comment-la-br-a-coince-le-reseau-descrocs-qui-se-faisait-passer-pour-des-agents-de-la-sonatel_556926.html)

Différence avec le scénario 1 : ici c'est le fraudeur qui lance les transferts depuis le compte
de la victime. Il vide le compte en plusieurs fois, vers plusieurs mules.

**Transactions à injecter** (hypothèse de simulation) :

| t | type | de → vers | montant | fraude |
|---|---|---|---|---|
| 0 | TRANSFER | V2 → M3 | 200 000 | 1 |
| 2 | TRANSFER | V2 → M4 | 200 000 | 1 |
| 4 | TRANSFER | V2 → M3 | 145 000 | 1 |
| 10 | CASH_OUT | M3 → A1 | 340 000 | 1 |
| 12 | CASH_OUT | M4 → A3 | 197 000 | 1 |

Paramètres à faire varier : 2 à 5 transferts en moins de 10 minutes ; total proche du solde
complet ; heure inhabituelle pour V2.

**Signaux attendus** : rafale de transferts depuis un compte habituellement calme, solde vidé,
destinataires jamais vus, retraits rapides.

---

## Scénario 3 — Le compte collecteur

**Documenté.** Les enquêtes décrivent des « intermédiaires chargés des retraits de fonds » et un
approvisionnement massif en cartes SIM enregistrées sous de fausses identités.

- Bilan 2025 du CNIN : [La Nouvelle Tribune, 15 janvier 2026](https://lanouvelletribune.info/2026/01/benin-1-500-interpellations-liees-a-la-cybercriminalite-en-2025/)
- Environ 19 000 SIM et 1 000 fausses pièces d'identité saisies à Hèvié : [Le Potentiel, 18 octobre 2026](https://lepotentiel.bj/?p=89196)
- SIM vendues avec compte Mobile Money déjà configuré, 2 000 à 2 500 FCFA pièce : [NetAfrique, 7 septembre 2026](https://netafrique.net/trafic-de-cartes-sim-pre-activees-la-bclcc-demantele-un-reseau-frauduleux-entre-le-burkina-et-le-benin/)

Un même compte mule reçoit l'argent de plusieurs victimes sur une courte période, puis le fait
sortir. C'est le scénario qui exerce le signal « nombre d'expéditeurs nouveaux ».

**Transactions à injecter** (hypothèse de simulation) :

| t | type | de → vers | montant | fraude |
|---|---|---|---|---|
| 0 | TRANSFER | V3 → M5 | 45 000 | 1 |
| 40 | TRANSFER | V4 → M5 | 120 000 | 1 |
| 95 | TRANSFER | V5 → M5 | 30 000 | 1 |
| 100 | CASH_OUT | M5 → A2 | 190 000 | 1 |
| 180 | TRANSFER | V6 → M5 | 250 000 | 1 |
| 185 | TRANSFER | M5 → M6 | 250 000 | 1 |
| 200 | CASH_OUT | M6 → A4 | 248 000 | 1 |

Paramètres à faire varier : 4 à 12 victimes en 24 à 72 heures ; aucune victime ne connaît les
autres ; M5 ne garde presque jamais de solde.

**Signaux attendus sur M5** : beaucoup d'expéditeurs nouveaux en peu de temps, rapport
entrées/sorties proche de 1, solde résiduel quasi nul.

---

## Scénario 4 — La chaîne de mules

**Documenté.** Le CNIN décrit des réseaux à plusieurs étages, des auteurs directs aux relais de
retrait puis aux responsables. Un « relais » a été poursuivi à la CRIET pour avoir retiré
l'argent de cybercriminels.

- [Oxygène Bénin, 27 février 2026](https://oxygene-benin.bj/criet-arrete-dans-une-buvette-il-aurait-servi-de-relais-pour-retirer-largent-des-cybercriminels/)
- Typologie de la GSMA sur la vitesse des fonds et le retrait par des mules : [GSMA, mai 2024](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-for-development/wp-content/uploads/2024/05/Mobile-Money-Fraud-Typologies-and-Mitigation-Strategies-20.05.24.pdf)

L'argent traverse deux ou trois comptes avant le retrait. Un des comptes de la chaîne a déjà été
signalé. C'est le scénario qui justifie la version 2 (GNN) : le premier destinataire paraît
propre, c'est son voisinage qui le trahit.

**Transactions à injecter** (hypothèse de simulation) :

| t | type | de → vers | montant | fraude |
|---|---|---|---|---|
| 0 | TRANSFER | V7 → M7 | 300 000 | 1 |
| 3 | TRANSFER | M7 → M8 | 150 000 | 1 |
| 4 | TRANSFER | M7 → M9 | 148 000 | 1 |
| 8 | TRANSFER | M8 → M10 | 149 000 | 1 |
| 12 | CASH_OUT | M9 → A1 | 147 000 | 1 |
| 15 | CASH_OUT | M10 → A5 | 148 000 | 1 |

Paramètres à faire varier : 2 à 4 étages ; M10 est marqué « déjà signalé » dans une liste à
part ; M7 a quelques semaines d'ancienneté et un petit historique normal pour paraître propre.

**Signaux attendus sur M7** : lien à deux sauts avec un compte signalé, éclatement immédiat des
fonds reçus.

---

## Scénario 5 — Le point de vente vidé

**Documenté.** Les agents et marchands sont une cible à part entière : leur compte porte un
solde élevé.

- Faux agents MTN vidant des comptes de points de vente : [Bénin Web TV, 28 décembre 2021](https://beninwebtv.com/benin-de-faux-agents-de-mtn-deposes-en-prison-pour-escroquerie/)
- Affaire de la prison de Missérété, dix ans ferme pour l'instigateur : [Bénin Web TV, 19 décembre 2023](https://beninwebtv.bj/benin-3-policiers-condamnes-dans-un-dossier-darnaque-doperateur-mobile-money/)
- Faux dépôt de 5 000 FCFA puis transfert de 200 000 FCFA depuis le téléphone de l'agente : [Le Béninois Libéré, 4 août 2025](https://lebeninoislibere.bj/benin-un-recidiviste-de-lescroquerie-via-mobile-money-face-a-la-criet-son-mode-operatoire/)

**Transactions à injecter** (hypothèse de simulation, sauf les deux premières lignes qui
reprennent l'affaire de 2025) :

| t | type | de → vers | montant | fraude |
|---|---|---|---|---|
| 0 | TRANSFER | M11 → A6 | 5 000 | 1 |
| 4 | TRANSFER | A6 → M12 | 200 000 | 1 |
| 9 | CASH_OUT | M12 → A7 | 198 000 | 1 |

Paramètres à faire varier : montant sortant de 150 000 à 2 000 000 FCFA ; le compte source est
un agent, qui d'habitude n'envoie pas de gros transferts à un particulier.

**Signaux attendus** : petit dépôt d'amorce suivi d'un gros transfert sortant inhabituel pour
un agent, vers un compte récent.

Ce scénario est le premier à couper si le temps manque : il demande de distinguer les comptes
d'agents dans les données.

---

## Contre-exemples à injecter aussi

Sans eux, le modèle apprendra que « beaucoup d'expéditeurs nouveaux » veut toujours dire
fraude, et la démo affichera de fausses alertes. Ces cas sont étiquetés `fraude = 0`.

| Cas légitime | Ce qui ressemble à une mule | Ce qui le distingue |
|---|---|---|
| Collecteur de tontine | Reçoit de nombreux expéditeurs en peu de temps | Mêmes expéditeurs chaque semaine, compte ancien, sorties régulières |
| Petit commerçant | Beaucoup d'entrées de clients nouveaux | Petits montants, entrées étalées sur la journée, solde qui reste |
| Étudiant qui reçoit de sa famille | Compte récent, retrait rapide | Un ou deux expéditeurs, toujours les mêmes |
| Vraie erreur de transfert | Renvoi d'un montant à un inconnu | Un dépôt réel a bien eu lieu juste avant |

Ces contre-exemples sont des hypothèses de simulation : nous n'avons pas de données réelles sur
ces comportements.

---

## Ce que ces scénarios ne couvrent pas

- Le remplacement frauduleux de carte SIM : aucun cas béninois daté n'a été trouvé.
- Les fausses offres d'emploi et les applications de prêt usuraire : documentées par le CNIN,
  mais la victime paie de petites sommes répétées, ce qui est un autre problème.
- La location de comptes par leurs vrais titulaires : aucune source trouvée pour le Bénin.

## Chiffres d'ampleur utilisables, et leurs limites

Il n'existe aucun chiffre public isolant la fraude au mobile money au Bénin ou dans l'UEMOA. Ce
que l'on peut dire sans tricher :

- Plus de 6 500 plaintes pour infractions numériques au Bénin en 2025, contre environ 4 000 en
  2024, toutes cybercriminalités confondues. [La Nouvelle Tribune, 15 janvier 2026](https://lanouvelletribune.info/2026/01/benin-1-500-interpellations-liees-a-la-cybercriminalite-en-2025/)
- 43 % des usagers de mobile money au Sénégal et 28 % en Côte d'Ivoire ont subi au moins une
  tentative de fraude en douze mois. Le Bénin n'a pas été enquêté. [CGAP, 20 juin 2024](https://www.cgap.org/blog/surveys-reveal-path-to-responsible-digital-finance-in-waemu)
- La BCEAO cite la fraude parmi les « risques croissants » sans la chiffrer (rapport 2024 sur
  les services financiers numériques).
