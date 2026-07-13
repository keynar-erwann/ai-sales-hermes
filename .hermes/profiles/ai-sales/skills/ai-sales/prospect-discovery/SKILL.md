---
name: prospect-discovery
description: Use when the AI Sales Company must discover ICP-fit B2B accounts and decision-makers for a partner company, attach real recent trigger signals, and hand off only proof-backed candidates to lead-enrichment/Hunter.io.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ai-sales, prospecting, icp, lead-generation, signal-detection, proof-boundary]
    related_skills: [lead-enrichment]
---

# Prospect Discovery

## Overview

This skill is the AI Sales Company radar. It decides who is worth contacting and why now.

It transforms a partner brief into a ranked list of B2B accounts and decision-makers with proof-backed signals. It does not send outreach. It does not invent missing company, person, title, email, or signal data. Once a candidate is sufficiently anchored, it hands the candidate to `lead-enrichment` for Hunter.io email discovery and verification.

The output must be good enough for another agent to continue without redoing the research: every lead has an ICP rationale, source URLs, signal evidence, confidence, and a safe next action.

## When to Use

Use this skill when the user asks to:
- find prospects for a partner company;
- build the first 20 enriched leads for the AI Sales Company challenge;
- discover target accounts and decision-makers from an ICP;
- identify trigger events such as funding, hiring, launches, press, new executives, partnerships, or tech changes;
- prepare candidates for Hunter.io enrichment;
- produce a proof-backed prospect list for CRM or outreach review.

Do not use this skill to:
- buy or scrape bulk lead lists blindly;
- guess people or emails;
- send messages;
- use LinkedIn/Instagram automation directly;
- bypass robots, ToS, login walls, or rate limits;
- enrich private/personal emails.

## Required Inputs

Minimum input:
- partner company name or offer;
- target market or rough ICP.

Preferred input:
- partner website;
- offer/value proposition;
- target geography;
- excluded industries/accounts;
- buyer personas and titles;
- minimum/maximum company size;
- proof of existing customers or best-fit use cases;
- CRM fields or output format required.

If the partner brief is incomplete, make reasonable assumptions only for search strategy and label them as assumptions. Never present an assumption as a prospect fact.

## Definitions

- Account: target company.
- Decision-maker: person likely to own or influence the buying decision.
- Trigger signal: recent, source-backed event that makes outreach timely.
- Pain hypothesis: plausible business tension inferred from sourced facts; must be labeled as a hypothesis.
- Proof boundary: every factual claim traces to a URL or tool output.
- Contactable: a lead with a professional email verified or marked safe for manual review by `lead-enrichment`.

## Discovery Workflow

### 1. Convert the partner brief into an ICP

Extract or draft:
- target industries;
- company size/stage;
- geography;
- buyer personas;
- pain points;
- disqualifiers;
- trigger events that imply timing.

Completion criterion: the ICP can be written as filters plus search queries, and assumptions are explicitly labeled.

### 2. Generate search lanes

Create 3-6 independent lanes so discovery is not biased by one source:
- recent funding or growth;
- hiring/recruiting signals;
- product launches or new markets;
- leadership changes;
- content/podcast/event appearances;
- technology stack or website clues;
- competitor/customer ecosystem.

Completion criterion: each lane has concrete search queries and expected evidence.

Example web queries:

```text
site:techcrunch.com France B2B SaaS raised seed 2026
site:welcometothejungle.com "Head of Sales" "AI" "Paris"
"announces" "Series A" "B2B SaaS" "France"
"hiring" "VP Sales" "startup" "France"
```

### 3. Discover target accounts

For each account candidate, capture:
- company name;
- domain;
- market/segment;
- geography;
- source URL proving the account exists and matches the lane;
- signal URL proving why now.

Reject accounts with no source. If the domain is uncertain, mark it uncertain and do not enrich yet.

Completion criterion: each account has a domain or a clear `needs_domain_research` state.

### 4. Identify decision-makers

For each account, find 1-2 likely buyers based on the ICP:
- founder/CEO for early-stage startups;
- VP Sales / Head of Revenue for sales products;
- Head of Growth / Marketing for demand-gen products;
- COO / RevOps for process automation;
- CTO / Head of Engineering only when the pain is technical/integration-heavy.

Capture:
- first name;
- last name;
- title;
- profile/source URL;
- rationale for why this person is the likely buyer.

Completion criterion: every person has a sourced identity or is marked `decision_maker_unknown`.

### 5. Attach a trigger signal

A prospect is not ready without a real reason to contact them.

Good signals:
- fundraising in the last 12 months;
- active hiring for sales/growth/ops roles;
- new market/product launch;
- leadership appointment;
- public complaint/pain indicator;
- relevant content posted by the company or decision-maker;
- stack/tooling clue that connects to the partner's offer.

Bad signals:
- generic company description;
- old news with no current relevance;
- unsupported claims;
- vibes like "they probably need this".

Completion criterion: each candidate has a signal statement and a source URL, or is marked `research_more`.

### 6. Score fit before enrichment

Score each candidate from 0-100:

- ICP fit: 0-40
- signal strength: 0-30
- buyer confidence: 0-20
- timing/geography/compliance fit: 0-10

Prioritize only candidates scoring 70+ for Hunter.io enrichment unless the user asks for exploratory research.

Completion criterion: every candidate has a score and a short scoring rationale.

### 7. Hand off to lead-enrichment

For each prioritized candidate with domain + first name + last name, call the Hunter.io helper from `lead-enrichment`:

```bash
python3 /root/.hermes/profiles/ai-sales/skills/ai-sales/lead-enrichment/scripts/hunter_client.py lead-record \
  --company "COMPANY" \
  --domain "DOMAIN" \
  --first-name "FIRST" \
  --last-name "LAST" \
  --title "TITLE" \
  --linkedin-url "PROFILE_OR_SOURCE_URL" \
  --company-source-urls "COMPANY_SOURCE_URL" \
  --person-source-urls "PERSON_SOURCE_URL"
```

Use small batches to protect Hunter.io credits. If the task asks for 20 leads, discover and score more than 20 candidates first, then enrich the top 20 or the top candidates until 20 usable records exist.

Completion criterion: each enriched candidate has `email.status`, Hunter.io metadata, proof notes, and `next_action`.

### 8. Produce the prospect list

Return both human-readable summary and machine-readable JSON/CSV when useful.

Completion criterion: another agent can sync the output to CRM or draft a personalized message without guessing facts.

## Standard Output Schema

Use this shape for discovery results:

```json
{
  "partner": {
    "name": "",
    "offer": "",
    "website": "",
    "assumptions": []
  },
  "icp": {
    "industries": [],
    "geography": [],
    "company_stage": [],
    "buyer_personas": [],
    "disqualifiers": [],
    "trigger_events": []
  },
  "leads": [
    {
      "rank": 1,
      "score": 0,
      "score_rationale": "",
      "company": {
        "name": "",
        "domain": "",
        "source_urls": []
      },
      "person": {
        "first_name": "",
        "last_name": "",
        "title": "",
        "profile_url": "",
        "source_urls": []
      },
      "signal": {
        "type": "funding|hiring|launch|press|leadership|content|tech|other",
        "summary": "",
        "source_url": "",
        "observed_date": ""
      },
      "pain_hypothesis": "",
      "enrichment": {
        "email_status": "verified|probable|risky|not_found|not_contactable|not_enriched",
        "email_address": "",
        "hunter_score": null,
        "checked_at": ""
      },
      "next_action": "lead_enrichment|manual_review|research_more|discard|sync_to_crm"
    }
  ],
  "proof_notes": []
}
```

If saving files, prefer:

```text
/root/.hermes/profiles/ai-sales/workspace/prospect-runs/YYYY-MM-DD-partner-slug/
  discovery.json
  discovery.csv
  sources.md
  README.md
```

## Output Quality Bar

A lead is demo-ready only if:
- the company is real and sourced;
- the person is real and sourced;
- the signal is real, recent, and sourced;
- the pain hypothesis follows from the evidence;
- Hunter.io enrichment was attempted when enough data existed;
- email status is explicit;
- no outreach is sent automatically;
- `next_action` is safe and explicit.

For the challenge, 10 excellent leads beat 100 generic leads. Never pad the list with weak prospects.

## Search and Evidence Rules

- Prefer primary sources: company site, careers page, press release, official blog, regulatory/company registry, funding announcement, credible media.
- Use secondary sources only when primary sources are unavailable and label them.
- Store URLs, not just snippets.
- Record the date of observation when possible.
- If a source disappears or is behind a login wall, do not rely on it as the sole proof.

## GDPR and Platform Guardrails

- Use public professional information only.
- Do not scrape LinkedIn/Instagram behind authentication or at scale.
- Respect opt-out state once CRM exists.
- Treat EU prospects conservatively: clear legitimate interest, relevance, and opt-out are mandatory before outreach.
- Keep discovery separate from sending; cold sends require human validation at this stage.

## Common Pitfalls

1. Starting with Hunter.io before knowing who to target.
   - Fix: discover and score accounts first; enrich only prioritized candidates.

2. Treating a company as a lead without a person.
   - Fix: either identify a decision-maker or mark `decision_maker_unknown`.

3. Using generic personalization.
   - Fix: every lead needs a specific signal and source.

4. Over-enriching low-fit accounts.
   - Fix: score before spending Hunter.io credits.

5. Hiding uncertainty.
   - Fix: use explicit states like `research_more`, `not_enriched`, and proof notes.

6. Confusing source URLs with proof.
   - Fix: the URL must actually support the specific claim made.

## Verification Checklist

- [ ] Partner brief converted into ICP filters and assumptions.
- [ ] Search lanes cover at least 3 independent discovery angles.
- [ ] Every account has a domain or explicit domain uncertainty.
- [ ] Every decision-maker has a sourced identity or `decision_maker_unknown`.
- [ ] Every demo-ready lead has a recent trigger signal with source URL.
- [ ] Every lead has a score and rationale.
- [ ] Hunter.io enrichment is used only after candidate prioritization.
- [ ] Output follows the standard schema or explains deviations.
- [ ] No outreach was sent.
- [ ] Weak or unsourced candidates are excluded instead of padded.
