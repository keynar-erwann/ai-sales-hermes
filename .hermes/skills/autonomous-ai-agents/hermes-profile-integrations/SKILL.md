---
name: hermes-profile-integrations
description: "Configure third-party APIs and external capabilities for a specific Hermes profile without leaking secrets or editing the wrong profile."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, profiles, integrations, api, mcp, skills, env]
    related_skills: [hermes-agent]
---

# Hermes Profile Integrations

Use this skill when the user wants a named Hermes profile to use a new external service/API/MCP, especially when the profile is intended to behave like a specialized agent or team.

This skill is for the repeatable workflow around profile-scoped integrations. For canonical CLI syntax, always consult the protected `hermes-agent` skill or the official Hermes docs first.

## Core principle

A profile integration is not just an API key. It should connect four things:

1. Profile scope: the target profile under `~/.hermes/profiles/<name>/`.
2. Credentials: stored only in that profile's `.env` or auth store, never in chat or skills.
3. Capability: toolset, MCP server, plugin, script, or skill procedure that can call the service.
4. Operating doctrine: proof boundaries, safety rules, validation/human-in-loop rules, output schema.

## Workflow

1. Load `hermes-agent` first.
   - Profiles, tools, MCP, env layout, and restart behavior are Hermes-specific.
   - Treat official docs as source of truth if command syntax differs.

2. Identify the target profile and inspect before modifying.
   - `hermes profile show <name>`
   - Read the profile's `SOUL.md` if relevant.
   - List profile skills and search for existing domain skills before creating new ones.
   - Check enabled toolsets for the platform that will run the profile.
   - Check MCP list for that profile.
   - Inspect `.env` only by listing variable names/presence, never values.

3. If the user provided a brief/challenge/spec file, read it before design.
   - Derive the integration's product role from the brief.
   - Example: a lead enrichment API belongs in a `lead-enrichment` or prospecting skill, not as a random generic API note.

4. Propose the integration boundary before editing.
   - What credential name is required.
   - Which skill/script/plugin/MCP will use it.
   - What the agent is allowed and forbidden to do.
   - How results are verified.
   - What remains manual/human-approved.

5. Store secrets profile-locally.
   - Preferred: `~/.hermes/profiles/<name>/.env` for simple API keys.
   - Use clear env var names such as `HUNTER_API_KEY`, `RESEND_API_KEY`, etc.
   - Never write the user's secret yourself unless they explicitly provide it through an approved secret mechanism. Usually ask the user to paste it into the profile `.env` locally.

6. Add durable capability at the right layer.
   - If a reliable MCP exists: configure it profile-scoped and enable only required tools.
   - If no MCP exists: create/update a domain skill and optionally add a helper script under that skill's `scripts/` directory.
   - If repeated structured calls are needed: prefer a small script that reads env vars and emits JSON over hand-typed curl commands in every session.

7. Verify safely.
   - First verify prerequisites without exposing secrets.
   - Then, after the user confirms the key is set, run a low-impact endpoint or account/status call.
   - Report HTTP status and redacted/summary output only.
   - Never print API keys, OAuth tokens, cookies, or full secret-bearing URLs.

8. Document restart requirements.
   - Tool and config changes usually require a new Hermes session or `/reset`.
   - Gateway/profile service changes may require gateway restart.

## Profile-scoped inspection checklist

Use this checklist before edits:

- Target profile path exists.
- `SOUL.md` read and understood.
- Profile description checked if orchestration/kanban will use it.
- Existing relevant skills searched.
- Toolsets checked for the target platform.
- MCP servers listed.
- `.env` presence checked and only variable names reported.
- External API reachability checked without a real key when safe.
- User explicitly approves modifications after the inspection/design step.

## Pitfalls

- Do not treat an integration as complete just because a key exists. The profile still needs a skill/tool/script/MCP that knows when and how to use it.
- Do not put API keys into `SOUL.md`, `SKILL.md`, README files, shell history, or chat replies.
- Do not modify another profile's skills/plugins/cron/memories unless the user explicitly directs it. Cross-profile writes change a different agent.
- Do not create narrow one-off skills named after a vendor alone when the durable class is a workflow. Prefer domain skills such as `lead-enrichment`, `email-sequencing`, or `crm-sync`; vendor details can live in references or scripts.
- Do not skip the brief/spec. User-provided challenge files often define non-negotiable product rules such as proof boundaries or human approval.

## Support files

- `references/hunter-io-ai-sales.md` — notes for integrating Hunter.io as an enrichment provider inside an AI sales Hermes profile.
