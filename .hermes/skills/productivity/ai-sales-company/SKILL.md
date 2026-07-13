---
name: ai-sales-company
description: "Use when building or extending an Hermes profile that acts as an AI sales organization: prospect discovery, lead enrichment, proof-backed outreach preparation, CRM-ready records, and human-review workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sales, prospecting, lead-enrichment, hermes-profiles, hunter-io, crm, outreach]
    related_skills: [hermes-agent, hermes-agent-skill-authoring, google-workspace, airtable]
---

# AI Sales Company

## Overview

Use this skill to build a class-level AI sales organization inside Hermes: a profile with doctrine, sales skills, external enrichment tools, proof boundaries, and CRM/outreach handoffs.

The core product standard is not volume. The standard is a traceable pipeline where each lead has a real account, a real decision-maker, a recent sourced signal, an explicit contactability state, and a safe next action.

Doctrine: This profile must always follow `sales:soul`.

Reference from the session that motivated this skill: `references/hunter-lead-enrichment.md`.

Reference for challenge/evaluation alignment: `references/challenge-brief-alignment.md`.

Reference for full five-team challenge buildouts: `references/five-team-challenge-buildout.md`.

Reference for the local-first five-team MVP pattern (when Slack/Gmail/CRM/LinkedIn integrations are not ready yet): `references/five-team-local-first-demo.md`.

## When to Use

Use this skill when the user asks to:
- create or improve an AI sales profile in Hermes;
- build prospecting or lead-enrichment workflows;
- integrate Hunter.io, Apollo-like enrichment, CRM, Slack validation, Gmail, or similar sales tools;
- design sales-agent skills such as `prospect-discovery`, `lead-enrichment`, `message-personalization`, `crm-sync`, or `daily-orchestration`;
- prepare a demo with sourced B2B leads and human-reviewed outreach.

Do not use this skill for generic copywriting, one-off email drafting, or unsourced lead-list generation.

## Target Architecture

Treat the profile as a sales company with five teams:

1. Prospection & Intelligence — ICP, target accounts, decision-makers, trigger signals, pain hypotheses, scoring.
2. Outreach & Engagement — personalized messages, sequences, reply triage, objections.
3. Admin & Rendez-vous — slots, calendar, no-show follow-up, meeting briefs.
4. Content & Marketing — audits, one-pagers, custom value assets.
5. CRM & Orchestration — source of truth, dedupe, opt-outs, daily loop, reporting.

Recommended workflow:

```text
partner brief
  → ICP
  → prospect-discovery
  → scored accounts + decision-makers + trigger signals
  → lead-enrichment / Hunter.io
  → verified/probable/risky/not_found email status
  → CRM/source of truth
  → message-personalization
  → human review
  → approved outreach only
```

## Setup Workflow

1. Inspect the profile before editing.
   - Check `~/.hermes/profiles/<name>/SOUL.md`, existing skills, MCP servers, toolsets, and `.env` key names without printing secret values.
   - Completion criterion: you know whether the profile already has doctrine, sales skills, and required tool access.

2. Strengthen the doctrine.
   - `SOUL.md` should define identity, non-negotiables, teams, workflow, statuses, and output standards.
   - Include proof boundaries, personalization, human-in-the-loop, GDPR, and deliverability.
   - Completion criterion: a fresh session of the profile knows how to behave before any chat instructions.

3. Build class-level sales skills.
   - Prefer reusable skills under `~/.hermes/profiles/<name>/skills/ai-sales/<skill>/SKILL.md` or the appropriate profile-local category.
   - Start with `prospect-discovery` and `lead-enrichment` before outreach automation.
   - Completion criterion: each skill has a rich SKILL.md, exact commands, safety rules, standard output schema, pitfalls, and verification checklist.

4. Add helper scripts only for deterministic API work.
   - Scripts should read credentials from environment or profile `.env` fallback, never from command-line arguments.
   - Output JSON, redact/omit secrets, and include metadata needed for CRM handoff.
   - Completion criterion: scripts have `--help`, fail cleanly when credentials are missing, and can be tested without spending credits when possible.

5. Create workspace structure.
   - Recommended directories:
     ```text
     ~/.hermes/profiles/<name>/workspace/prospect-runs/
     ~/.hermes/profiles/<name>/workspace/crm/
     ~/.hermes/profiles/<name>/workspace/review-queue/
     ~/.hermes/profiles/<name>/workspace/reports/
     ```
   - For challenge-style builds, also create the five-team operating system before treating a partner run as the main deliverable:
     ```text
     ~/.hermes/profiles/<name>/workspace/company/teams.md
     ~/.hermes/profiles/<name>/workspace/company/operating-model.md
     ~/.hermes/profiles/<name>/workspace/company/handoffs.md
     ~/.hermes/profiles/<name>/workspace/team-1-prospection-intelligence/
     ~/.hermes/profiles/<name>/workspace/team-2-outreach-engagement/
     ~/.hermes/profiles/<name>/workspace/team-3-admin-rdv/
     ~/.hermes/profiles/<name>/workspace/team-4-content-marketing/
     ~/.hermes/profiles/<name>/workspace/team-5-crm-orchestration/
     ```
   - Completion criterion: future runs have obvious places for JSON/CSV/sources/reports, and the five teams have documented responsibilities and handoffs.

6. Verify with small, cheap probes.
   - First test account/quota or dry-run paths.
   - Then test one domain search.
   - Then verify one email.
   - Only then run larger lead generation.
   - Completion criterion: the integration is proven end-to-end without wasting API credits.

## Hunter.io Pattern

Hunter.io is best treated as an enrichment source, not as the prospecting brain.

Recommended command set for a helper:
- `account` — prove the key and quota work.
- `domain-search` — explore contacts/patterns for a domain.
- `email-finder` — find a person-domain email.
- `email-verifier` — verify before CRM/outreach.
- `lead-record` — package finder + verifier into a CRM-ready proof-backed record.

Contactability states:
- `verified` — verified professional email, still requires human validation before cold send.
- `probable` — found but needs manual review.
- `risky` — do not send; research more.
- `not_found` — no email; do not guess.
- `not_contactable` — invalid, personal/webmail, opt-out, blocked, or non-compliant.

Important nuance: Hunter.io `type: personal` often means nominative professional email rather than generic role inbox. Confirm the domain and avoid treating a company-domain nominative address as private merely because Hunter uses `personal`.

## Standard Lead Record

Use a CRM-ready structure like:

```json
{
  "company": {"name": "", "domain": "", "source_urls": []},
  "person": {"first_name": "", "last_name": "", "title": "", "linkedin_url": "", "source_urls": []},
  "signal": {"type": "", "summary": "", "source_url": "", "observed_date": ""},
  "email": {"address": "", "status": "verified|probable|risky|not_found|not_contactable", "hunter_score": null, "hunter_sources": []},
  "proof": {"tools_used": [], "checked_at": "", "notes": []},
  "next_action": "manual_review|research_more|discard|sync_to_crm"
}
```

If a field is unknown, leave it empty/null and explain why in proof notes. Do not fill gaps with plausible guesses.

## Challenge Brief Alignment

When this work is for a challenge, evaluation, or take-home brief, first anchor the profile to the actual brief before building more features.

1. Locate the authoritative challenge file (`CHALLENGE.md`, project README, or equivalent). If it lives outside the profile but the profile references it, copy or link it into `~/.hermes/profiles/<name>/workspace/`.
2. Create `workspace/challenge-checklist.md` mapping the brief to the real implementation state: objective, scoring rubric, target architecture, `done`, `partial`, `missing`, milestones, deliverables, and guardrails.
3. Keep the partner run separate from the product build: a 10-20 lead run proves the prospecting case, but the challenge often also requires CRM, personalization, human review, scheduling, reporting, and orchestration.
4. Use the checklist to decide the next action instead of inferring from memory or from a partial README.

See `references/challenge-brief-alignment.md` for the reusable checklist workflow.

## Demo Sequence

For an evaluation/demo, build in this order:

1. Profile doctrine (`SOUL.md`) and README.
2. Challenge brief copied/linked into the workspace plus a `challenge-checklist.md`.
3. Five-team operating system: `company/teams.md`, `company/operating-model.md`, `company/handoffs.md`, and one workspace folder per team.
4. Core class-level skills for the MVP company: `icp-builder`, `prospect-discovery`, `lead-enrichment`, `lead-scoring`, `crm-sync`, `message-personalization`, `pipeline-report`, `daily-orchestration`.
5. Local CRM source of truth.
6. First 10-20 sourced leads with signals and enrichment state.
7. `message-personalization` outputs and human review queue.
8. Content/audit, meeting-handoff simulation, pipeline report, and orchestration digest.
9. Slack/Gmail/CRM integrations only after the local loop is coherent.

Do not start by wiring outreach. A demo with excellent sourced leads is stronger and safer than a shallow automation that sends messages. Do not confuse the first lead run with the full challenge deliverable; the five teams and CRM/orchestration loop must be visible.

## Common Pitfalls

1. Starting with email enrichment before deciding who is worth contacting.
   - Fix: score accounts and decision-makers first, then spend enrichment credits.

2. Letting API output become unsourced claims.
   - Fix: preserve source URLs and the specific field each source supports.

3. Passing secrets in commands.
   - Fix: read from `.env`/environment; never pass API keys in argv or examples.

4. Treating “found” as “safe to email.”
   - Fix: verify email and still set `manual_review` before cold outreach.

5. Creating many narrow one-off skills.
   - Fix: keep class-level skills (`prospect-discovery`, `lead-enrichment`, `message-personalization`) and put run-specific details under `references/` or workspace run folders.

6. Padding lead lists.
   - Fix: exclude weak/unsourced candidates; quality beats count.

7. Treating a partner prospecting run as the whole challenge.
   - Fix: inspect the actual challenge brief and maintain `workspace/challenge-checklist.md`; the lead run is only one proof point inside the broader sales-company product.

8. Under-building the five teams after a user explicitly references them.
   - Fix: stop proposing incremental lead-list work and build the class-level operating system first: five team folders, team responsibilities, handoffs, local CRM, and the core orchestration/reporting skills.

## Verification Checklist

- [ ] Profile doctrine captures proof, personalization, human review, GDPR, deliverability.
- [ ] Sales skills are reusable and profile-local when the profile is the product artifact.
- [ ] Helper scripts do not expose secrets and have clear `--help`.
- [ ] API integration tested with a cheap account/domain/verifier sequence.
- [ ] Lead records include sources, contactability status, and safe `next_action`.
- [ ] No outreach is sent automatically during early setup/demo.
- [ ] Workspace has prospect-runs, CRM, review-queue, and reports directories.
- [ ] Challenge/evaluation builds show all five teams, not only the lead-generation run.
- [ ] If real Slack/Gmail/Resend/CRM/LinkedIn/Instagram integrations are not configured, the demo labels local substitutes honestly: review queue, JSON CRM, prepared drafts, and simulated handoff.
