# Five-Team AI Sales Company Buildout Pattern

Use this reference when the user is building an Hermes `ai-sales` profile for a challenge or product demo that expects a full AI Sales Company, not only prospect generation.

## Lesson captured

Do not collapse the work into “20 leads” just because the immediate demo partner is known. The 20-lead run is only the S1 proof. The class-level product must visibly implement the five teams and the end-to-end operating model.

If the user pushes back with “there are 5 teams” or “the rest of the challenge,” switch from lead-list mode to company-operating-system mode.

## Recommended sequence

1. Put the challenge brief where the profile can use it.
   - Copy or link `CHALLENGE.md` into `~/.hermes/profiles/<profile>/workspace/CHALLENGE.md` when available.
   - Create `workspace/challenge-checklist.md` mapping: brief requirement → current status → missing work → deliverable.

2. Create the company operating system before deeper run work.
   - `workspace/company/teams.md`
   - `workspace/company/operating-model.md`
   - `workspace/company/handoffs.md`
   - `workspace/team-1-prospection-intelligence/README.md`
   - `workspace/team-2-outreach-engagement/README.md`
   - `workspace/team-3-admin-rdv/README.md`
   - `workspace/team-4-content-marketing/README.md`
   - `workspace/team-5-crm-orchestration/README.md`

3. Establish the local source of truth early.
   - `workspace/crm/accounts.json`
   - `workspace/crm/contacts.json`
   - `workspace/crm/interactions.json`
   - `workspace/crm/opportunities.json`
   - `workspace/crm/opt_outs.json`

4. Fill only the priority skill gaps first.
   - Already typical: `prospect-discovery`, `lead-enrichment`.
   - Add core MVP: `icp-builder`, `lead-scoring`, `crm-sync`, `message-personalization`, `pipeline-report`, `daily-orchestration`.
   - Leave channel-specific or secondary skills (`linkedin-outreach`, `instagram-outreach`, `meeting-scheduler`, etc.) for later unless integrations are already available.

5. Then run the partner demo end-to-end.
   - Partner brief → ICP → candidates → 20 sourced leads → scoring/enrichment → CRM sync → review-ready messages → content/audits → meeting handoff simulation → pipeline report → orchestration digest.

## Pitfall

Starting with external integrations or raw lead volume makes the system look like a script. For this challenge class, the stronger proof is: five teams, handoffs, CRM state, proof boundary, human review, and one partner passing through the complete loop.
