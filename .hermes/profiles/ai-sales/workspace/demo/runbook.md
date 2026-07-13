# Demo Runbook — AI Sales Company Wella

Objectif : montrer une démo end-to-end local-first du profil `ai-sales` sur Wella Professionals France, sans envoyer de messages externes.

## Pré-requis

- Profil Hermes : `ai-sales`
- Brief challenge : `workspace/CHALLENGE.md`
- Brief partenaire : `workspace/partner-brief-wella-professionals-fr.md`
- Run Wella : `workspace/prospect-runs/2026-07-12-wella-professionals-fr/`

## Parcours de démo

### 1. Montrer l'organisation 5 équipes

Ouvrir :

```text
workspace/company/teams.md
workspace/company/operating-model.md
workspace/company/handoffs.md
```

À montrer : les 5 équipes, leurs rôles, le modèle de handoff et les états de pipeline.

### 2. Montrer les skills

Vérifier les 20 skills dans :

```text
skills/ai-sales/*/SKILL.md
```

Point clé : les skills sont durables, pas seulement des réponses dans le chat.

### 3. Montrer l'ICP Wella

Ouvrir :

```text
workspace/prospect-runs/2026-07-12-wella-professionals-fr/icp.md
```

À montrer : segments, buyer personas, trigger signals, disqualifiers, scoring.

### 4. Montrer la prospection sourcée

Ouvrir :

```text
workspace/prospect-runs/2026-07-12-wella-professionals-fr/discovery.csv
workspace/prospect-runs/2026-07-12-wella-professionals-fr/sources.md
```

À montrer : 20 leads, sources OSM + sites publics, score, email non deviné.

### 5. Montrer le CRM local

Ouvrir :

```text
workspace/crm/accounts.json
workspace/crm/contacts.json
workspace/crm/opportunities.json
workspace/crm/interactions.json
workspace/crm/opt_outs.json
```

À montrer : source de vérité locale et traçable.

### 6. Montrer la review queue humaine

Ouvrir :

```text
workspace/review-queue/pending/
```

À montrer : messages personnalisés préparés mais pas envoyés, statut `manual_review`.

### 7. Montrer Content & Marketing

Ouvrir :

```text
workspace/content-assets/audits/
workspace/content-assets/offers/
```

À montrer : audits express et one-pagers personnalisés pour appuyer l'outreach.

### 8. Montrer Admin & RDV

Ouvrir :

```text
workspace/meetings/wella-positive-reply-simulation.md
```

À montrer : comment une réponse positive devient une proposition de RDV + handoff brief.

### 9. Montrer CRM & Orchestration

Ouvrir :

```text
workspace/reports/2026-07-12-wella-pipeline-report.md
workspace/reports/2026-07-12-daily-orchestration-digest.md
```

À montrer : digest, next actions par équipe, blockers, décisions humaines.

## Message de conclusion démo

Cette démo ne prétend pas que tout est branché en production. Elle montre le produit : une société commerciale IA structurée, avec frontière de preuve, CRM, handoffs, review humaine, contenu à valeur et orchestration. Les intégrations Slack/Gmail/Resend/LinkedIn/Instagram/CRM externe sont les prochaines couches à brancher sur un pipeline déjà propre.

## Commandes de vérification

```bash
python3 /root/.hermes/profiles/ai-sales/workspace/demo/discover_wella.py
python3 /root/.hermes/profiles/ai-sales/workspace/demo/build_wella_outputs.py
```

Puis vérifier :

```text
20 skills
20 leads discovery
20 accounts CRM
5 review items
3 audits + 3 offers
1 meeting simulation
2 reports
```
