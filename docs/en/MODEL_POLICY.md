# Model Policy

## Goal

Choose model strength based on ambiguity and risk.

## Recommended policy

### Tier A: stronger model
Use for:
- ambiguous reports
- contradictory title/body
- bug vs request ambiguity
- attachment-heavy reports
- final ready-to-dispatch judgment

### Tier B: faster/cheaper model
Use for:
- bulk first-pass triage
- format cleanup
- simple missing-field detection
- low-risk backlog grooming

## Escalation rule

Escalate from Tier B to Tier A when:
- confidence is low
- issue type is unclear
- expected behavior cannot be inferred safely
- the skill would otherwise guess product intent

## Hard rule

Never let a weak model auto-mark a highly ambiguous item as ready without an escalation path.
