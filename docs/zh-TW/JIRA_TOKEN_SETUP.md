# Jira API Token 設定指南

完全不懂技術也能照著做。  
整個流程大約 5 分鐘。

> **推薦：** 直接告訴 Claude 或 Codex「幫我設定 Jira 連線」，skill 會自動執行設定腳本，在本機終端機依序引導你輸入 Jira 網址、專案代碼、Email 與 API Token（token 不顯示，全程不經過 agent），設定完即可使用。  
> 以下手動步驟為備用方案。

> **補充：** scripts 路徑需要本機已有 `python3`。如果系統沒有 Python 3，設定腳本會直接停止並提示先安裝；這個 repo 不會自動幫你安裝 Python。

---

## 什麼是 API Token？

你可以把它想成一把**專屬鑰匙**，讓 agent 代替你操作 Jira。  
這把鑰匙只有你自己知道，絕對不要給別人，也不要放進任何公開的地方。

---

## 第一步：產生你的 Jira API Token

1. 打開瀏覽器，前往這個網址：  
   👉 **https://id.atlassian.com/manage-profile/security/api-tokens**

2. 如果還沒登入，先用你的 Atlassian 帳號（就是你登入 Jira 用的帳號）登入。

3. 頁面上會看到「**API tokens**」區塊，點擊「**Create API token**」按鈕。

4. 在彈出的視窗中，幫這個 token 取一個名字，方便你記住用途。  
   建議填：`jira-intake-skill`

5. 點「**Create**」。

6. 畫面上會出現一串英文和數字組成的長字串，這就是你的 **API Token**。  
   ⚠️ **這串字只會出現一次，現在必須複製起來！**  
   點「Copy」按鈕，或用滑鼠全選後按 Ctrl+C（Windows）/ Cmd+C（Mac）複製。

7. 點「Close」關閉視窗。

---

## 第二步：把 Token 儲存到設定檔案

找到你的 `config` 資料夾（和 `team-config.private.json` 放在一起的地方）。

在這個資料夾裡建立一個新的文字檔，檔名叫做 `.env`。
這份檔案只放在 repo 的 `config/` 目錄內，不要寫進 `~/.zshrc`、`~/.bash_profile` 之類的全域 shell 設定。

> **注意：** 檔名前面有一個小點，這是正確的，不是打錯。

### Mac 怎麼建立 `.env` 檔案

**方法 A（推薦）：用終端機建立**

1. 打開「終端機」（在 Finder → 應用程式 → 工具程式裡面）
2. 輸入以下指令，把 `你的config資料夾路徑` 換成你的實際路徑：
   ```
   touch /你的config資料夾路徑/.env
   open -e /你的config資料夾路徑/.env
   ```
3. 文字編輯器會自動打開這個空白檔案

**方法 B：用文字編輯器 + Finder**

1. 打開「文字編輯器」（TextEdit）
2. 選單 → 格式 → 製作純文字格式（很重要，不能是 RTF）
3. 先把內容填好（見下方），存檔時取名 `.env`，存到 `config` 資料夾
4. 如果 Finder 不讓你用點開頭的檔名，先存成 `env.txt`，再用終端機改名：
   ```
   mv /你的路徑/env.txt /你的路徑/.env
   ```

### Windows 怎麼建立 `.env` 檔案

1. 打開記事本（Notepad）
2. 先把內容填好（見下方）
3. 「另存新檔」→ 檔案類型選「**所有檔案 (*.*)**」→ 檔名輸入 `.env` → 存到 `config` 資料夾

---

## 第三步：填入 Token

用任何文字編輯器打開剛才建立的 `.env` 檔案，填入以下內容：

```
JIRA_API_TOKEN=<貼上你剛才複製的-token>
```

例如（這是佔位符，你的會不一樣）：

```
JIRA_API_TOKEN=<your-api-token>
```

存檔。完成。

---

## 第四步：確認設定是否正確

如果你用的是可開 terminal 的 Claude Code 或 Codex，可以執行以下指令確認連線正常：

```bash
python3 scripts/jira_lookup_metadata.py config/team-config.private.json projects
```

如果看到一串 JSON 資料（不是錯誤訊息），代表設定成功。

---

## 常見問題

**Q：我存了 .env 但 agent 說還是找不到 token？**  
A：確認 `.env` 檔案是否在和 `team-config.private.json` **同一個資料夾**裡。  
檔案名稱必須是 `.env`（有小點，沒有其他副檔名）。

**Q：我的 .env 檔案不見了？**  
A：以點開頭的檔案在 Mac 和 Linux 預設是隱藏的。  
Mac 可以按 **Cmd + Shift + .** 讓 Finder 顯示隱藏檔案。

**Q：Token 要多久換一次？**  
A：Atlassian 的 API Token 目前不會自動過期，但建議每 6-12 個月換一次。  
換 token 時只要回到步驟一重新產生，再更新 `.env` 裡的值就好。

**Q：token 不小心給別人看到了怎麼辦？**  
A：立刻回到 https://id.atlassian.com/manage-profile/security/api-tokens  
找到那個 token，點「Revoke」撤銷它，然後重新產生一個新的。

**Q：我不是用 scripts，我是用 Jira MCP 的話要設定嗎？**  
A：不需要。Jira MCP 有自己的登入機制，不用設定 API Token。  
這份指南只適用於透過 scripts 執行的情況。

---

## 小結

```
你的 config/ 資料夾長這樣：

config/
├── team-config.private.json   ← 你的 Jira 網址和設定
├── field-mapping.private.json ← （選填）欄位對應
└── .env                       ← 你的 API Token（這份不會被 commit）
```

`config/.env` 和 `team-config.private.json` 都不會被上傳到 Git，放心使用。
