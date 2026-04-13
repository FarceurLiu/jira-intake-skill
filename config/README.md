# config 使用說明

## 檔案用途

### `team-config.example.json`
公開範本，可放進 git。使用者應複製成 `team-config.private.json` 後再填入真實值。

### `team-config.private.json`
實際執行用的私有設定檔，不要 commit。

### `field-mapping.example.json`
欄位與類型對應範本。

## 建議做法

1. 複製 `team-config.example.json`
2. 另存成 `team-config.private.json`
3. 填入真實 Jira 網址、bot email、project key
4. 在 `config/.env` 設定 `JIRA_API_TOKEN`
5. 先跑欄位資料查詢
6. 再調整欄位對應
7. `statusTransitionMap` 可用邏輯鍵對應狀態轉換 id 或狀態名稱，例如 `to_in_review`

## 不要放進 git 的內容

- 真實 Jira 網址（若屬敏感）
- 真實 bot email
- 真實 token
- 真實 accountId
- 真實狀態轉換 id 對照（若不想公開）

## 目前腳本會直接使用的欄位

- `baseUrl`
- `projectKey`
- `email`
- `apiTokenEnv`
- `statusTransitionMap`

其他欄位可以先保留在設定檔中，之後擴充使用。
