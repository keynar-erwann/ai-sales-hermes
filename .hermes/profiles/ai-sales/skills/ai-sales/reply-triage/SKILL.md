---
name: reply-triage
description: "Use when classifying inbound replies into interested, objection, later, not-now, opt-out, or irrelevant, then routing CRM next actions."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sales, reply-triage, ai-sales]
    related_skills: []
---

# Reply Triage

## Overview

Classifies replies and updates CRM routing.

## Procedure

1. Read reply and thread context.
2. Classify: interested, objection, later, not_now, opt_out, irrelevant.
3. Update CRM stage and interaction.
4. Route to meeting, objection handling, follow-up, or hard stop.

## Verification Checklist

- [ ] Opt-outs are hard stops.
- [ ] Positive replies route to Admin & RDV.
- [ ] CRM interaction is recorded.

