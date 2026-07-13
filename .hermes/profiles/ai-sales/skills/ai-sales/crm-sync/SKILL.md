---
name: crm-sync
description: "Use when writing, reading, deduplicating, or updating the AI Sales Company source-of-truth CRM for accounts, contacts, interactions, opportunities, and opt-outs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sales, crm, ai-sales]
    related_skills: [pipeline-report, daily-orchestration]
---

# CRM Sync

## Overview

Maintains a local CRM source of truth until an external CRM such as HubSpot, Attio, Airtable, or Google Sheets is connected.

## When to Use

Use whenever a lead, message, review decision, reply, meeting, or opt-out changes state.

## Local CRM Files

```text
workspace/crm/accounts.json
workspace/crm/contacts.json
workspace/crm/interactions.json
workspace/crm/opportunities.json
workspace/crm/opt_outs.json
```

## Data Rules

- Deduplicate by domain for accounts.
- Deduplicate by professional email or source URL for contacts.
- Never delete opt-outs.
- Unknown fields stay empty/null, never guessed.
- Every record should include `source_urls` and `updated_at`.

## Procedure

1. Read existing CRM files.
   - Completion criterion: current account/contact IDs and opt-outs are known.
2. Normalize incoming records.
   - Completion criterion: domain, names, status, sources and next action follow schema.
3. Deduplicate.
   - Completion criterion: no duplicate account/contact is added.
4. Update stages and interactions.
   - Completion criterion: every state change has an interaction note.
5. Write CRM files.
   - Completion criterion: JSON parses successfully and opt-outs remain preserved.

## Account Schema

```json
{
  "account_id": "acct_slug",
  "name": "",
  "domain": "",
  "city": "",
  "segment": "",
  "source_urls": [],
  "stage": "candidate",
  "score_total": null,
  "next_action": "research_more",
  "created_at": "",
  "updated_at": ""
}
```

## Common Pitfalls

1. Treating run files as CRM. Fix: sync selected records into `workspace/crm/`.
2. Losing opt-outs. Fix: read and preserve `opt_outs.json` before writes.
3. Untraceable state changes. Fix: add an interaction for every transition.

## Verification Checklist

- [ ] CRM JSON files parse.
- [ ] No duplicate domains.
- [ ] Opt-outs preserved.
- [ ] Every actionable lead has `next_action`.

