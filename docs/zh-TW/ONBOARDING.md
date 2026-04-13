# 上手順序

## 開始前：先安裝 skill

如果你是第一次使用，先把 repo 放到 agent 的標準 skill 目錄：

### Claude Code

```bash
git clone https://github.com/FarceurLiu/jira-intake-skill.git ~/.claude/skills/jira-intake
```

### Codex

```bash
git clone https://github.com/FarceurLiu/jira-intake-skill.git "${CODEX_HOME:-$HOME/.codex}/skills/jira-intake"
```

安裝或更新後，請重新開一個新 session，讓 skill 重新載入。

## 你是哪種情境？先選路徑

```
你想用這個 skill 做什麼？
│
├── 只是想整理反饋、產出 Jira 草稿
│   不需要真的建立 Jira 任務
│   → 路徑 A：零設定，現在就可以用
│
├── 想讓 agent 直接幫我建 Jira 任務
│   │
│   ├── 我用的是有 Jira 整合的環境（Jira MCP 已連線）
│   │   → 路徑 B：零設定，直接說「幫我建到 Jira」
│   │
│   └── 我沒有 Jira MCP，需要用 API 接
│       → 路徑 C：需要一次性技術設定，看下方
│
└── 我要協助設定或調整這個工具
    → 路徑 D：維護者流程，看下方
```

---

## 路徑 A：零設定，整理反饋 + 手動建單

**不需要任何設定。** 把反饋丟給 Claude 或 Codex，拿到整理好的草稿，自己貼進 Jira。

→ 看 [`GUIDE_MANUAL.md`](./GUIDE_MANUAL.md)

---

## 路徑 B：Jira MCP 已連線

**不需要任何設定。** Claude 或 Codex 直接幫你建、更新、回寫 comment。

整理完後對 agent 說：
- 「幫我建到 Jira」
- 「建到 [專案名] 的這週 sprint」
- 「回寫 comment 到原本那張單」

---

## 路徑 C：用 API 接 Jira（首次設定）

需要一位工程師做一次性設定。設定完後，團隊其他人不需要再動。

前提是本機已有 `python3`。如果沒有，這個 repo 不會自動安裝，需先自行安裝或請工程師協助。

**自動化設定（推薦）：** 直接告訴 Claude 或 Codex「幫我設定 Jira 連線」，skill 會自動執行 `scripts/setup_jira_token.sh`：
- 在本機終端機依序輸入：Jira 網址、專案代碼、Email、API Token（token 輸入不顯示，全程不經過 agent）
- 開啟瀏覽器到 Atlassian token 頁面方便複製 token
- 自動寫入環境變數與 config
- 自動驗證連線

**手動設定：**
1. 申請 Jira API token → 看 [`JIRA_TOKEN_SETUP.md`](./JIRA_TOKEN_SETUP.md)
2. 建立私有 config → 複製 `config/team-config.private.sample.json`，填入真實值
3. 設定環境變數 `JIRA_API_TOKEN`
4. 測試連線 → `python3 scripts/jira_lookup_metadata.py config/team-config.private.json projects`
5. 填入 `assigneeMap`、`defaultBoardId`、`sprintField`

→ 完整說明看 [`docs/en/JIRA_INTEGRATION_GUIDE.md`](../en/JIRA_INTEGRATION_GUIDE.md)

---

## 路徑 D：維護者流程

1. 確認 `SKILL.md` 的核心 workflow 與讀取導航是否符合團隊需求
2. 確認 `references/` 內的判斷規則是否符合團隊需求
3. 視需要填入 `references/organization-rules-template.md`（priority 和 assignee 的自訂規則）
4. 確認 `config/team-config.private.json` 有正確的欄位 id
5. 規則調整後，再同步更新 `references/assignee-rules.md`

---

## 如果你是 Codex 使用者

Codex 和 Claude 一樣，可以直接使用 intake 分析功能（路徑 A）。  
把反饋文字貼給 Codex，請它用 `jira-intake` skill 整理即可。  
若要讓 Codex 直接建立 Jira，仍需要可寫入的執行路徑：  
- 你的 Codex 環境已連 Jira MCP  
- 或本機已完成 `scripts + team config + API token` 設定

也就是說，Codex 預設沒有 Jira 原生連線不代表不能建單；沒有 MCP 時，仍可走這個 repo 內建的 scripts 路徑。
