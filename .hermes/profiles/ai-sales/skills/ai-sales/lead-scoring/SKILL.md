---
name: lead-scoring
description: "Use when prioritizing discovered leads with a fit × intent × timing score and deciding whether to enrich, draft, research more, or discard."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sales, lead-scoring, ai-sales]
    related_skills: [icp-builder, lead-enrichment]
---

# Lead Scoring

## Overview

Scores leads so the AI Sales Company spends research and enrichment effort only where quality justifies it.

## When to Use

Use after prospect discovery and before Hunter.io enrichment or message drafting.

## Scoring Model

Score each dimension from 0 to 5.

- `fit`: account matches ICP and buyer persona.
- `intent`: public signal indicates a plausible current need.
- `timing`: signal is recent or the account is in an active change window.

Total:

```text
total = fit * 0.45 + intent * 0.35 + timing * 0.20
```

Recommended routing:

- `4.0-5.0`: enrich or draft.
- `3.0-3.9`: research more or enrich only if source quality is strong.
- `2.0-2.9`: keep as candidate, do not spend Hunter credits.
- `<2.0`: discard.

## Procedure

1. Read ICP and lead record.
   - Completion criterion: fit rules and disqualifiers are visible.
2. Check source quality.
   - Completion criterion: every score references a source or states that proof is missing.
3. Assign fit, intent, timing.
   - Completion criterion: each number has a one-sentence reason.
4. Set next action.
   - Completion criterion: lead is routed to `lead_enrichment`, `manual_review`, `research_more`, `sync_to_crm`, or `discard`.
5. Write score into JSON/CSV/CRM.
   - Completion criterion: no lead is prioritized without a score reason.

## Output Fields

```json
{
  "score": {
    "fit": 0,
    "intent": 0,
    "timing": 0,
    "total": 0.0,
    "reason": ""
  },
  "next_action": "research_more"
}
```

## Common Pitfalls

1. Scoring by gut feel. Fix: tie every score to a source or missing-proof note.
2. Over-enriching. Fix: only spend Hunter.io on high-score leads with reliable domains and named people.
3. Padding lists. Fix: discard weak records.

## Verification Checklist

- [ ] Every high-priority lead has source-backed scoring.
- [ ] Low-confidence leads are not routed to outreach.
- [ ] Hunter.io is used only where justified.

