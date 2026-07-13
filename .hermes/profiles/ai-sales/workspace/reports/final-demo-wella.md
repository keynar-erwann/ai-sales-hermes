# Final Demo — Wella Professionals France x AI Sales Company

Date: 2026-07-12

## Résumé

Cette démo montre une version local-first de l'AI Sales Company dans Hermes pour Wella Professionals France.

Le système couvre les 5 équipes demandées dans le challenge :

1. Prospection & Intelligence
2. Outreach & Engagement
3. Admin & Rendez-vous
4. Content & Marketing
5. CRM & Orchestration

Aucun message externe n'a été envoyé. Les drafts sont préparés pour validation humaine.

## Entrées

- Challenge : `workspace/CHALLENGE.md`
- Partner brief : `workspace/partner-brief-wella-professionals-fr.md`
- ICP : `workspace/prospect-runs/2026-07-12-wella-professionals-fr/icp.md`

## Sorties principales

### Prospection & Intelligence

- 40 candidats sauvegardés : `workspace/prospect-runs/2026-07-12-wella-professionals-fr/candidates.json`
- 20 leads sélectionnés : `workspace/prospect-runs/2026-07-12-wella-professionals-fr/discovery.json`
- Export CSV : `workspace/prospect-runs/2026-07-12-wella-professionals-fr/discovery.csv`
- Sources : `workspace/prospect-runs/2026-07-12-wella-professionals-fr/sources.md`

### CRM & Orchestration

- Accounts : `workspace/crm/accounts.json`
- Contacts : `workspace/crm/contacts.json`
- Opportunities : `workspace/crm/opportunities.json`
- Interactions : `workspace/crm/interactions.json`
- Opt-outs : `workspace/crm/opt_outs.json`
- Pipeline report : `workspace/reports/2026-07-12-wella-pipeline-report.md`
- Daily digest : `workspace/reports/2026-07-12-daily-orchestration-digest.md`

### Outreach & Engagement

- 5 messages personnalisés en attente de validation : `workspace/review-queue/pending/`
- Copies drafts : `workspace/outreach-drafts/`

### Content & Marketing

- 3 audits express : `workspace/content-assets/audits/`
- 3 one-pagers d'offre : `workspace/content-assets/offers/`

### Admin & Rendez-vous

- Simulation de réponse positive + handoff : `workspace/meetings/wella-positive-reply-simulation.md`

## Frontière de preuve

- Les leads proviennent de sources publiques : OpenStreetMap Overpass + sites web publics.
- Chaque lead sélectionné a au moins une source entreprise et une source signal.
- Aucun décideur nommé n'a été inventé.
- Aucun email n'a été deviné.
- Hunter.io n'a pas été utilisé sur ces 20 leads parce qu'aucun couple personne nommée + domaine fiable n'a été établi pendant cette passe.

## Ce que la démo prouve

- Le profil `ai-sales` est structuré comme une société commerciale, pas comme un simple chatbot.
- Les 5 équipes existent et ont des responsabilités claires.
- Les skills sont durables dans `skills/ai-sales/`.
- Le CRM local maintient une source de vérité.
- Les messages sont personnalisés mais bloqués en `manual_review`.
- La boucle d'orchestration produit un digest et des next actions par équipe.

## Limites assumées

- Slack réel non branché : remplacé par une review queue locale démontrable.
- Gmail/Resend réels non branchés : séquences et drafts créés localement.
- LinkedIn/Instagram réels non automatisés : skills de préparation sûre créés, sans action plateforme.
- CRM externe non branché : CRM local JSON utilisé comme source de vérité MVP.
- Capture/vidéo non produite ici : transcript et runbook disponibles.

## Prochaine étape pour passer de MVP à intégrations

1. Valider humainement les 20 leads et retirer les faux positifs éventuels.
2. Identifier les décideurs nommés des 5 meilleurs comptes.
3. Utiliser Hunter.io uniquement sur les personnes sourcées.
4. Brancher Slack pour review queue réelle.
5. Brancher Gmail ou Resend pour brouillons/envoi validé.
6. Choisir CRM externe : HubSpot, Attio, Airtable ou Google Sheets.
7. Préparer repo GitHub et capture/vidéo.
