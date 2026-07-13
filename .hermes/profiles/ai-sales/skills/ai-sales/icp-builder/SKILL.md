---
name: icp-builder
description: "Use when defining or refining the ideal customer profile for an AI Sales Company partner before prospect discovery, scoring, and outreach."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sales, icp, prospecting, ai-sales]
    related_skills: [prospect-discovery, lead-scoring]
---

# ICP Builder

## Overview

Defines the Ideal Customer Profile for a partner company before any lead generation. The output must be specific enough to drive search, scoring, exclusions, and messaging.

## When to Use

Use this skill when:

- a new partner brief is received;
- a run needs an `icp.md`;
- prospect discovery is too broad;
- scoring criteria are unclear.

Do not use it to invent market facts. Use only the partner brief, public sources, and explicit assumptions.

## Procedure

1. Read the partner brief and available website evidence.
   - Completion criterion: partner offer, target buyers, geography, and constraints are summarized with source URLs.
2. Define target account segments.
   - Completion criterion: 3-5 account segments exist, each with inclusion and exclusion rules.
3. Define buyer personas.
   - Completion criterion: each persona has role titles, buying reason, and proof needed before outreach.
4. Define trigger signals.
   - Completion criterion: at least 8 searchable signals are listed.
5. Define disqualifiers.
   - Completion criterion: clear reject rules prevent low-fit padding.
6. Produce `icp.md` in the run folder.
   - Completion criterion: another agent can run prospect discovery from the file without extra context.

## Output Schema

```markdown
# ICP — <Partner>

## Partner offer
## Target geography
## Account segments
## Buyer personas
## Trigger signals
## Pain hypotheses
## Disqualifiers
## Scoring weights
## Search queries
## Assumptions to validate
```

## Wella Demo Defaults

For Wella Professionals France, start with:

- salons premium with strong coloration/blond/balayage services;
- colorist studios;
- multi-site independent salon groups;
- training academies or influential professional stylists;
- France-first geography.

## Common Pitfalls

1. ICP too broad. Fix: add disqualifiers and geography.
2. Persona invented. Fix: use role categories if no named person is sourced.
3. Weak signal list. Fix: require public proof before discovery.

## Verification Checklist

- [ ] ICP has account segments and buyer personas.
- [ ] ICP includes explicit exclusions.
- [ ] ICP lists searchable signals.
- [ ] ICP states assumptions separately from facts.
- [ ] ICP can drive scoring.

