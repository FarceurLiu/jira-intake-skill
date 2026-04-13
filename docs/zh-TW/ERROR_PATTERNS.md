# 常見錯誤模式

## 反饋輸入錯誤
- 只丟一句感覺怪怪的
- 標題像 bug，實際是需求
- 標題像需求，實際是要移除東西
- 一張單塞了兩到三個問題
- 沒有說哪個頁面
- 同一問題拆成 iOS / Android 多張，但沒先判斷是不是同一規格或同一 root cause
- 明明像既有任務延伸，卻當成全新單建立
- UI 微調只寫怪怪的、太大、太花、比較好看，沒有寫清楚現況與目標

## 模型判斷錯誤
- 過度腦補產品意圖
- 把附件當成足夠證據
- 因為看懂部分內容，就誤判整張單可發派
- 對語意反轉不敏感
- 看見跨平台相似單就直接視為不同問題，沒有先判斷 shared spec / backend root cause
- 沒先提醒 possible duplicate / follow-up，就把近重複單當新 ticket 正常流轉

## Jira 對接錯誤
- 把不同專案的欄位 id 混用
- transition id 寫死
- issue type 名稱和實際 Jira 設定不一致
- assignee 寫名字，不寫 accountId

## 流程錯誤
- 草稿確認前就直接建 Jira
- 還沒 validate payload 就直接送 API
- team config 寫進公開 repo
