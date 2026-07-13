---
name: message-personalization
description: "Use when turning a sourced lead, signal, and pain hypothesis into a concise human outreach draft that must pass manual review before sending."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sales, outreach, personalization, ai-sales]
    related_skills: [crm-sync, email-sequencing]
---

# Message Personalization

## Overview

Turns proof-backed lead records into concise, human messages. The goal is not clever copy; it is relevance that feels like a strong commercial wrote it after doing real research.

## When to Use

Use after a lead is qualified/scored and before human review.

Do not use when the lead has no real signal. Route to `research_more` instead.

## Message Standard

A good message must include:

- one specific observation from a source;
- one plausible pain hypothesis;
- one relevant bridge to the partner offer;
- one simple ask;
- no fake urgency, no generic flattery.

## Procedure

1. Read the lead record and sources.
   - Completion criterion: account, persona, signal and pain hypothesis are known.
2. Pick one angle.
   - Completion criterion: the angle is traceable to a source URL.
3. Draft a short email.
   - Completion criterion: under ~120 words unless the user asks otherwise.
4. Draft optional LinkedIn/Instagram variants only if appropriate.
   - Completion criterion: drafts are channel-specific, not copy-paste.
5. Add review metadata.
   - Completion criterion: output status is `manual_review`, never `send`.
6. Save to review queue.
   - Completion criterion: a `.md` file exists in `workspace/review-queue/pending/`.

## Output Template

```markdown
# Review Item — <Account>

Status: manual_review
Risk: low|medium|high
Lead source:
Signal source:

## Angle

## Email draft

## LinkedIn draft optional

## Why this is personalized

## Human reviewer notes
```

## Common Pitfalls

1. Generic praise. Fix: cite the concrete observation.
2. Too many angles. Fix: one message, one reason to reply.
3. Sending automatically. Fix: always route to review queue.

## Verification Checklist

- [ ] Message uses a real signal.
- [ ] Message would not work unchanged for 100 prospects.
- [ ] Draft is in `manual_review`.
- [ ] No unsupported claims.

