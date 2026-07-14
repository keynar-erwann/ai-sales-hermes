# AI Sales Company — Hermes Profile

Profil : `ai-sales`

Ce profil implémente le challenge `CHALLENGE.md` : une société commerciale IA dans Hermes, organisée en 5 équipes, avec skills réutilisables, CRM local, Slack pour validation/digest, Mailtrap sandbox pour tests d'envoi, et frontière de preuve stricte.

## Lancer / vérifier

```bash
hermes -p ai-sales
python3 /root/.hermes/profiles/ai-sales/workspace/scripts/validate_profile.py
python3 /root/.hermes/profiles/ai-sales/workspace/scripts/run_daily.py
```

Par défaut `run_daily.py` n'envoie aucun cold outreach. Il inspecte la review queue, notifie Slack et écrit un digest.

Envoi sandbox seulement après validation humaine :

```bash
python3 workspace/scripts/review_manager.py approve <draft.md>
python3 workspace/scripts/run_daily.py --send-approved --test-recipient
```

## Architecture challenge

```text
Partner brief
  → ICP Builder
  → Prospect Discovery
  → Signal Detection / Pain Mapping
  → Lead Enrichment
  → Lead Scoring
  → CRM Sync
  → Message Personalization
  → Human Review Slack / review queue
  → Approved Outreach
  → Reply Triage / Follow-up / Meeting Scheduler
  → Handoff Brief
  → Pipeline Report
  → Daily Orchestration
```

## 5 équipes

1. Prospection & Intelligence : `icp-builder`, `prospect-discovery`, `signal-detection`, `pain-mapping`, `lead-enrichment`, `lead-scoring`.
2. Outreach & Engagement : `message-personalization`, `email-sequencing`, `linkedin-outreach`, `instagram-outreach`, `reply-triage`, `objection-handling`.
3. Admin & Rendez-vous : `meeting-scheduler`, `followup-cadence`, `handoff-brief`.
4. Content & Marketing : `marketing-audit`, `personalized-offer`.
5. CRM & Orchestration : `crm-sync`, `daily-orchestration`, `pipeline-report`.

## Intégrations réelles configurées

- Slack Bot token : valide pour `chat.postMessage` vers le canal `ai-sales`.
- Slack Socket Mode : nécessite un `SLACK_APP_TOKEN` xapp valide avec scope `connections:write`; le token actuel est détecté invalide par Slack pour la réception temps réel.
- Mailtrap SMTP : credentials dans `.env`, vérifiés en login SMTP.
- Hunter.io : clé présente dans `.env`, utilisée par `lead-enrichment`.

## Garde-fous

- Secrets uniquement dans `.env`, pas dans `config.yaml` ni scripts.
- Pas d'envoi depuis `review-queue/pending/`.
- Pas d'email deviné.
- Pas d'automatisation LinkedIn/Instagram sans intégration conforme.
- Toute preuve prospect doit conserver sa source.
