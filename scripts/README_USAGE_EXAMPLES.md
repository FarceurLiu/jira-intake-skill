# Script Usage Examples

## Validate payload

```bash
python3 scripts/validate_jira_payload.py payload.json
python3 scripts/validate_jira_payload.py payload.json --config config/team-config.private.json --field-mapping config/field-mapping.example.json
```

## Create issue

```bash
export JIRA_API_TOKEN=your_token
python3 scripts/create_jira_issue.py config/team-config.private.json payload.json
```

## Update issue

```bash
export JIRA_API_TOKEN=your_token
python3 scripts/update_jira_issue.py config/team-config.private.json APP-123 payload.json
```

## Move issue to another status

```bash
export JIRA_API_TOKEN=your_token
python3 scripts/transition_jira_issue.py config/team-config.private.json APP-123 31
python3 scripts/transition_jira_issue.py config/team-config.private.json APP-123 to_in_review
python3 scripts/transition_jira_issue.py config/team-config.private.json APP-123 "Done"
```

## Comment back to original issue

```bash
export JIRA_API_TOKEN=your_token
python3 scripts/comment_jira_issue.py config/team-config.private.json APP-123 --comment-file /path/to/comment.md
python3 scripts/comment_jira_issue.py config/team-config.private.json APP-123 --comment-file /path/to/comment.adf.json --format adf
```

## Lookup metadata

```bash
export JIRA_API_TOKEN=your_token

# existing modes
python3 scripts/jira_lookup_metadata.py config/team-config.private.json fields
python3 scripts/jira_lookup_metadata.py config/team-config.private.json issue-types
python3 scripts/jira_lookup_metadata.py config/team-config.private.json transitions APP-123

# list all accessible projects (for first-time setup)
python3 scripts/jira_lookup_metadata.py config/team-config.private.json projects

# list boards for the projectKey set in config
python3 scripts/jira_lookup_metadata.py config/team-config.private.json boards

# list active + future sprints — boardId via argument or defaultBoardId in config
python3 scripts/jira_lookup_metadata.py config/team-config.private.json sprints 42
python3 scripts/jira_lookup_metadata.py config/team-config.private.json sprints   # uses defaultBoardId

# list assignable members + accountId for the projectKey in config
python3 scripts/jira_lookup_metadata.py config/team-config.private.json members

# paginated modes auto-fetch all pages; override page size if needed
python3 scripts/jira_lookup_metadata.py config/team-config.private.json members --page-size 100
python3 scripts/jira_lookup_metadata.py config/team-config.private.json projects --page-size 25
```

Paginated modes (`projects`, `boards`, `sprints`, `members`) always return **all items** across
all pages. The output includes a `total` field showing how many items were collected:

```json
{"ok": true, "mode": "members", "total": 87, "data": [...]}
```

Non-paginated modes (`fields`, `transitions`, `issue-types`) make a single request and return
the raw Jira response unchanged.

### Typical first-time setup flow

```bash
# 1. find your project key
python3 scripts/jira_lookup_metadata.py config/team-config.private.json projects

# 2. set projectKey in config, then find the board
python3 scripts/jira_lookup_metadata.py config/team-config.private.json boards

# 3. set defaultBoardId in config, then verify sprint field id
python3 scripts/jira_lookup_metadata.py config/team-config.private.json fields | grep -i sprint

# 4. list sprints to confirm defaultBoardId works
python3 scripts/jira_lookup_metadata.py config/team-config.private.json sprints

# 5. list members to fill in assigneeMap
python3 scripts/jira_lookup_metadata.py config/team-config.private.json members
```
