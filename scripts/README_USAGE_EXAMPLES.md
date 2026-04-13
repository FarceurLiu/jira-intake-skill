# 腳本使用範例

## 驗證 payload

```bash
python3 scripts/validate_jira_payload.py payload.json
python3 scripts/validate_jira_payload.py payload.json --config config/team-config.private.json --field-mapping config/field-mapping.example.json
```

## 建立議題

```bash
export JIRA_API_TOKEN=your_token
python3 scripts/create_jira_issue.py config/team-config.private.json payload.json
```

## 更新議題

```bash
export JIRA_API_TOKEN=your_token
python3 scripts/update_jira_issue.py config/team-config.private.json APP-123 payload.json
```

## 移動議題狀態

```bash
export JIRA_API_TOKEN=your_token
python3 scripts/transition_jira_issue.py config/team-config.private.json APP-123 31
python3 scripts/transition_jira_issue.py config/team-config.private.json APP-123 to_in_review
python3 scripts/transition_jira_issue.py config/team-config.private.json APP-123 "Done"
```

## 回寫留言

```bash
export JIRA_API_TOKEN=your_token
python3 scripts/comment_jira_issue.py config/team-config.private.json APP-123 --comment-file /path/to/comment.md
python3 scripts/comment_jira_issue.py config/team-config.private.json APP-123 --comment-file /path/to/comment.adf.json --format adf
```

## 查詢欄位資料

```bash
export JIRA_API_TOKEN=your_token

# 現有模式
python3 scripts/jira_lookup_metadata.py config/team-config.private.json fields
python3 scripts/jira_lookup_metadata.py config/team-config.private.json issue-types
python3 scripts/jira_lookup_metadata.py config/team-config.private.json transitions APP-123

# 列出可存取專案，用於首次設定
python3 scripts/jira_lookup_metadata.py config/team-config.private.json projects

# 列出 config 內 projectKey 對應的看板
python3 scripts/jira_lookup_metadata.py config/team-config.private.json boards

# 列出進行中與未來衝刺，可用參數指定 boardId，或使用 config 內 defaultBoardId
python3 scripts/jira_lookup_metadata.py config/team-config.private.json sprints 42
python3 scripts/jira_lookup_metadata.py config/team-config.private.json sprints

# 列出可指派成員與 accountId
python3 scripts/jira_lookup_metadata.py config/team-config.private.json members

# 分頁模式會自動抓取全部頁面；必要時可覆寫單頁數量
python3 scripts/jira_lookup_metadata.py config/team-config.private.json members --page-size 100
python3 scripts/jira_lookup_metadata.py config/team-config.private.json projects --page-size 25
```

分頁模式（`projects`、`boards`、`sprints`、`members`）會回傳所有頁面的項目。
輸出會包含 `total` 欄位，表示實際收集到的項目數：

```json
{"ok": true, "mode": "members", "total": 87, "data": [...]}
```

非分頁模式（`fields`、`transitions`、`issue-types`）只發出一次請求。

## 寫入腳本輸出

建立、更新、留言與移動狀態腳本預設只輸出安全摘要，例如議題 key、議題網址、留言 id 或 HTTP 狀態。
除非正在排查問題，否則不要加 `--verbose`；該參數會輸出完整 Jira 回應。

## 首次設定流程

```bash
# 1. 找到專案 key
python3 scripts/jira_lookup_metadata.py config/team-config.private.json projects

# 2. 在 config 填入 projectKey，然後查詢看板
python3 scripts/jira_lookup_metadata.py config/team-config.private.json boards

# 3. 在 config 填入 defaultBoardId，然後確認 sprint 欄位 id
python3 scripts/jira_lookup_metadata.py config/team-config.private.json fields | grep -i sprint

# 4. 列出衝刺，確認 defaultBoardId 可用
python3 scripts/jira_lookup_metadata.py config/team-config.private.json sprints

# 5. 列出成員，用於填寫 assigneeMap
python3 scripts/jira_lookup_metadata.py config/team-config.private.json members
```
