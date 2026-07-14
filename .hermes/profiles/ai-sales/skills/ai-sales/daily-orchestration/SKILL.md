---
name: daily-orchestration
description: "Use when running the AI Sales Company daily loop: inspect CRM, choose priorities, delegate work to the five teams, and produce a digest."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sales, orchestration, ai-sales, daily-loop]
    related_skills: [crm-sync, pipeline-report]
---

# Daily Orchestration

## Overview

The daily orchestration skill is the chef d'orchestre. It reads the source of truth, decides what matters now, and routes tasks to the five teams.

## When to Use

Use at the beginning of a demo, at the start of a work session, or when the user asks what the AI Sales Company should do next.

## Inputs

- Partner brief.
- CRM files.
- Prospect run files.
- Review queue.
- Reports.
- User constraints.

## Procedure

1. Inspect state.
   - Completion criterion: latest CRM, review queue, and run folders are known.
2. Identify blockers.
   - Completion criterion: missing data, missing integrations, and unsafe actions are listed.
3. Prioritize actions.
   - Completion criterion: every action has owner team, expected output, and reason.
4. Delegate or execute.
   - Completion criterion: work is routed to the correct skill/team.
5. Produce digest.
   - Completion criterion: digest lists status, decisions, and next actions.

## Daily Orchestration Digest — <date>

- Use the exact header template below to ensure consistent reporting.
- Include a section for "Decisions needed from human" to facilitate swift validation of outreach drafts and prospect lists.

```markdown
# Daily Orchestration Digest — <date>

## Pipeline status
## Blockers
## Team 1 — Prospection & Intelligence
## Team 2 — Outreach & Engagement
## Team 3 — Admin & Rendez-vous
## Team 4 — Content & Marketing
## Team 5 — CRM & Orchestration
## Decisions needed from human
## Next 24h plan
```

## Wella Demo Loop

For Wella, the first complete loop should:

1. verify partner brief;
2. produce ICP;
3. create 20 sourced leads;
4. sync CRM;
5. generate 5 review-ready messages;
6. create 2 content audits;
7. simulate one positive reply into a handoff brief;
8. produce final pipeline report.

## Operational scripts

Canonical runtime scripts live under:

```text
/root/.hermes/profiles/ai-sales/workspace/scripts/
```

Use these exact commands:

```bash
# Full profile/challenge validation
python3 /root/.hermes/profiles/ai-sales/workspace/scripts/validate_profile.py

# Daily loop: inspect CRM/review queue, notify Slack, write digest, do not send cold outreach
python3 /root/.hermes/profiles/ai-sales/workspace/scripts/run_daily.py

# Human review operations
python3 /root/.hermes/profiles/ai-sales/workspace/scripts/review_manager.py list
python3 /root/.hermes/profiles/ai-sales/workspace/scripts/review_manager.py notify
python3 /root/.hermes/profiles/ai-sales/workspace/scripts/review_manager.py approve <draft.md>
python3 /root/.hermes/profiles/ai-sales/workspace/scripts/review_manager.py reject <draft.md>

# Sandbox send: approved files only; --test-recipient routes to Mailtrap test recipient
python3 /root/.hermes/profiles/ai-sales/workspace/scripts/run_daily.py --send-approved --test-recipient
```

Daily cron is configured as a no-agent job:

```text
daily-ai-sales-orchestration · 0 9 * * * · deliver=slack · script=daily_orchestration_cron.py
```

## Integration status rules

- Slack Bot API working means outbound notifications/digests can be delivered.
- Slack Socket Mode working means incoming Slack validation/commands are live.
- If `validate_profile.py` reports `socket_error: invalid_auth`, the profile is still safe for outbound Slack and local review, but full native Slack validation is blocked until `SLACK_APP_TOKEN` is replaced with an app-level token with `connections:write` and the gateway is restarted.
- SMTP must be checked through `smtp_sender.py --check` or `validate_profile.py`; never assume Mailtrap works.

## Common Pitfalls

1. Doing the work without state. Fix: inspect CRM and run files first.
2. Skipping teams. Fix: every digest covers all 5 teams.
3. Unsafe automation. Fix: cold outreach remains in `review-queue/pending/` until explicit human approval moves it to `approved/`.
4. Sending to placeholder recipients. Fix: approved files need an explicit `To:`/`Recipient:`/`Email:` field, unless using `--test-recipient` for Mailtrap sandbox tests.
5. Ignoring connectivity failures. Fix: report the exact failed integration and continue only in honest local-first mode.
6. Hardcoding secrets. Fix: scripts read `.env`; config and scripts must not contain SMTP/Slack/API secret values.
7. **Workspace Hygiene :** Toujours vérifier l'état des répertoires `/workspace/review-queue/pending` et `approved` avant d'initier une nouvelle boucle pour éviter de dupliquer les efforts.
8. **Source de Vérité :** Ne jamais générer d'actions à partir d'un état intermédiaire ; le CRM (`/workspace/crm/`) est la seule référence pour le statut des prospects.

### Scripts utiles
- `scripts/sync_crm.py` : Script de synchronisation automatique des runs de prospection vers le CRM.
- `scripts/verify_workspace.sh` : Script de vérification de l'intégrité des dossiers avant lancement (vérifie `CHALLENGE.md`, `crm`, `review-queue`).

## Verification Checklist

- [ ] CRM/readiness inspected.
- [ ] All 5 teams covered.
- [ ] Human decisions are explicit.
- [ ] Output saved in reports or demo folder.
- [ ] `validate_profile.py` was run.
- [ ] SMTP login is OK.
- [ ] Slack Bot outbound is OK.
- [ ] Slack Socket Mode status is stated honestly.

