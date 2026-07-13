# Challenge brief alignment workflow

Use this when building or extending an Hermes `ai-sales` profile for an external challenge, evaluation, or demo brief.

## Lesson

Do not treat the first prospecting run (for example, “20 leads for a partner”) as the whole challenge. In the Orchestra-style AI Sales Company brief, the partner run is only the proof case for a broader product: prospecting, personalization, CRM, human review, scheduling, reporting, and orchestration.

## Workflow

1. Locate the authoritative challenge brief before planning work.
   - Search likely project/profile roots for `CHALLENGE.md`, `README.md`, or equivalent.
   - If the profile README references a challenge file that is outside the profile, copy or link it into the profile workspace so future sessions have it locally.

2. Create a challenge-to-implementation checklist.
   - Map every explicit requirement to one of: `done`, `partial`, `missing`, or `deferred`.
   - Include evaluation criteria / point weights when present.
   - Break the work into the brief’s own milestones rather than inventing a narrower plan.

3. Keep the partner demo separate from the product build.
   - Partner brief / ICP / leads are the case study.
   - Skills, CRM, review queue, orchestration, and reporting are the reusable product.

4. Recommended workspace files:

```text
workspace/CHALLENGE.md
workspace/challenge-checklist.md
workspace/partner-brief-<slug>.md
workspace/prospect-runs/<date>-<partner>/
workspace/crm/
workspace/review-queue/
workspace/reports/
```

5. Checklist sections to include:
   - exact objective from the brief;
   - scoring rubric;
   - target architecture;
   - real current state;
   - done / partial / missing;
   - milestone plan;
   - expected deliverables;
   - immediate next action;
   - non-negotiable guardrails.

## Pitfall

If the user pushes back with “what about the rest of the challenge?” or asks whether the challenge file is present, stop summarizing from memory. Inspect the actual brief, anchor the plan to it, and update the workspace checklist before continuing.
