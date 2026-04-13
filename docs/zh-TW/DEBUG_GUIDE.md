# 防呆與偵錯指南

這份文件給非工程師和維護者用。
當 skill 判斷怪怪的、建 Jira 失敗、欄位對不上時，先看這份。

目前這份 repo 以 macOS + 本機 terminal 為主要支援目標。
如果你走的是 scripts 路徑，請先確認本機有 `python3`；這個 repo 不會自動幫你安裝 Python。

## 一、最常見的問題

### 1. skill 一直說不能發派
常見原因：
- 原始反饋太模糊
- 只有影片沒有文字
- 沒寫預期行為
- 不清楚是 bug 還是需求

先檢查：
- 是否有頁面 / 模組名稱
- 是否有實際行為
- 是否有預期行為
- 是否有重現步驟

### 2. skill 把需求判成 bug，或反過來
常見原因：
- 原始標題寫法模糊
- 團隊規格沒有寫清楚
- 模型在資訊不足時過度推測

處理方式：
- 補一句：`這是規格修正，不是 bug`
- 補一句：`目前行為符合實作，但我們要改規格`
- 若仍模糊，升級到較強模型判讀

### 3. Jira 建單失敗
常見原因：
- 本機沒有 `python3`
- token 沒設
- project key 錯
- issue type 不存在
- custom field id 不對
- 權限不足

先檢查：
- `python3` 是否可用：`python3 --version`
- `config/team-config.private.json` 是否正確
- `config/.env` 是否存在，且裡面有 `JIRA_API_TOKEN`
- Jira 專案是否允許這個帳號建單

如果你是第一次設定，最穩的方式是直接執行：

```bash
bash scripts/setup_jira_token.sh
```

這個腳本會：
- 檢查 `python3` 是否存在
- 建立 `config/team-config.private.json`
- 寫入 `config/.env`
- 驗證 Jira 連線

### 4. Jira 可以建單，但不能移欄
常見原因：
- transition id 錯
- 目標 workflow 不同
- 該 issue type 沒有那條 transition

處理方式：
- 先跑 metadata lookup 查 transitions
- 不要假設所有 project 的 transition id 一樣

可直接檢查：

```bash
python3 scripts/jira_lookup_metadata.py config/team-config.private.json transitions APP-123
```

### 5. skill 判定 blocked，但沒有回寫補件 comment
常見原因：
- 沒有執行 comment script
- 原始來源不是 Jira issue
- comment 檔案格式不對

處理方式：
- 先產出標準化補件 comment
- 再跑 `comment_jira_issue.py`
- 若 comment 是純文字，腳本會自動包成 ADF

如果你沒有 Jira MCP，也還沒完成 scripts 設定，這是正常現象。
此時 repo 會退回草稿模式，不會自動寫回 Jira。

## 二、建議防呆規則

- 沒有 `expected behavior` 就不要標 ready
- 沒有頁面或模組名稱就不要標 ready
- title/body 衝突時一律 blocked
- 只有影片時預設 blocked，除非異常非常明確
- `needs-product-decision` 不要硬標成 ready
- 小模型低信心時，一律升級到高階模型
- assignee 無明確 mapping 時，只回 owner type

## 三、排錯順序

1. 先確認輸入是不是夠清楚
2. 再確認你走的是哪條路徑：草稿模式、Jira MCP、或 scripts
3. 如果是 scripts，先確認 `python3`、`config/team-config.private.json`、`config/.env`
4. 再確認 skill 判斷規則是不是合理
5. 再確認 payload 是否完整
6. 最後才查 Jira API / token / 權限

## 四、遇到問題時建議回覆給使用者的話

### 補件型
- 目前資訊不足，還不能直接發派
- 還缺頁面、預期行為、重現步驟

### Jira 失敗型
- 任務內容已整理完成，但 Jira 建單失敗
- 先檢查 `python3`、token、project key、issue type、欄位設定

### 回寫補件型
- 目前這筆任務仍不能直接發派
- 我已整理缺少資訊與追問，建議先回寫到原 Jira comment 等待補件

### 判讀不穩型
- 這筆反饋存在規格歧義，建議改用較強模型再判一次
