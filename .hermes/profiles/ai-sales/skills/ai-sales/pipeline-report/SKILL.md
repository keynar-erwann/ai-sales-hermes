---
name: pipeline-report
description: "Use when producing an investor/evaluator-readable digest of the AI Sales Company pipeline, including counts, blockers, risks, and next actions."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sales, reporting, pipeline, ai-sales]
    related_skills: [crm-sync, daily-orchestration]
---

# Pipeline Report

## Overview

Produces clear pipeline reporting from CRM and run files. This is the evidence that the AI Sales Company is orchestrated, not just generating text.

## When to Use

Use after a run, before a demo, or during daily orchestration.

## Report Sections

- Executive summary.
- Pipeline counts by stage.
- Top opportunities.
- Review queue status.
- Enrichment status.
- Risks and blockers.
- Next actions by team.
- Proof boundary notes.

## Procedure

1. Read CRM files and review queue.
   - Completion criterion: counts by stage can be computed.
2. Read latest prospect run if relevant.
   - Completion criterion: run source files are identified.
3. Summarize progress.
   - Completion criterion: every number comes from a file or is labeled as not yet available.
4. List next actions by team.
   - Completion criterion: each of the 5 teams has either an action or an explicit no-action reason.
5. Save report.
   - Completion criterion: report exists under `workspace/reports/`.

## Output File

```text
workspace/reports/YYYY-MM-DD-pipeline-report.md
```

## Common Pitfalls

1. Reporting vibes. Fix: use counts and file-backed facts.
2. Ignoring blockers. Fix: list missing integrations and data gaps.
3. Hiding weak data. Fix: call out proof gaps.

## Verification Checklist

- [ ] Counts match CRM files.
- [ ] All 5 teams are represented.
- [ ] Next actions are concrete.
- [ ] Proof gaps are visible.

