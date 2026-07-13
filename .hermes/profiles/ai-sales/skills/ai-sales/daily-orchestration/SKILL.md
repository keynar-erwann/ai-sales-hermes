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

## Daily Digest Template

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

## Common Pitfalls

1. Doing the work without state. Fix: inspect CRM and run files first.
2. Skipping teams. Fix: every digest covers all 5 teams.
3. Unsafe automation. Fix: cold outreach remains manual review unless explicitly approved.

## Verification Checklist

- [ ] CRM/readiness inspected.
- [ ] All 5 teams covered.
- [ ] Human decisions are explicit.
- [ ] Output saved in reports or demo folder.

