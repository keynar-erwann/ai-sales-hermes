## Orchestra Agent

```
CHALLENGE TECHNIQUE · ALTERNANT
```
**BRIEF DE MISSION**

# Construire une AI

# Sales Company

# dans Hermes

#### Une équipe d'agents IA qui trouve les prospects parfaits, engage de

#### façon authentique, gère les rendez-vous et pilote le pipeline — de bout en

#### bout, pour chaque société partenaire.

**POUR**

##### Erwann Keynar

github.com/keynar-erwann

```
DE LA PART DE
```
##### Orchestra Intelligence

```
ndoumekeynar@gmail.com
```
**SOCLE**

##### Hermes Agent (open-source)

```
HORIZON
```
##### Futur produit Orchestra Agent

```
LA MISSION EN UNE PHRASE
```
#### Recrée dans Hermes une « société commerciale » entièrement tenue par des

#### agents IA coordonnés — prospection, outreach hyper-personnalisé, prise de

#### RDV, contenu et CRM — avec des skills impeccables et les intégrations

#### LinkedIn, Instagram, Gmail, Resend, Slack et un CRM.


## 01 Le contexte

##### Avant la mission, comprends l'univers dans lequel tu construis. Tu n'as pas encore

##### accès à Orchestra Agent — mais tu vas bâtir sur sa base technique, Hermes.

#### Ce qu'est Orchestra Agent

##### Orchestra Agent, ce n'est pas un chatbot de plus. Ce sont des employés IA : des agents qui

##### exécutent des missions complètes — recherche, analyse, production, livraison — sur une

##### infrastructure privée, pour une entreprise cliente. Un client = un agent (ou une équipe d'agents)

##### configuré comme un collaborateur, avec sa doctrine, ses outils et sa mémoire.

##### Sous le capot, Orchestra Agent est la version produit de Hermes Agent , un socle open-source (Nous

##### Research, licence MIT). C'est exactement là-dessus que tu vas travailler. Ce que tu construis dans

##### Hermes deviendra, demain, un produit Orchestra Agent vendu à des sociétés partenaires.

#### Comment Hermes fonctionne (l'essentiel)

## 02 La mission

##### On te challenge sur un produit ambitieux et concret. L'objectif : impressionner par la

##### qualité, la finesse et la vision 360 °.

#### Le défi

##### Construis une AI Sales Company : une équipe d'agents qui, pour une société partenaire donnée,

##### prend en charge tout le cycle commercial B 2 B — de « qui contacter » jusqu'à « rendez-vous pris et

##### suivi dans le CRM ». Inspiration assumée : 11 X (Alice / Julian), Artisan (Ava), Agent Forge , Clay pour

##### l'enrichissement. Mais on veut ta patte, pas une copie.

```
Un profil = un agent configuré (~/.hermes/profiles/<nom>/) : sa doctrine (SOUL.md), sa config,
ses clés, sa mémoire, ses skills.
Les skills = des procédures réutilisables écrites en SKILL.md. C'est là que vit le savoir-faire : «
comment prospecter », « comment personnaliser un message ». Pas dans le chat — dans des skills
durables.
Les toolsets = ce que l'agent a le droit de faire (web, fichiers, code...), activables/verrouillables par
profil.
Les serveurs MCP = les branchements vers le monde extérieur (Gmail, CRM, LinkedIn...). C'est par là
que ton agent agit vraiment.
La gateway = le pont vers les plateformes de messagerie (Slack nativement), pour les notifications et
la validation humaine.
```

```
LE STANDARD VISÉ
```
##### Un outreach indiscernable de celui d'un excellent commercial humain. Chaque message

##### est ancré sur un signal réel et récent du prospect. Zéro spam générique. La personnalisation

##### n'est pas une option — c'est le cœur du produit.

#### Ce que la « société » doit savoir faire

```
Trouver les prospects parfaits pour chaque société partenaire (ICP précis, comptes + décideurs).
Analyser leur actualité et leurs points de tension : levées, recrutements, lancements, presse,
changements d'équipe, signaux d'intention.
Engager de façon authentique , hyper-personnalisée, multi-canal (LinkedIn, Instagram, email), la plus
humaine possible.
Gérer les rendez-vous : proposer des créneaux, réserver, gérer le calendrier, relancer les no-shows.
Produire du contenu à valeur : audits express et offres marketing personnalisées par prospect.
Piloter le tout dans un CRM : chaque prospect suivi, chaque relance orchestrée, un reporting
quotidien.
```
## 03 L'architecture cible — 5 équipes, un chef d'orchestre

##### Pense la société comme un vrai orga : des équipes spécialisées qui se passent le relais,

##### coordonnées par un agent « chef d'orchestre » qui tient la boucle quotidienne et

##### délègue.

#### Équipe 1 Prospection & Intelligence

```
Le radar. Trouve qui vaut la peine d'être contacté, et pourquoi maintenant.
Définit l'ICP par partenaire, découvre comptes + décideurs, détecte les trigger events (levée,
recrutement, lancement, presse, nouvel exec), cartographie les points de tension , enrichit (email
pro, LinkedIn, tech stack) et score chaque lead (fit × intention × timing).
```
#### Équipe 2 Outreach & Engagement

```
La voix. Engage chaque prospect comme le ferait un commercial d'élite.
Construit un angle personnalisé ancré sur un signal réel, orchestre des séquences multi-canal
(LinkedIn, Instagram, Gmail chaud, Resend à l'échelle), trie les réponses (intéressé / objection / pas
maintenant / opt-out) et gère les objections. Ton humain, jamais robotique.
```

#### Équipe 3 Admin & Rendez-vous

```
Le chef de cabinet. Transforme un « oui » en rendez-vous tenu.
Propose des créneaux, réserve dans le calendrier , envoie l'invitation, gère les conflits et les buffers,
relance les silences et les no-shows, et prépare un brief de passation avant chaque RDV (contexte
prospect complet).
```
#### Équipe 4 Content & Marketing

```
L'artisan. Donne une raison concrète de répondre.
Produit un audit express personnalisé du prospect (site, SEO/GEO, social), un one-pager d'offre
sur-mesure , et les assets de contenu qui appuient l'outreach. La valeur avant la demande.
```
#### Équipe 5 CRM & Orchestration

```
Le chef d'orchestre. La colonne vertébrale et la mémoire.
Tient l' état de chaque prospect dans le CRM, exécute la boucle quotidienne (qui relancer, qui faire
avancer), produit un digest Slack quotidien du pipeline, et garantit l'hygiène des données
(dédoublonnage, opt-out, RGPD).
```
```
LE PRINCIPE D'ORCHESTRATION
```
##### Un agent chef d'orchestre tourne chaque jour : il lit l'état du pipeline, décide des actions, et

##### délègue à des sous-agents spécialisés (Hermes gère la délégation). Chaque équipe est un ou

##### plusieurs skills ; le chef d'orchestre est le skill qui les enchaîne.

## 04 Les skills à construire

##### Le cœur de l'évaluation. Chaque skill est un SKILL.md autonome, réutilisable, avec une

##### procédure claire et une frontière de preuve. Voici la carte cible — libre à toi d'en ajouter,

##### d'en fusionner, de nous surprendre.


###### PROSPECTION & INTELLIGENCE

```
SKILL CE QU'IL FAIT OUTILS
```
```
icp-builder Définit / affine l'ICP par société partenaire (secteur, taille,
rôle, signaux)
```
```
Web, brief
partenaire
```
```
prospect-discovery Trouve les comptes cibles + les bons décideurs Apollo / LinkedIn,
web
```
```
signal-detection Détecte les trigger events récents (levée, recrutement,
presse, lancement)
```
```
Web search,
presse
```
```
pain-mapping Cartographie les points de tension et enjeux du prospect Web, site, social
```
```
lead-enrichment Enrichit en cascade (email pro vérifié, LinkedIn, tel, tech
stack)
```
```
Apollo / Clay-like
```
```
lead-scoring Score et priorise : fit × intention × timing Interne
```
###### OUTREACH & ENGAGEMENT

```
SKILL CE QU'IL FAIT OUTILS
```
```
message-personalization Rédige un angle unique ancré sur un signal réel (jamais
générique)
```
```
Interne
```
```
linkedin-outreach Connexion + séquence LinkedIn, ton humain, cadence
maîtrisée
```
```
Unipile /
MCP
```
```
instagram-outreach DM Instagram ciblé (là où c'est pertinent : fondateurs, D 2 C) Unipile /
MCP
```
```
email-sequencing Séquences email multi-touch (Gmail chaud / Resend échelle) Gmail,
Resend
```
```
reply-triage Classe et route les réponses (intéressé / objection / plus tard
/ opt-out)
```
```
Gmail, CRM
```
```
objection-handling Répond aux objections courantes avec justesse Interne
```

###### ADMIN & RDV · CONTENT · CRM & ORCHESTRATION

```
SKILL CE QU'IL FAIT OUTILS
```
```
meeting-scheduler Propose des créneaux, réserve, envoie l'invite Google Cal /
Cal.com
```
```
followup-cadence Relances intelligentes : silence, no-show, post-RDV CRM, email
```
```
handoff-brief Brief de passation complet avant chaque rendez-vous CRM
```
```
marketing-audit Audit express personnalisé (site, SEO/GEO, social) du
prospect
```
```
Web
```
```
personalized-offer One-pager d'offre sur-mesure par prospect Interne
```
```
crm-sync Écrit / lit l'état de chaque prospect — source de vérité HubSpot / Attio
```
```
daily-orchestration La boucle quotidienne qui délègue aux équipes Sous-agents
```
```
pipeline-report Digest quotidien du pipeline poussé dans Slack Slack
```
## 05 Les intégrations

##### Ton agent doit agir , pas seulement rédiger. Chaque canal se branche via un serveur

##### MCP ou une API. Attention à la réalité du terrain : ToS des plateformes, délivrabilité,

##### comptes chauffés.

```
LinkedIn + Instagram Unipile / HeyReach
Messagerie unifiée via une API tierce (pas d'accès
officiel brut). Comptes chauffés, rate limits stricts,
ton humain — sinon bannissement.
```
```
Gmail MCP Gmail (OAuth)
Boîte « chaude » pour l'outreach 1 : 1 personnalisé.
Envoi, lecture des réponses, threading.
```
```
Resend API
Envoi transactionnel / à l'échelle. Domaine dédié
vérifié (SPF, DKIM, DMARC) obligatoire pour la
délivrabilité.
```
```
Slack natif (gateway Hermes)
Notifications, validation humaine avant envoi ,
digest quotidien du pipeline, alertes réponses
chaudes.
```
```
Calendrier Google Cal / Cal.com
Réservation de créneaux, gestion des conflits et
buffers, invitations automatiques.
```
```
CRM HubSpot (gratuit) / Attio
Source de vérité du pipeline. Chaque prospect,
chaque interaction, chaque état — traçable et à
jour.
```

```
Enrichissement Apollo / Clay-like
Trouve les emails pro vérifiés et les données
firmographiques en cascade.
```
```
Signaux & recherche Web search
Actualité, presse, changements d'équipe, sources
publiques pour ancrer chaque message.
```
## 06 Les règles d'or

##### Ce qui sépare un vrai produit d'un script de spam. Non négociable.

### 1 Frontière^ de^ preuve

```
Zéro donnée prospect inventée. Chaque fait affirmé sur un prospect trace vers une source réelle. Si l'info
n'est pas sourcée, elle n'existe pas.
```
### 2 Personnalisation^ obligatoire

```
Aucun envoi générique. Chaque message est ancré sur un signal réel et récent. Un message qui pourrait être
envoyé à 100 personnes n'est envoyé à personne.
```
### 3 Humain^ dans^ la^ boucle

```
Au démarrage, chaque envoi cold passe par une validation Slack. La confiance se gagne avant l'autonomie.
```
### 4 RGPD^ &^ consentement

```
Base légale claire, opt-out en un clic respecté partout, pas de scraping abusif. Les prospects sont européens.
```
### 5 Délivrabilité^ &^ respect^ des^ plateformes

```
Domaine chauffé, volumes progressifs, rate limits LinkedIn/Instagram respectés. Un compte banni = une
équipe à l'arrêt.
```
## 07 Comment on évalue

##### On cherche la qualité et la vision, pas la quantité de features. Barème indicatif sur 100.

**Qualité de la personnalisation**
L'outreach est-il indiscernable d'un excellent humain?

###### 25

**Orchestration multi-équipes**
Les agents se passent-ils le relais proprement, sans perte d'info?

###### 20

**Design des skills**
Autonomes, réutilisables, SKILL.md clairs et robustes

###### 15

**Intégrité CRM & frontière de preuve**
Chaque prospect traçable, à jour, zéro hallucination

###### 15


**Démo end-to-end**
Un vrai run sur une société partenaire, de A à Z

###### 15

**Créativité & vision 360 °**
Des angles qu'on n'avait pas listés

###### 10

## 08 Livrables & jalons

##### Une trame en 4 semaines — adapte-la, mais montre une progression et une démo finale

##### qui tourne.

##### S

SOCLE

```
Fondations + prospection. Profil Hermes ai-sales, SOUL.md, ICP, skill de découverte → 20
leads enrichis avec leurs signaux.
```
##### S

VOIX

```
Personnalisation + 1 canal. Skills de personnalisation + séquence email, sync CRM. Premiers
messages validés en Slack.
```
##### S

ÉCHELLE

```
Multi-canal + RDV. LinkedIn/Instagram, scheduling, relances, digest Slack quotidien.
```
##### S

SHOW

```
Orchestration + démo. La boucle complète qui tourne sur une vraie société partenaire, +
documentation des skills.
```
## 09 Pour démarrer

```
Mise en route Soumission
```
```
Installe Hermes Agent (Nous Research, doc
officielle)
Crée le profil ai-sales
Écris le SOUL.md : la doctrine de ton
équipe commerciale
Premier skill : prospect-discovery
Branche un premier MCP (Gmail ou CRM)
```
```
Un repo GitHub sous keynar-erwann
(profil + skills + doc)
Un README qui explique l'archi et
comment lancer une démo
Une capture / vidéo d'un run end-to-end
Questions à tout moment :
ndoumekeynar@gmail.com
```

**UN DERNIER MOT**

##### On ne cherche pas quelqu'un qui coche des cases. On cherche quelqu'un qui pense comme un

##### fondateur : qui comprend qu'un bon message vaut mille envois, qui soigne le détail, et qui a

##### envie de construire le produit commercial IA le plus fin du marché. Surprends-nous.


