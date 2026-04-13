# JIRA INTEGRATION GUIDE

## Recommended architecture

### Layer 1: Intake skill
- judge whether feedback is dispatchable
- identify missing information
- separate missing-info from needs-product-decision
- normalize title and description
- suggest priority and assignee
- require source of truth for expected behavior when the request is not a pure bug
- keep the core workflow in `SKILL.md` and detailed judgment rules in split `references/` files

### Layer 2: Connector scripts or MCP
- create Jira issues
- update Jira issues
- comment back to Jira issues
- move Jira status
- look up metadata

### Layer 3: Team-private config
- base URL
- project key
- issue type mapping
- transition ids
- assignee mapping
- custom field ids

## Recommended flow

1. Raw feedback enters intake skill
2. Skill immediately produces a draft; if the input is genuinely ambiguous, it asks one follow-up question before drafting
3. User confirms the draft
4. If the ticket is blocked or needs-product-decision, generate a structured clarification comment
5. If the source is an existing Jira issue, write the clarification comment back
6. Generate Jira payload and run `create_jira_issue.py`
7. Run `validate_jira_payload.py` only when debugging a failed create
8. Later, if work is completed, run `transition_jira_issue.py`

Do not send items that are flagged as blocked or needs-product-decision straight into the dev queue.

## MCP vs scripts

### If Jira MCP exists
Use MCP as transport.
Keep the skill responsible for readiness checks and payload shaping.
Do not couple the business rules to one MCP implementation.

### If Jira MCP does not exist
Use the provided Python scripts against Jira REST API.
This is simpler to share and easier to audit.

The scripts now support:
- retry with exponential backoff on transient Jira failures
- validation before create/update
- transition resolution by id, logical key, or status name
- explicit Jira comment write-back for blocked or decision-needed items

## Required secrets

Do not commit real secrets.
Recommended runtime secrets:
- JIRA_API_TOKEN

Recommended private config values:
- Jira base URL
- bot email
- project key
- transition ids
- internal assignee accountId mapping
- custom field ids

## What belongs in the public repo

Safe to include:
- SKILL.md
- generic references
- example config files
- generic scripts
- generic payload templates
- package sync script

Do not include:
- real tokens
- real accountId mappings
- private project internals

## Data security boundary

### Content that must not be sent to external models in full

Some Jira tickets and raw feedback contain sensitive content that must not be forwarded to external AI models or retained in logs without redaction. Before processing, check whether the input contains any of the following:

- User personal data: name, email, phone number, address
- Order IDs, transaction references, or invoice numbers
- Payment-related errors, amounts, card details, or flow screenshots
- Internal credentials, API keys, or access tokens mentioned in bug context
- Screenshots or attachments that contain any of the above

If sensitive content is present:
- Pass only the minimum context needed for intake classification
- Redact or summarize sensitive fields before sending to the model
- Do not log the full raw payload or raw model response

### What must not appear in logs

- Full Jira ticket bodies when they contain personal or financial data
- Raw model responses that echo back sensitive input
- JIRA_API_TOKEN, auth headers, or credentials in any form
- accountId mappings if they are considered internal

### Transport boundary

When using Jira MCP: the MCP server handles credentials. Do not pass JIRA_API_TOKEN or base URL into model context — they are not needed for intake logic.

When using scripts: token is injected via env var at runtime. Do not embed it in the payload JSON file or in any log output.

## Future extension

Later you can add:
- auto-create subtasks
- board-specific transition helpers
- release-aware priority tuning
- analytics on common missing feedback patterns

## Package snapshot

Treat root as the source of truth.
Use the root repo as the single source of truth. If you later need a distributable artifact, package it from root instead of maintaining two copies by hand.
