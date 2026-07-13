# Five-Team Local-First AI Sales Company Demo

Use this reference when building an AI Sales Company challenge/demo where the brief asks for a complete sales organization, not only lead generation.

## Key lesson

Do not collapse the work into “20 leads”. Lead discovery is only the Prospection & Intelligence proof point. The demo should show all five teams and an end-to-end handoff loop, even when external integrations are not yet configured.

## Required five-team framing

1. Prospection & Intelligence
   - ICP, accounts, decision-makers, signals, pain hypotheses, enrichment, scoring.
2. Outreach & Engagement
   - personalized messages, email sequence drafts, LinkedIn/Instagram drafts, reply triage, objections.
3. Admin & Rendez-vous
   - positive-reply handling, proposed slots, no-show/follow-up cadence, handoff brief.
4. Content & Marketing
   - express audits, personalized offers, value-before-ask assets.
5. CRM & Orchestration
   - source of truth, dedupe, opt-outs, daily loop, pipeline digest.

## Recommended local-first MVP

Before wiring Slack/Gmail/Resend/LinkedIn/Instagram/HubSpot, build a local proof that the system works:

```text
workspace/company/
  teams.md
  operating-model.md
  handoffs.md
workspace/team-1-prospection-intelligence/README.md
workspace/team-2-outreach-engagement/README.md
workspace/team-3-admin-rdv/README.md
workspace/team-4-content-marketing/README.md
workspace/team-5-crm-orchestration/README.md
workspace/crm/
  accounts.json
  contacts.json
  interactions.json
  opportunities.json
  opt_outs.json
workspace/review-queue/
  pending/
  approved/
  rejected/
  needs-research/
workspace/content-assets/
  audits/
  offers/
workspace/meetings/
workspace/reports/
workspace/demo/
  runbook.md
  transcript.md
```

## Skills to prioritize

Start with the minimum class-level skill map, not a long list of one-off run skills:

- `icp-builder`
- `prospect-discovery`
- `signal-detection`
- `pain-mapping`
- `lead-enrichment`
- `lead-scoring`
- `message-personalization`
- `email-sequencing`
- `reply-triage`
- `objection-handling`
- `meeting-scheduler`
- `followup-cadence`
- `handoff-brief`
- `marketing-audit`
- `personalized-offer`
- `crm-sync`
- `daily-orchestration`
- `pipeline-report`

LinkedIn/Instagram skills can exist in preparation-only mode unless compliant integrations are configured.

## Proof boundary for early demos

- Do not invent decision-makers.
- Do not invent emails.
- Do not spend enrichment credits unless there is a reliable domain and a sourced person.
- If Hunter.io cannot be used safely, record `not_found` or `research_more` and explain why.
- A local review queue is an acceptable MVP for “human in the loop” when Slack is not wired yet, but state clearly that Slack is not actually connected.
- Local JSON CRM is acceptable for the first demo when external CRM is not configured, but call it a local MVP.

## Demo flow

```text
Partner brief
  → ICP
  → discovery candidates
  → 20 selected sourced leads
  → CRM local sync
  → 5 review-ready personalized drafts
  → 2-3 content audits/offers
  → 1 positive-reply meeting handoff simulation
  → pipeline report
  → daily orchestration digest
  → runbook/transcript
```

## User steering pattern

If the user pushes back that “the rest of the challenge” is missing, immediately re-anchor on the challenge brief and the five teams. Do not defend the lead-only plan. Treat the pushback as a workflow correction and expand the plan to cover the full operating model.
