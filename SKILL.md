---
name: jira-intake
description: Use when someone submits product feedback, a bug report, a QA finding, a UI issue, or any raw description that needs to become a Jira ticket. Triggers on phrases like "幫我整理這個反饋", "這個 bug 怎麼寫", "幫我建一張票", "整理成 Jira", "這個問題怎麼派", "可以幫我開單嗎", "help me create a ticket", "turn this into a Jira issue".
---

# Jira Intake

將雜亂的產品反饋整理為可派工的 Jira 任務。

## 目前階段

**Phase 1 — intake + draft（預設開放）**

| 功能 | 狀態 |
|------|------|
| 立即產出草稿；視情況在草稿中標注待確認事項 | 開放，無需設定 |
| 區分 bug / 需求 / 規格修正 / UX 調整 | 開放，無需設定 |
| 產出 Jira 草稿（標題、描述、優先序、完成條件） | 開放，無需設定 |
| 產出可回寫的補件 comment | 開放，無需設定 |
| 直接建立 Jira 任務 | 需要 Jira MCP 或 scripts + team config |
| 指派 assignee | 建單時即時查詢成員清單，讓用戶選擇 |
| Transition 狀態 | 需要填 statusTransitionMap |

沒有設定 config 時，照樣執行 intake 並輸出草稿，不會 crash，也不會跳過 intake。

## 核心原則

- 預設先產出草稿。
- 在使用者確認草稿，且存在可寫入路徑前，不寫入 Jira。
- 只有在真的卡住、無法產出有用草稿時，才追問。
- 若需要追問，只問一個最關鍵的問題。
- 傳輸路徑與 intake 判斷分離，不因寫入能力不同而跳過判斷。

## 工作流程

1. 先偵測最高可用執行路徑：
   - MCP 路徑：Jira MCP 可查詢專案
   - Scripts 路徑：`config/team-config.private.json` 與 `config/.env` 存在，此時讀 `docs/en/JIRA_INTEGRATION_GUIDE.md`
   - 手動路徑：前兩者皆不可用，輸出可直接貼入 Jira 的完整票文字
   - 任一路徑失敗時，自動回退到下一條
   - 除非用戶明確在排查設定，否則不要暴露底層傳輸錯誤

2. 讀取原始反饋、標題、描述、附件與上下文：
   - 若有多個明顯獨立項目，進入批次模式並編號 `#1`、`#2`、`#3`
   - 從上下文識別回報者角色，並在整個 session 內沿用
   - 若發現敏感資料，先警告並詢問要去識別後繼續，還是直接建單

3. 做 intake 判斷並決定是否直接草稿：
   - 一律先讀 `references/dispatch-checklist.md`
   - 一律讀 `references/priority-rules.md`、`references/assignee-rules.md`、`references/jira-template.md`
   - 當需要判斷證據、spec、主觀偏好、Figma 有效性、版本相容時，讀 `references/evidence-and-spec-rules.md`
   - 當需要判斷 UI 細修、元件類型、動畫、跨平台鏡像、duplicate 時，讀 `references/ui-and-animation-rules.md`
   - 當需要判斷 ownership、敏感資料、破壞性操作、依賴關係時，讀 `references/risk-and-dependency-rules.md`
   - 當原始回報太模糊、需要示例輔助標準化時，讀 `references/examples.md`
   - 除非真的無法辨識問題，否則先出草稿，不要過早停住

4. 產出草稿：
   - 預設使用條列格式
   - 若有截圖或影片，在描述中標示「附截圖」或「附影片」
   - 若產品意圖未定，草稿內標注待確認事項，不中止流程
   - 若無 App 版本、build number、環境資訊，不主動追問

5. 顯示草稿並請使用者確認：
   - MCP 可用：`這樣理解對嗎？確認後我直接建單。`
   - Scripts 可用：`這樣理解對嗎？確認後用 scripts 建單。`
   - 僅手動路徑可用：
     > 這個 skill 支援直接寫入 Jira，但目前這個環境尚未完成可寫入路徑的設定，所以我會先輸出完整的手動格式讓你貼入。如果你有 Atlassian 帳號且可建立個人 API token，之後也可以做一次性設定直接建單，需要的話告訴我。
   - 批次模式沿用相同欄位結構，並要求用戶一次確認或指出要修改的編號

6. 用戶確認後再派工：
   - 批次模式預設一次詢問 board、sprint、assignee，並套用到所有票
   - 若用戶已提供 session 層級預設值，靜默套用
   - 若 config 已設定預設 project、sprint 策略或 assignee，靜默套用
   - 否則才查詢並詢問專案、board、sprint、assignee

7. 依路徑執行：
   - MCP 路徑：解析專案、sprint、assignee 後建立，若支援則附加附件
   - Scripts 路徑：使用 `scripts/create_jira_issue.py`，只在排查失敗時才用 `scripts/validate_jira_payload.py`
   - 手動路徑：輸出完整票文字，讓用戶貼入 Jira

## 寫入路徑與設定觸發

- 若用戶只是要草稿，不主動推設定。
- 若用戶明確要建立或寫入 Jira，且 MCP 不可用、scripts 設定也缺失，應明確說明是「此環境尚未完成 Jira 連線設定」，不是 skill 沒有這個能力，然後再問：
  > 你可以在 Atlassian 帳號設定（id.atlassian.com）裡建立個人 API token 嗎？這跟管理員權限無關，一般帳號通常都可以建。（若公司有限制則無法）
- 若可以，再引導執行 `scripts/setup_jira_token.sh`。
- 若不確定、公司限制、或不想設定，直接走手動路徑，不再追問。
- 若 token 設定完成但建單失敗，優先視為專案權限問題，而不是 token 錯誤。
- 手動路徑是正常主路徑之一，不用施壓式語氣推設定。

## 輸出規範

預設輸出永遠是草稿，口吻簡短，像在跟隊友說話。

**格式強制規定**：票的欄位一律以條列格式輸出，每個欄位獨立一行，格式為 `欄位名稱：內容`。不得改用段落或自由格式描述票內容。

### 預設草稿格式

**[標題]**

- 問題描述：[現象 + 截圖/影片說明]
- 優先序：[緊急 / 高 / 中 / 低]
- 負責人：[role 或人名]
- 標籤：[...]
- 完成條件：[只在修法不明顯時才寫，簡單 UI bug 可省略]

這樣理解對嗎？確認後我可以直接建單。

### 當資訊真的不足時

只問一件真正卡住的事，不列清單。

> 目前理解：[一句話]
>
> 有一件事需要確認：[一個具體問題]

若 UI 元素定位不明，可附最小引導：

> 可以這樣描述：
> - 頁面：設定頁 / 詳細頁 / 彈窗 / ...
> - 元件：右上角關閉鈕 / 搜尋列清除鈕 / ...
> - 現在看起來怎麼了：位置跑掉 / 顏色不對 / 大小怪 / ...
>
> （不需要全填，有方向就好）

## 按需讀取

### 收單與分析（所有用戶）
- `references/dispatch-checklist.md`：決定是否該停下來追問
- `references/priority-rules.md`：判斷優先序
- `references/assignee-rules.md`：判斷負責人類型
- `references/jira-template.md`：標準票格式
- `references/evidence-and-spec-rules.md`：證據充分性、spec、主觀偏好、版本相容
- `references/ui-and-animation-rules.md`：UI 細修、元件類型、動畫、duplicate、跨平台判斷
- `references/risk-and-dependency-rules.md`：ownership、敏感資料、破壞性流程、依賴關係
- `references/examples.md`：模糊輸入的標準化示例
- `templates/JIRA_INTAKE_COMMENT_TEMPLATE.md`：blocked 或 needs-product-decision 回寫 comment

### 無設定的非工程用戶
- `docs/zh-TW/GUIDE_MANUAL.md`：零設定使用指南
- `docs/zh-TW/ONBOARDING.md`：不確定怎麼開始時再讀

### Jira 執行（MCP 或 scripts）
- `scripts/setup_jira_token.sh`：首次設定 token
- `docs/en/JIRA_INTEGRATION_GUIDE.md`：建立、更新、transition、metadata 查詢
- `scripts/comment_jira_issue.py`：回寫 blocked 或 needs-decision comment
- `scripts/preflight_checklist.txt`：Jira 執行前最後防線
- `config/team-config.private.sample.json`、`config/field-mapping.example.json`：設定起點

### 排查問題
- `docs/en/MODEL_POLICY.md`：模型強度選擇
- `docs/zh-TW/MODEL_SUPPORT.md`、`docs/zh-TW/USE_CASES.md`：非工程用戶的邊界與適用情境
- `docs/zh-TW/DEBUG_GUIDE.md`、`docs/en/TROUBLESHOOTING.md`、`docs/zh-TW/ERROR_PATTERNS.md`：輸出不穩或 Jira 執行失敗時才讀

## 邊界

- 完全無法識別問題時，不產出草稿。
- 預期行為純屬推測時，在草稿中標不確定性，不要講成已確認。
- 未經用戶確認，不自動建立 Jira。
- 除非用戶要求，不把多個不同問題合併成一張票。
- 含敏感資料時，先去識別，再決定是否寫入或送模型。
- 不記錄含敏感資料的完整 payload 或完整 Jira 回應。
