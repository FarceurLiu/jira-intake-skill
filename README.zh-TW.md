# jira-intake-skill

把模糊的產品反饋整理成可發派的 Jira 草稿——在任何 Jira 寫入操作之前，先完成 intake 判斷。

[English](./README.md)

> 目前支援目標：macOS + 本機 terminal 環境。
> 安裝 skill 後即可使用草稿模式；若要直接操作 Jira，仍需 `python3` 與私有 Jira 設定。
> 本專案與 Atlassian、Anthropic、OpenAI 無隸屬或背書關係。
> 最適合已習慣 agent workflow，且可接受偶爾使用本機 terminal 的使用者。

---

## 這個 skill 的核心價值不是開單，而是 intake 治理

它做的事：
- 判斷反饋是否有足夠資訊可以發派
- 分清楚「缺資料」和「還沒有產品決策」是兩件不同的事
- 先出草稿讓你確認，才進行任何 Jira 寫入
- 沒有可寫入的 Jira 路徑時，自動降級為手動可貼的草稿格式

直接建 Jira 單是選填功能，且只在用戶明確確認後才執行。

---

## 開源邊界

這個 repo 若要公開，應只保留：
- 通用 intake 規則
- 通用範例
- 可公開的 config sample
- 可重用的 scripts

不應放進公開 repo 的內容：
- 私有 Jira 設定
- 真實 accountId mapping
- 能識別特定組織結構的 workflow 規則
- 真實客戶回報、截圖、交易資訊、事故內容
- 從正式環境直接複製且未去識別的案例

這個 repo 應保持通用，不要把組織專屬 mapping 或真實案例放進公開樹。

---

團隊在收到 bug 回報、QA 測試反饋、UX 問題或功能需求時，常常面臨這些困境：

- 描述太模糊，不知道哪裡出問題
- 標題和內容講的不是同一件事
- 只有截圖或影片，沒有文字說明
- 不確定這是 bug、需求，還是規格要改
- 想直接貼進 Jira，但格式都要重新整理

這個 skill 幫你把這些原始反饋直接轉成草稿，讓你確認後再建單。

---

## 一眼看懂

| 功能 | 安裝後可直接使用 | 額外需求 |
|------|------------------|----------|
| 把原始反饋整理成 Jira 草稿 | 可以 | 無 |
| 判斷 blocked / ready / needs-product-decision | 可以 | 無 |
| 產出補件 comment 或追問方向 | 可以 | 無 |
| 直接建立 / 更新 / transition Jira 任務 | 不行 | Jira MCP 或 scripts + 私有設定 |

## 基本需求

- 零設定草稿模式：Claude Code 或 Codex 這類支援 skill 的 agent 環境
- scripts 路徑：`python3`（這個 repo 不會自動安裝）、Jira API token、私有 config
- Jira MCP 路徑：可連 Jira 的執行環境

---

## 適合誰用

- QA、PM、設計師、一般產品與協作角色
- 任何需要整理 Jira 任務的人
- 不需要懂 Jira API，也不需要任何技術背景

---

## 能做什麼

### 零設定模式（直接可用）

不需要任何帳號或設定：

- 把反饋整理成 Jira 草稿（標題、問題描述、優先序、負責人、標籤）
- 區分 bug / 新需求 / 規格修正 / UI 調整
- 偵測資訊是否足夠，不夠就追問最關鍵的那一件事
- 批量模式：一次整理多筆反饋

### 連線模式（需設定）

設定好 Jira MCP 或 scripts 後可以直接建單：

- 建立 Jira 任務
- 選擇看板、sprint、指派負責人
- 回寫補件 comment 到原 Jira 單
- 自動 transition 任務狀態

---

## 安裝

把這個 repo clone 到 agent 的標準 skill 目錄。
如果要對外開源，建議直接寫標準路徑，不要寫成像 `~/skills` 這種自訂目錄，否則其他使用者很可能不會自動載入。

### Claude Code

```bash
git clone https://github.com/FarceurLiu/jira-intake-skill.git ~/.claude/skills/jira-intake
```

重新開一個 Claude Code session，skill 會自動載入。

### Codex

```bash
git clone https://github.com/FarceurLiu/jira-intake-skill.git "${CODEX_HOME:-$HOME/.codex}/skills/jira-intake"
```

重新開一個 Codex session，skill 會自動載入。

### 補充說明

- 資料夾名稱建議保留為 `jira-intake`，除非你刻意想改 skill 名稱。
- 安裝完即可使用「零設定模式」產出草稿，不需要先接 Jira。
- 若要直接建 Jira，仍需另外完成 Jira MCP 或 scripts 連線設定。

### 快速驗證

安裝後可直接測試：

```text
幫我把這個 bug 反饋整理成 Jira 草稿
```

如果想更明確觸發，也可以直接提到 skill 名稱：

```text
請用 jira-intake 幫我整理這段反饋
```

之後更新：

```bash
git -C ~/.claude/skills/jira-intake pull
git -C "${CODEX_HOME:-$HOME/.codex}/skills/jira-intake" pull
```

---

## 怎麼觸發

直接說中文就好，不需要特定格式：

```
幫我整理這個 bug 反饋
這個問題怎麼派工
幫我建一張 Jira 票
```

或者直接貼反饋：

```
我要反饋：iOS 設定頁的返回按鈕點了沒反應，試了三次都這樣
```

---

## 使用範例

**你說：**
> 我要反饋：iOS 設定頁的主圖示顯示靠左，應該要置中

**skill 回：**
> **[UX][iOS] 設定頁主圖示對齊異常，應置中顯示**
>
> 問題描述：iOS 設定頁主圖示目前靠左對齊，預期行為為置中顯示。
> 優先序：中
> 負責人：iOS 工程師
> 標籤：ios, ui, alignment
>
> 這樣理解對嗎？確認後我列出看板讓你選。

**你說：** 確認

**skill 接著問：** 選看板 → 選 sprint → 選負責人 → 建單完成，回傳 ticket 連結

---

## 設定 Jira 連線（選填）

想讓 skill 直接幫你建單，需要一次性設定。

**自動化設定（推薦）：**

告訴 Claude 或 Codex「幫我設定 Jira 連線」，skill 會在本機終端機引導你輸入：
- Jira 網址（例如 `https://your-company.atlassian.net`）
- 專案代碼（例如 `APP`）
- 登入 Email
- API Token（輸入時不顯示，不會經過 agent）

**手動設定：**

```bash
# 1. 複製設定範本
cp config/team-config.private.sample.json config/team-config.private.json

# 2. 填入 Jira 網址、專案代碼、Email
# 用任意編輯器開啟 config/team-config.private.json 修改

# 3. 建立 token 設定檔
cat > config/.env <<'EOF'
JIRA_API_TOKEN=你的-token-在這裡
EOF

# 4. 驗證連線
python3 scripts/jira_lookup_metadata.py config/team-config.private.json projects
```

詳細步驟見 [`docs/zh-TW/CONFIG_SETUP.md`](docs/zh-TW/CONFIG_SETUP.md)。

---

## 批量反饋

可以一次送多筆，skill 會分開整理：

```
反饋：
1. 詳細頁標題文字消失
2. 表單頁偶發閃退
3. 載入等待動畫速度過快
```

skill 會產出三份草稿，統一確認後一次選看板、sprint、負責人，批量建單。

---

## 安全說明

以下內容不會被 commit 進 repo：

- API token（存在 `config/.env`，已在 `.gitignore`）
- 私有設定（`config/team-config.private.json`，已在 `.gitignore`）
- 真實的 Jira accountId
- 真實客戶回報、交易編號、事故描述、正式環境截圖

若反饋內含用戶個資、交易編號或財務相關資訊，skill 會在建單前主動提醒去識別化。

---

## 設定降級行為

| 情況 | skill 的行為 |
|------|------------|
| 沒有任何設定 | 產出草稿，提示手動貼進 Jira |
| 有 config 但 Jira MCP 沒連 | 改用 scripts 建單 |
| scripts 也沒設定 | 輸出完整草稿，請使用者自行貼入 |

---

## 文件索引

| 文件 | 說明 |
|------|------|
| [`docs/zh-TW/ONBOARDING.md`](docs/zh-TW/ONBOARDING.md) | 新手看這裡，選適合你的路徑 |
| [`docs/zh-TW/QUICKSTART.md`](docs/zh-TW/QUICKSTART.md) | 快速上手 |
| [`docs/zh-TW/GUIDE_MANUAL.md`](docs/zh-TW/GUIDE_MANUAL.md) | 零設定手動建單流程 |
| [`docs/zh-TW/CONFIG_SETUP.md`](docs/zh-TW/CONFIG_SETUP.md) | Jira 連線設定 |
| [`docs/zh-TW/JIRA_TOKEN_SETUP.md`](docs/zh-TW/JIRA_TOKEN_SETUP.md) | 取得 API Token |
| [`docs/zh-TW/DEBUG_GUIDE.md`](docs/zh-TW/DEBUG_GUIDE.md) | 常見問題排查 |
| [`docs/en/JIRA_INTEGRATION_GUIDE.md`](docs/en/JIRA_INTEGRATION_GUIDE.md) | Jira API 整合說明（英文） |
| [`tests/intake-cases.md`](tests/intake-cases.md) | intake 判斷回歸測例 |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | 貢獻方式與基本檢查 |
| [`SECURITY.md`](SECURITY.md) | 安全回報與敏感資料處理 |

---

## 授權

Apache License 2.0
