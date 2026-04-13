# Risk and Dependency Rules

Use this file for ownership, sensitive data, destructive actions, and completion dependency judgment.

## Ownership rules

- Assign by ownership rule, not personal guess.
- If ownership is unclear, mark as pending assignment.

## Completion/dependency rules

- If the issue involves destructive flows such as cancel action, clear draft content, or force logout, suggest a confirmation dialog in acceptance criteria, but do not force it.
- If acceptance depends on another role's deliverable, write the dependency explicitly.
- If completion requires two roles in sequence, write both steps clearly.
- If completion depends on the reporter producing assets or specs, flag that dependency in the draft.

## Sensitive data boundary

- If the report contains personal data, transaction identifiers, financial information, or screenshots containing them, warn first and ask whether to de-identify before proceeding.
- Pass only the minimum context needed for intake judgment.
- Do not log or forward full sensitive payloads or full Jira responses containing sensitive data.
