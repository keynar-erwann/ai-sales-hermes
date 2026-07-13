# Hunter.io Lead Enrichment Pattern

This reference captures a proven setup for adding Hunter.io to an Hermes AI sales profile.

## Context

The user had a profile named `ai-sales` and needed it to use Hunter.io as the first enrichment source for an AI Sales Company challenge. The durable pattern is profile-local: doctrine and skills live inside `~/.hermes/profiles/<profile>/`, not only in the active default profile.

## Safe Inspection Pattern

Before writing anything:

1. Read the challenge/brief if present.
2. Inspect the target profile:
   - `SOUL.md`
   - existing skills under `~/.hermes/profiles/<profile>/skills/`
   - toolsets and MCP servers
   - `.env` key names only, never secret values
3. Identify the missing product layer before adding integrations.

In the session, Hunter.io belonged under the class-level sales capability `lead-enrichment`, not as a one-off “hunter” skill.

## Files Created in the Working Example

Profile-local files:

```text
~/.hermes/profiles/ai-sales/SOUL.md
~/.hermes/profiles/ai-sales/workspace/README.md
~/.hermes/profiles/ai-sales/skills/ai-sales/lead-enrichment/SKILL.md
~/.hermes/profiles/ai-sales/skills/ai-sales/lead-enrichment/scripts/hunter_client.py
~/.hermes/profiles/ai-sales/skills/ai-sales/prospect-discovery/SKILL.md
~/.hermes/profiles/ai-sales/skills/ai-sales/prospect-discovery/templates/run-readme.md
```

Workspace directories:

```text
workspace/prospect-runs/
workspace/crm/
workspace/review-queue/
workspace/reports/
```

## Hunter.io Helper Requirements

A good `hunter_client.py` should:

- read `HUNTER_API_KEY` from the environment or the profile `.env` fallback;
- never accept the API key as a CLI argument;
- output JSON;
- include `--help`;
- fail cleanly when the key is missing;
- avoid printing secrets;
- normalize Hunter responses into sales-ready states.

Useful commands:

```bash
python3 hunter_client.py account
python3 hunter_client.py domain-search --domain stripe.com --limit 3
python3 hunter_client.py email-finder --domain stripe.com --first-name Kevin --last-name Bognar
python3 hunter_client.py email-verifier --email kbognar@stripe.com
python3 hunter_client.py lead-record --company Stripe --domain stripe.com --first-name Kevin --last-name Bognar
```

## Proven Test Sequence

1. `account` confirmed the key and quota without exposing the key.
2. `domain-search --domain stripe.com --limit 3` returned contacts with confidence scores and source URLs.
3. `email-verifier --email <one_found_email>` returned a deliverable result with score 100.
4. `lead-record` packaged finder + verifier into a CRM-ready record.

Use a small limit and one verifier first to avoid burning credits.

## Contactability Mapping

Recommended statuses:

- `verified`: deliverable professional email with strong score.
- `probable`: found but verifier is inconclusive or lower confidence.
- `risky`: low confidence, catch-all/ambiguous, or needs more research.
- `not_found`: Hunter returned no email.
- `not_contactable`: invalid, disposable, webmail/personal, opt-out, or compliance block.

Hunter.io's `type: personal` may mean a nominative professional address on the company domain rather than a private email. Confirm domain and context before classifying it as private.

## Lead Record Pattern

A `lead-record` command should call `email-finder`, then `email-verifier` only if an email is found, and return:

```json
{
  "company": {"name": "", "domain": "", "source_urls": []},
  "person": {"first_name": "", "last_name": "", "title": "", "linkedin_url": "", "source_urls": []},
  "email": {"address": "", "status": "", "hunter_score": null, "hunter_finder": {}, "hunter_verification": {}, "hunter_sources": []},
  "proof": {"tools_used": ["hunter.io"], "checked_at": "", "notes": []},
  "next_action": "manual_review"
}
```

Default to `manual_review` for contactable leads during early product/demo stages. Do not send automatically.

## Product Sequencing Lesson

Do not wire Gmail/Slack/CRM/outreach first. The stronger sequence is:

1. doctrine + architecture README;
2. `lead-enrichment` + Hunter.io helper;
3. `prospect-discovery` with scoring and signal proof;
4. first sourced 10-20 lead demo;
5. CRM source of truth;
6. message personalization and human review;
7. actual outreach integrations.

This sequencing matches a product evaluation better than a shallow automation that sends messages before proving lead quality.
