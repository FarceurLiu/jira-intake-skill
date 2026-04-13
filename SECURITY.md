# Security Policy

## Scope

This repo is a macOS-first skill and script bundle for Jira intake workflows.
Please treat the following as sensitive:

- Jira API tokens
- private config files
- Jira account IDs if your team treats them as internal
- internal workflow mappings or owner-assignment rules that identify team structure
- screenshots or payloads containing user PII, transaction identifiers, or financial details
- real production examples copied from customer reports, support cases, or incident tickets

## Reporting a Vulnerability

Do not open a public issue with secrets, tokens, private config, or sensitive Jira payloads.

For suspected security issues:

1. Prepare a minimal, redacted reproduction.
2. Contact the maintainer privately first through GitHub.
3. Wait for confirmation before public disclosure.

For non-sensitive bugs or documentation issues, use the normal issue tracker.

## Safe Reporting Guidelines

- Never include real `.env` contents.
- Never include `config/team-config.private.json`.
- Redact Jira base URLs if they are internal-only.
- Redact user data from screenshots and ticket payloads.
- Replace real examples with synthetic examples before committing docs or tests.
