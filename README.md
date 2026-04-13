# jira-intake-skill

Turn messy product feedback into dispatchable Jira drafts — with explicit intake judgment before any Jira write-back.

[繁體中文](./README.zh-TW.md)

> Current support target: macOS with a local terminal environment.
> Draft mode works after skill install. Direct Jira execution requires `python3` plus private Jira setup.
> This project is not affiliated with or endorsed by Atlassian, Anthropic, or OpenAI.
> Best for users comfortable with agent-based workflows and occasional local terminal setup.

## What this repo is

This is an intake-governance skill for teams that receive raw bug reports, QA findings, UX issues, and product feedback that are not ready to dispatch.

Its core value is not Jira ticket generation. It is:
- separating missing-info from product-decision gaps
- deciding whether an item is ready to dispatch
- producing a clean, confirmed draft before anything is written to Jira
- falling back to manual output when no writable Jira path exists

Direct Jira execution is optional and only runs after explicit user confirmation.

## Open-source boundary

This repo is intended to stay open-source safe.
Keep it generic: no private Jira config, no real accountId mappings, no organization-specific workflow rules, and no real customer or production examples.

## At a glance

| Capability | Works after install | Extra requirement |
|---|---|---|
| Turn raw feedback into a Jira draft | Yes | None |
| Detect blocked vs ready vs needs-product-decision | Yes | None |
| Generate clarification comments for follow-up | Yes | None |
| Create / update / transition Jira issues directly | No | Jira MCP or scripts + private config |

## Requirements

- Draft mode: a supported agent environment such as Claude Code or OpenAI Codex
- Scripts path: `python3` (not auto-installed by this repo), Jira API token, and private config files
- Jira MCP path: a connected Jira-capable environment

## Default safety model

By default, this skill produces drafts first.
It does not write to Jira unless a writable path is available and the user has explicitly confirmed the draft.

If Jira connectivity is missing, broken, or partially configured, the skill falls back to manual output instead of skipping intake judgment.
Sensitive data — user PII, transaction references, and financial details — is flagged before dispatch.

## When it will not auto-dispatch

The skill stays in draft mode and does not write to Jira when:
- the issue itself cannot be identified
- the report mixes multiple unrelated issues that cannot be separated
- expected behavior depends on an unconfirmed product or design decision
- the report may contain sensitive data that should be reviewed first
- no writable Jira path is available

## Who it is for

Useful for:
- PMs
- QAs
- designers
- cross-functional teammates
- engineers who want cleaner intake before triage

You do **not** need Jira API knowledge to use draft mode.

## What it can do

### Zero-setup mode
No Jira connection required.

- analyze raw feedback
- classify bug / request / spec-fix / UX-adjustment
- detect blocked vs ready vs needs-product-decision
- produce a draft ticket
- produce clarification comments for follow-up

### Connected mode
Requires Jira MCP or scripts + private config.

- create Jira issues
- update Jira issues
- post Jira comments
- transition issue status
- look up projects, boards, sprints, and assignable members

## What it does not do

- It is not a background Jira automation bot.
- It is not a neutral or universal Jira standard. It reflects an opinionated intake-governance approach.
- It does not replace product decisions.
- It does not guess unclear expected behavior without evidence.
- It does not ship your private Jira config.
- It does not support other trackers like Linear or GitHub Issues today.

## Repo layout

| Path | Purpose |
|---|---|
| `SKILL.md` | main skill entry point |
| `references/` | split intake rules, templates, examples |
| `templates/` | reusable output templates |
| `scripts/` | optional Jira REST helpers |
| `config/` | public config examples only |
| `docs/` | onboarding, setup, troubleshooting |
| `tests/` | regression cases for intake judgment |

## Quick start

### Option A: use draft mode only
1. Install the skill using the standard path in the Installation section below.
2. Start a new Claude Code or Codex session so the skill reloads.
3. Paste raw feedback and ask it to turn it into a Jira draft.

Example prompts:
- `Help me turn this bug report into a Jira ticket`
- `幫我整理這個反饋，看看能不能發派`
- `Turn this QA finding into a dispatchable Jira issue`
- `Use jira-intake to normalize this feedback`

### Option B: enable direct Jira execution
1. Copy the private config sample:
   ```bash
   cp config/team-config.example.json config/team-config.private.json
   ```
2. Fill in your Jira base URL, project key, and email.
3. Create `config/.env` with your API token:
   ```bash
   cat > config/.env <<'EOF'
   JIRA_API_TOKEN=your-token-here
   EOF
   ```
4. Verify the connection:
   ```bash
   python3 scripts/jira_lookup_metadata.py config/team-config.private.json projects
   ```

For guided setup, see `docs/zh-TW/CONFIG_SETUP.md` and `docs/zh-TW/JIRA_TOKEN_SETUP.md`.

## Installation

Clone this repo into your agent's skill directory.
For public/open-source usage, use the standard per-agent skill path instead of an arbitrary folder such as `~/skills`.

Recommended install paths:

For Claude Code:

```bash
git clone https://github.com/FarceurLiu/jira-intake-skill.git ~/.claude/skills/jira-intake
```

For OpenAI Codex:

```bash
git clone https://github.com/FarceurLiu/jira-intake-skill.git "${CODEX_HOME:-$HOME/.codex}/skills/jira-intake"
```

Notes:
- Keep the folder name as `jira-intake` unless you intentionally want a different skill name.
- After install or update, start a new session so the agent reloads skills.
- Draft-only mode works immediately after install. Direct Jira execution still requires Jira MCP or the private scripts setup described above.

Quick verification:
- Ask: `Turn this bug report into a Jira draft`
- Or explicitly mention the skill name: `Use jira-intake to normalize this feedback`

Update later with:

```bash
git -C ~/.claude/skills/jira-intake pull
git -C "${CODEX_HOME:-$HOME/.codex}/skills/jira-intake" pull
```

## Security notes

Do not commit:
- real API tokens
- `config/team-config.private.json`
- `config/.env`
- real Jira account IDs if your team treats them as internal
- internal-only workflow mappings you do not want to expose
- real customer feedback, screenshots, transaction references, incident details, or copied production payloads

The repo already ignores private config and `.env` files.

Connected mode presents human-readable choices only. Internal identifiers such as Jira accountId, private workflow mappings, and sensitive team config are never exposed to end users during execution.

## Docs index

- onboarding: `docs/zh-TW/ONBOARDING.md`
- quickstart: `docs/zh-TW/QUICKSTART.md`
- config setup: `docs/zh-TW/CONFIG_SETUP.md`
- token setup: `docs/zh-TW/JIRA_TOKEN_SETUP.md`
- Jira integration: `docs/en/JIRA_INTEGRATION_GUIDE.md`
- troubleshooting: `docs/en/TROUBLESHOOTING.md`
- regression cases: `tests/intake-cases.md`
- contributing: `CONTRIBUTING.md`
- security: `SECURITY.md`


## License

MIT
