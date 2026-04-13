# Jira 連線設定流程

這份文件說明如何把 skill 從「收單 + 草稿模式」升級到「可直接建立 Jira 任務」模式。

**不設定也可以用。** 沒有 config 時，skill 仍然可以跑完 intake 分析並產出草稿，只是無法自動建立 Jira。

---

## 必填 vs 選填

### 必填（想要自動建立 Jira 時）

| 欄位 | 說明 |
|------|------|
| `baseUrl` | Jira 網址，例如 `https://your-domain.atlassian.net` |
| `projectKey` | Jira 專案代碼，例如 `APP` |
| `email` | 呼叫 API 的帳號 email |
| `apiTokenEnv` | 存放 API token 的環境變數名稱，預設 `JIRA_API_TOKEN` |

### 選填（填了才有完整功能）

| 欄位 | 說明 | 沒填時的行為 |
|------|------|-------------|
| `defaultBoardId` | 預設看板 ID | 技能會列出所有看板請你選 |
| `sprintField` | Sprint 自訂欄位 ID，通常是 `customfield_10020` | 建立的任務不會帶 sprint |
| `assigneeMap` | 平台 / 模組 → accountId 對應表 | 技能只給角色建議，不自動帶負責人 |
| `statusTransitionMap` | 邏輯鍵 → 狀態轉換 ID 對應表 | 無法自動轉換狀態 |
| `defaultIssueType` | 預設建立類型，例如 `Task` / `Bug` | 預設用 `Task` |
| `defaultLabels` | 每張單自動加的標籤 | 不加標籤 |
| `defaultProjectKey` | 預設 Jira 專案代碼 | 每次建單時詢問 |
| `defaultSprintStrategy` | `ask`（詢問）或 `latest-active`（自動選最近衝刺） | `ask` |
| `defaultAssigneeId` | 預設負責人的 accountId | 每次建單時詢問 |

---

## 建立私有 config 的步驟

### 步驟 1：複製範本

```bash
cp config/team-config.example.json config/team-config.private.json
```

### 步驟 2：填入必填欄位

打開 `config/team-config.private.json`，至少填完：
- `baseUrl`
- `projectKey`
- `email`

### 步驟 3：設定 API token

建議直接放在 `config/.env`，不要寫進全域 shell 啟動檔。

```bash
cat > config/.env <<'EOF'
JIRA_API_TOKEN=your-token-here
EOF
```

申請 token 看 [`JIRA_TOKEN_SETUP.md`](./JIRA_TOKEN_SETUP.md)

### 步驟 4：驗證連線

```bash
python3 scripts/jira_lookup_metadata.py config/team-config.private.json projects
```

回傳 project 清單代表連線成功。

---

## 建立 assigneeMap

assigneeMap 需要每個人的 Jira accountId（不是 email，不是帳號名稱）。

### 查詢指令

```bash
# 列出 project 成員（回傳 accountId）
python3 scripts/jira_lookup_metadata.py config/team-config.private.json members
```

### 填入 config

```json
"assigneeMap": {
  "iOS": "712020:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "Android": "712020:yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy",
  "Web": "712020:zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz",
  "Backend": "...",
  "Design": "...",
  "PM": "..."
}
```

Key 要與 `references/assignee-rules.md` 裡的規則對得上。

---

## 驗證 board 與 sprint

### 查詢 board ID

```bash
python3 scripts/jira_lookup_metadata.py config/team-config.private.json boards
```

把回傳的 boardId 填入 `defaultBoardId`。

### 查詢 sprint

```bash
python3 scripts/jira_lookup_metadata.py config/team-config.private.json sprints <boardId>
```

確認 sprint 欄位是 `customfield_10020`（大多數 Jira 都是，但可用以下確認）：

```bash
python3 scripts/jira_lookup_metadata.py config/team-config.private.json fields
```

---

## 設定沒完整填寫時 skill 的降級行為

| 缺少的欄位 | skill 的行為 |
|------------|-------------|
| 沒有設定檔 | 跑完收單，輸出手動建單用的草稿，不嘗試建立 Jira |
| 有 config 但缺 `baseUrl` / `projectKey` | 無法建立 Jira，輸出草稿並提示缺少設定 |
| `assigneeMap` 為空 | 給出角色建議（例如「建議指派 iOS 工程師」），不帶 accountId |
| `defaultBoardId` 未設定 | 列出可用看板，請使用者選擇後繼續 |
| `sprintField` 未設定 | 建立任務時不帶 sprint，之後可手動加 |
| `statusTransitionMap` 未設定 | 建立任務後不自動轉換狀態，只建單 |

**原則**：缺設定時往「輸出草稿 + 提示缺啥」方向降級，不直接報錯中斷。

---

## 不要 commit 進 git 的內容

- `team-config.private.json`（已在 `.gitignore`）
- `config/.env`
- 真實 accountId
- 真實 API token
- 真實 transition ID（若不想公開）
