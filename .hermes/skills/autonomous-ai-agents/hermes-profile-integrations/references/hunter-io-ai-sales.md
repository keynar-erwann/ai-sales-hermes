# Hunter.io inside an AI Sales Hermes profile

Session-derived reference for configuring Hunter.io in an `ai-sales`-style profile.

## Product placement

Hunter.io is not an outreach engine. Treat it as an enrichment provider inside the Prospection & Intelligence workflow, usually under a `lead-enrichment` skill.

Best fit in the AI Sales Company architecture:

- Team: Prospection & Intelligence
- Skill: `lead-enrichment`
- Purpose: find and verify professional email data for accounts/decision-makers already selected by ICP and signal work
- Downstream consumers: CRM sync, message personalization, email sequencing, human approval queue

## Credential

Use a profile-scoped env var:

```bash
HUNTER_API_KEY=...
```

Recommended path for a named profile:

```bash
~/.hermes/profiles/<profile-name>/.env
```

Never place the key in `SOUL.md`, `SKILL.md`, docs, logs, or messages.

## Core endpoints

Use Hunter.io endpoints according to the task:

- Domain contact discovery:
  `GET https://api.hunter.io/v2/domain-search?domain=<domain>&api_key=$HUNTER_API_KEY`

- Known-person email finding:
  `GET https://api.hunter.io/v2/email-finder?domain=<domain>&first_name=<first>&last_name=<last>&api_key=$HUNTER_API_KEY`

- Email verification:
  `GET https://api.hunter.io/v2/email-verifier?email=<email>&api_key=$HUNTER_API_KEY`

Prefer a helper script that reads `HUNTER_API_KEY` from the environment and emits redacted JSON, instead of manually constructing secret-bearing curl URLs repeatedly.

## Proof boundary

A Hunter.io result should be stored as evidence, not as unquestioned truth. Track:

- provider: `hunter.io`
- endpoint used
- query inputs: domain, first name, last name, email being verified
- returned email, if any
- Hunter score/confidence/status fields when present
- verification status
- source URLs, if returned by Hunter
- checked_at timestamp
- raw response file path if saved, with secrets redacted

Classify output explicitly:

- `verified` — verification endpoint indicates a deliverable/valid result
- `probable` — Hunter suggests the email but verification is inconclusive
- `not_found` — no result
- `rejected` — invalid, disposable, blocked, opt-out, or otherwise unsafe

Never invent an email from a pattern. If Hunter does not return or verify it, mark it as not found/probable rather than fabricating.

## Sales safety rules

- Hunter.io enrichment must not automatically trigger outreach.
- Cold outreach drafts should remain human-approved at the beginning of an AI sales deployment.
- If the prospect is EU-based, keep RGPD/base-legale and opt-out handling explicit.
- Respect provider quotas and rate limits; design enrichment in batches with clear caps.
- Keep enrichment separate from message personalization: Hunter gives contact data, not the personalized reason to contact.

## Suggested skill design

Create or update a domain skill such as:

```text
~/.hermes/profiles/<profile>/skills/ai-sales/lead-enrichment/SKILL.md
```

The skill should include:

1. Inputs: target account, domain, decision-maker name/role, existing evidence.
2. Enrichment cascade: existing CRM -> public web -> Hunter domain search -> Hunter email finder -> Hunter verifier.
3. Output schema: lead/contact record with evidence fields.
4. Stop conditions: opt-out, missing consent basis, low confidence, no verified email.
5. Human approval boundary before any email/LinkedIn/Instagram send.

## Minimal verification sequence

After the user adds `HUNTER_API_KEY` to the target profile `.env`:

1. Start a fresh Hermes session for that profile, or ensure env reload behavior is known.
2. Confirm the variable is present without printing its value.
3. Call a harmless/account or low-volume test endpoint.
4. Run one controlled lookup on a public test domain only if the user approves.
5. Summarize status and remaining quota if the API returns it.
