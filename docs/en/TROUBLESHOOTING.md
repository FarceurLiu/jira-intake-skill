# Troubleshooting

## Symptom: item is always blocked
Check:
- page/module missing
- actual behavior missing
- expected behavior missing
- repro steps missing
- attachment unclear

## Symptom: issue type classification is unstable
Check:
- conflicting title/body
- spec not finalized
- weak model used on ambiguous input
- no examples loaded

Action:
- add one explicit sentence clarifying intent
- escalate model tier
- ask targeted follow-up questions

## Symptom: Jira create failed
Check:
- token present in runtime env
- baseUrl correct
- projectKey correct
- issue type valid in target project
- required custom fields missing
- account has permission

## Symptom: Jira transition failed
Check:
- transition id valid for this issue
- issue type workflow differs
- status name is same but id differs across projects

## Safe debug order
1. input quality
2. skill decision
3. payload validation
4. Jira metadata
5. auth and permissions
