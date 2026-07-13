---
name: sales-enrichment-integrations
description: Use when wiring lead-enrichment providers such as Hunter.io, Apollo-like APIs, or Clay-like enrichment into a Hermes sales/profile workflow. Build proof-backed, GDPR-aware enrichment skills and helper scripts without exposing API keys or inventing prospect data.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sales, enrichment, hunter, crm, prospecting, integrations]
    related_skills: [hermes-agent, hermes-agent-skill-authoring, google-workspace, airtable]
---

# Sales Enrichment Integrations

## Overview

Use this skill to connect lead-enrichment APIs to a Hermes sales agent/profile. The target pattern is not "call an API and dump contacts"; it is a durable enrichment layer that turns raw accounts and decision-makers into proof-backed records ready for CRM, scoring, and human-reviewed outreach.

The core standard is a strict proof boundary: no invented emails, no guessed titles, no unsourced prospect facts, and no automatic cold outreach from an enrichment step.

See `references/hunter-io-hermes.md` for the Hunter.io implementation pattern captured from an AI Sales Company setup.

## When to Use

Use when the user asks to:
- add Hunter.io, Apollo-like, Clay-like, or another enrichment provider to a Hermes profile;
- create or update sales prospecting/enrichment skills;
- build helper scripts for email discovery/verification;
- prepare lead data for CRM sync or personalized outreach;
- validate an enrichment provider with live API calls.

Do not use for:
- sending outreach messages;
- scraping private data or bypassing platform restrictions;
- storing API keys in skills, README files, shell history, or hard-coded scripts;
- bulk enrichment without a proof/consent/deliverability policy.

## Setup Pattern

1. Inspect the mission and profile before editing.
   - Read the challenge/spec, profile `SOUL.md`, existing skills, enabled tools, MCP servers, and profile `.env` key names without printing secret values.
   - Completion criterion: you know whether to patch an existing sales skill or create a profile-local class skill such as `lead-enrichment`.

2. Put secrets in the target profile environment.
   - Store provider credentials in the target profile `.env`, e.g. `HUNTER_API_KEY=...`.
   - Never ask the user to paste the key into chat unless the platform has an explicit secret-entry mechanism.
   - Completion criterion: scripts can read the key from environment or a profile-local `.env` fallback, and the key never appears in command arguments or output.

3. Create a provider helper script.
   - Prefer `python3` standard library for a portable client: `argparse`, `urllib.request`, `json`, `os`.
   - Commands should map to business operations: `account`, `domain-search`, `email-finder`, `email-verifier`, `lead-record`.
   - Completion criterion: `--help` works, syntax checks pass, missing-key errors are explicit, and output is normalized JSON.

4. Create or patch the sales enrichment SKILL.md.
   - Document when to use the provider, allowed operations, proof requirements, output schema, and guardrails.
   - Include exact commands, but use environment variables or scripts so secrets are not exposed.
   - Completion criterion: another agent can run the workflow without re-discovering the provider API shape.

5. Verify in a low-credit sequence.
   - First run an account/quota check.
   - Then run one small domain search, e.g. `--limit 3`.
   - Then verify one email only.
   - Avoid live `lead-record` tests if it would spend extra credits unnecessarily; use a mocked/unit test first.
   - Completion criterion: the integration is proven with minimal quota burn.

6. Package a proof-backed lead record.
   - Combine finder + verifier metadata into a stable schema for CRM/scoring/outreach handoff.
   - Set `next_action` conservatively (`manual_review`, `research_more`, `discard`) rather than sending.
   - Completion criterion: every contactable email has verification status, source metadata, timestamp, and human-review state.

## Standard Lead Record Shape

```json
{
  "company": {
    "name": "",
    "domain": "",
    "source_urls": []
  },
  "person": {
    "first_name": "",
    "last_name": "",
    "title": "",
    "linkedin_url": "",
    "source_urls": []
  },
  "email": {
    "address": "",
    "status": "verified|probable|risky|not_found|not_contactable",
    "provider_score": null,
    "provider_verification": {},
    "provider_sources": []
  },
  "proof": {
    "tools_used": [],
    "checked_at": "ISO-8601 timestamp",
    "notes": []
  },
  "next_action": "manual_review|sync_to_crm|research_more|discard"
}
```

Use empty strings/nulls for unknown fields and explain the gap in `proof.notes`. Do not fill unknowns with plausible guesses.

## Contactability States

- `verified`: provider verification indicates valid/high-confidence professional contact data.
- `probable`: found but not fully verified; requires manual review before cold email.
- `risky`: low score, catch-all, unverifiable, or weak source; do not send.
- `not_found`: provider found no email/contact.
- `not_contactable`: invalid, personal/private, disposable/webmail, opt-out, blocked, or compliance issue.

Never upgrade a contactability state without evidence.

## Security and Compliance Guardrails

- Keep API keys in profile `.env` or approved secret stores only.
- Do not pass keys in CLI arguments because shell history and process listings can leak them.
- Avoid printing account responses in public demos if they include personal account email or team identifiers.
- Prefer professional domain addresses over webmail or personal addresses.
- Treat opt-out as a hard stop across all channels.
- Enrichment prepares a lead; it does not send outreach.

## Common Pitfalls

1. Building the provider call before reading the challenge/profile.
   - Fix: inspect the target mission and profile first so the integration lands in the correct business skill.

2. Treating `domain-search` results as ready-to-contact.
   - Fix: run email verification and assign a conservative contactability status before CRM/outreach handoff.

3. Guessing email patterns from provider output.
   - Fix: patterns can guide manual research, but a lead record needs provider-supported or verified email data.

4. Burning credits during testing.
   - Fix: use account check, tiny domain search, one verifier call, and mocked tests for composite commands.

5. Losing source metadata during normalization.
   - Fix: preserve provider sources, dates, scores, and verification flags in the lead record.

## Verification Checklist

- [ ] Target profile and mission/spec inspected before edits.
- [ ] API key stored outside skills/scripts and never printed.
- [ ] Helper script has `--help`, missing-key behavior, normalized JSON, and syntax/unit checks.
- [ ] Live test proves account/quota, small search, and one verification without excessive credit use.
- [ ] Skill documents proof boundary, contactability states, and standard output schema.
- [ ] Lead records require human review before cold outreach unless the user explicitly changes the product policy.
