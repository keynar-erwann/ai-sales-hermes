# Hunter.io in a Hermes AI Sales Profile

## Captured Pattern

A Hunter.io integration for a Hermes `ai-sales` profile should live as a business enrichment layer, not as a generic API dump. In the AI Sales Company challenge, Hunter.io maps to the Prospection & Intelligence team and the `lead-enrichment` skill: verified professional email discovery, proof preservation, and CRM/outreach handoff.

## Profile Layout Used

Example profile-local files:

```text
~/.hermes/profiles/ai-sales/.env
~/.hermes/profiles/ai-sales/SOUL.md
~/.hermes/profiles/ai-sales/skills/ai-sales/lead-enrichment/SKILL.md
~/.hermes/profiles/ai-sales/skills/ai-sales/lead-enrichment/scripts/hunter_client.py
```

The `.env` contains:

```bash
HUNTER_API_KEY=...
```

Do not print the key. Do not pass it as a CLI argument.

## Helper Script Commands

The useful command set was:

```bash
python3 hunter_client.py account
python3 hunter_client.py domain-search --domain stripe.com --limit 3
python3 hunter_client.py email-finder --domain stripe.com --first-name Kevin --last-name Bognar
python3 hunter_client.py email-verifier --email kbognar@stripe.com
python3 hunter_client.py lead-record --company Stripe --domain stripe.com --first-name Kevin --last-name Bognar --title "Vice President of Sales" --linkedin-url "https://www.linkedin.com/in/kevinjbognar"
```

`lead-record` should run `email-finder`, then `email-verifier` if an email is found, and return a CRM/outreach-ready JSON record. It spends credits, so test it with mocked responses before a live run.

## Live Verification Sequence

A low-credit proof sequence:

1. `account` confirms API key/quota. Be aware the response may include the user's Hunter account email; do not paste it into public artifacts.
2. `domain-search --limit 3` confirms search and source metadata. Hunter's `type: personal` often means a named professional address rather than a generic address; inspect the domain before treating it as private/personal.
3. `email-verifier` on one found address confirms deliverability and produces the contactability status.

Example successful verifier signals:

```json
{
  "result": "deliverable",
  "score": 100,
  "mx_records": true,
  "smtp_check": true,
  "disposable": false,
  "webmail": false,
  "accept_all": false,
  "status": "verified"
}
```

## Normalization Rules

Preserve:
- `score` / confidence;
- `result` / verifier status;
- `sources` with URI/domain and seen dates;
- `mx_records`, `smtp_check`, `accept_all`, `disposable`, `webmail` flags;
- checked timestamp.

Map to contactability:
- deliverable + high score + no disposable/webmail => `verified`;
- deliverable but weaker evidence => `probable`;
- low score/inconclusive/catch-all => `risky`;
- invalid/undeliverable/disposable/webmail/blocked => `not_contactable`;
- no email => `not_found`.

## Product Guardrails

- Hunter.io enrichment is not an outreach sender.
- A found email is not automatically a valid message target.
- For early product demos, set `next_action: manual_review` for verified/probable contacts.
- Every message still needs a real, recent, sourced personalization signal.
- Keep opt-out and GDPR constraints above growth/volume goals.
