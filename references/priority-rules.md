# Priority Rules

Use priority to express business urgency plus user impact, not emotional wording.

## Suggested model

### P0
- Core flow blocked
- Data loss, critical save failure, login failure, app crash on major flow
- Large user impact or urgent release blocker

### P1
- Important flow degraded
- Major UX breakage, but workaround exists
- High visibility issue in active testing or imminent release

### P2
- Noticeable problem with moderate impact
- Non-core flow issue
- Improvement needed before wider rollout, but not an immediate blocker

### P3
- Cosmetic issue
- Nice-to-have adjustment
- Low-frequency or low-impact cleanup

## Priority check dimensions

1. How many users or testers are affected
2. Whether the core flow is blocked
3. Whether a workaround exists
4. Whether the issue affects release confidence
5. Whether the issue is bug, spec gap, or polish

## Output guidance

Always include a one-line reason for the suggested priority.
