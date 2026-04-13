# Contributing

Thanks for contributing.

## Before You Open a PR

- Read [README.md](./README.md) for product scope and support boundaries.
- This repo is currently macOS-first.
- Keep examples synthetic. Do not commit real tokens, real Jira account IDs, or private team config.
- If you change setup or user-facing behavior, update the matching docs in the same PR.

## Good Contribution Areas

- documentation clarity
- intake-rule refinements
- regression case additions in `tests/intake-cases.md`
- safer setup flows
- script robustness
- macOS-first usability improvements
- small CI or validation improvements

## PR Expectations

- Keep changes scoped.
- Explain the user-visible effect.
- Mention any docs updated.
- If you change intake behavior, update the matching `references/` files and relevant regression cases in `tests/intake-cases.md`.
- Do not broaden platform support claims unless you also verify and document them.

## Local Checks

Run these before submitting:

```bash
bash -n scripts/setup_jira_token.sh
python3 -m py_compile scripts/*.py
```

## Sensitive Data Rules

Never include:

- real Jira API tokens
- `config/team-config.private.json`
- real account IDs
- screenshots or payloads with user PII
