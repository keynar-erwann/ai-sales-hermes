---
name: lead-enrichment
description: Use when enriching B2B leads for the AI Sales Company with verified professional emails, firmographic signals, and proof boundaries. Uses Hunter.io as the first enrichment source while forbidding guessed data and preserving evidence for CRM/outreach handoff.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ai-sales, prospecting, enrichment, hunter, email-verification, rgpd]
    related_skills: [google-workspace, airtable]
---

# Lead Enrichment

## Overview

This skill turns a raw account or decision-maker into a proof-backed sales lead. It is part of the AI Sales Company "Prospection & Intelligence" team.

Hunter.io is the first enrichment source for professional email discovery and verification. The goal is not to maximize volume; the goal is to produce reliable, traceable, GDPR-aware records that can safely move into CRM and human-reviewed outreach.

Golden rule: an email is never invented. If Hunter.io or another approved source does not support the email, mark it as unknown instead of guessing.

## When to Use

Use this skill when the user asks to:
- enrich a lead, founder, executive, or decision-maker;
- find or verify a professional email;
- prepare leads for CRM sync or outreach;
- build the first 20 enriched leads for a partner company;
- validate whether a lead is contactable.

Do not use this skill to:
- scrape private data or bypass platform restrictions;
- infer personal emails;
- send outreach automatically;
- contact prospects without human validation;
- fabricate missing titles, companies, emails, or trigger events.

## Inputs

Minimum viable input:
- company domain, e.g. `example.com`;
- optionally first name, last name, role/title, LinkedIn URL, company name, country/market.

Preferred input:
- partner ICP;
- target account domain;
- target persona;
- source URL proving the person/company context;
- reason this lead might matter now.

If the company domain is missing, find it through public web research first and keep the source URL. Do not call Hunter.io against an uncertain domain without labeling the uncertainty.

## Tooling

Primary helper script:

```bash
python3 /root/.hermes/profiles/ai-sales/skills/ai-sales/lead-enrichment/scripts/hunter_client.py --help
```

The script reads `HUNTER_API_KEY` from the environment. The key must live in:

```bash
/root/.hermes/profiles/ai-sales/.env
```

Required line:

```bash
HUNTER_API_KEY=...
```

Never print or hard-code the key. Do not put the key directly in a shell command.

## Hunter.io Operations

### 1. Domain search

Use when you know the company domain and need possible contacts or company email patterns.

```bash
python3 /root/.hermes/profiles/ai-sales/skills/ai-sales/lead-enrichment/scripts/hunter_client.py domain-search --domain example.com --limit 10
```

Completion criterion: output includes the queried domain, request status, returned contacts or a clear empty result, and no exposed API key.

### 2. Email finder

Use when you already have a named person and a domain.

```bash
python3 /root/.hermes/profiles/ai-sales/skills/ai-sales/lead-enrichment/scripts/hunter_client.py email-finder --domain example.com --first-name Ada --last-name Lovelace
```

Completion criterion: output includes `email` only if Hunter.io returns one, plus score/confidence and sources when available.

### 3. Email verifier

Use before any email is considered contactable.

```bash
python3 /root/.hermes/profiles/ai-sales/skills/ai-sales/lead-enrichment/scripts/hunter_client.py email-verifier --email ada@example.com
```

Completion criterion: output includes verification status, score, and enough metadata to decide `verified`, `risky`, or `not_contactable`.

### 4. Lead record

Use when a lead is ready to be packaged for CRM, scoring, or human-reviewed outreach. This command runs Hunter.io `email-finder` and, if an email is found, `email-verifier`, then returns the standard proof-backed schema.

```bash
python3 /root/.hermes/profiles/ai-sales/skills/ai-sales/lead-enrichment/scripts/hunter_client.py lead-record \
  --company Stripe \
  --domain stripe.com \
  --first-name Kevin \
  --last-name Bognar \
  --title "Vice President of Sales" \
  --linkedin-url "https://www.linkedin.com/in/kevinjbognar"
```

Optional proof anchors:

```bash
  --company-source-urls "https://stripe.com" \
  --person-source-urls "https://www.linkedin.com/in/kevinjbognar"
```

Completion criterion: output follows the standard lead schema, includes Hunter.io finder/verifier metadata, and sets `next_action` to a safe value such as `manual_review`, not automatic sending.

## Enrichment Workflow

1. Anchor the account.
   - Confirm the company name and domain from public sources.
   - Save at least one source URL.
   - Done when the domain is known or explicitly marked unknown.

2. Anchor the person.
   - Confirm the person's name, role, and company from public sources where possible.
   - If the person cannot be confirmed, enrich the account but do not invent a decision-maker.
   - Done when the person is confirmed, uncertain, or absent.

3. Find contact data with Hunter.io.
   - If a person is known, run `email-finder`.
   - If only the domain is known, run `domain-search` and filter for ICP-relevant roles.
   - Done when each candidate has `email_found`, `email_not_found`, or `needs_manual_research`.

4. Verify before use.
   - Run `email-verifier` for every email that might enter CRM or outreach.
   - Treat low-confidence, disposable, personal, or invalid emails as not contactable.
   - **Crucial**: If Hunter.io returns `not_found`, do NOT invent an email pattern. Adhere strictly to the `not_found` status.
   - Done when every email has a verification status.

5. Produce a proof-backed lead record.
   - Include sources, Hunter.io metadata, score/confidence, and timestamp.
   - Separate facts from interpretation.
   - Done when another agent can sync the record to CRM without re-asking what is proven.

6. Hand off safely.
   - If contactable, pass to `message-personalization` or CRM sync with proof.
   - If not contactable, mark the next best action: manual research, LinkedIn-only, or discard.
   - Done when the lead has a clear next action and no missing hidden assumptions.

## Contactability Rules

Use these statuses consistently:

- `verified`: Hunter.io verification indicates the address is valid/high-confidence.
- `probable`: Hunter.io found an email but verification is inconclusive. Do not send cold email without manual review.
- `risky`: low score, catch-all, unverifiable, or weak source. Do not send; research further.
- `not_found`: Hunter.io found no email.
- `not_contactable`: invalid, personal email, opt-out, blocked domain, or GDPR/compliance issue.

Never upgrade a status manually without evidence.

## Troubleshooting Email Sending
See `references/troubleshooting-email.md` for CLI email tool limitations and alternative dispatch workflows.

## Standard Output Schema

Return enriched leads in this shape whenever possible:

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
    "hunter_score": null,
    "hunter_verification": {},
    "hunter_sources": []
  },
  "proof": {
    "tools_used": ["hunter.io"],
    "checked_at": "ISO-8601 timestamp",
    "notes": []
  },
  "next_action": "sync_to_crm|manual_review|research_more|discard"
}
```

If a field is unknown, leave it empty/null and explain why in `proof.notes`. Do not fill gaps with plausible guesses.

## GDPR and Deliverability Guardrails

- Use professional contact data only.
- Keep opt-out state as a hard stop across all channels.
- Do not enrich or contact private/personal addresses unless the user explicitly confirms a lawful basis and the context is appropriate.
- Avoid bulk blind exports. Prefer small batches with proof and human review.
- Outreach is not part of this skill. This skill may prepare contactability; another skill drafts messaging, and humans validate early cold sends.

## Common Pitfalls

1. Guessing common email formats.
   - Fix: use Hunter.io finder/verifier or mark unknown.

2. Treating a found email as verified.
   - Fix: run `email-verifier` before CRM/outreach handoff.

3. Losing the source trail.
   - Fix: include public source URLs and Hunter.io metadata in the lead record.

4. Mixing facts and assumptions.
   - Fix: facts go in company/person/email fields; assumptions go in proof notes or scoring rationale.

5. Sending too early.
   - Fix: enrichment stops at contactability and next action. Cold outreach requires human validation at the current product stage.

## Verification Checklist

- [ ] `HUNTER_API_KEY` is present in the profile environment before live Hunter.io calls.
- [ ] No API key appears in commands, logs, output, skills, or CRM notes.
- [ ] Domain and person identity are sourced or marked uncertain.
- [ ] Every email has a Hunter.io result or an explicit `not_found`/`needs_manual_research` state.
- [ ] Every contactable email has been verified.
- [ ] Output follows the standard lead schema or explains deviations.
- [ ] Next action is explicit and safe.
