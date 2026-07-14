# Troubleshooting Email Sending (CLI Environment)

This session identified that standard email CLI tools (`himalaya`, `sendmail`, `mail`) are unavailable in this environment. 

## Actionable Alternatives

1. **Copy/Paste Workflow**: Use the `workspace/review-queue/pending/` drafts for manual email dispatch.
2. **CRM Sync**: If a CRM integration exists (e.g., via `crm-sync` skill), push draft records directly to the CRM for team dispatch.
3. **Environment setup**: If programmatic sending is required, setup the `himalaya` skill (requires installed CLI binary and authenticated config).

Do NOT attempt to use `himalaya` or `sendmail` commands until verified installed in the current environment.
