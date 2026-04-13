# Intake Regression Cases

Use these cases to verify that refactors do not weaken intake judgment.
All examples in this file must remain synthetic and must not be copied from real company or customer cases.

## How to use

For each case, verify:
- whether the skill drafts immediately or asks one blocking question
- whether the type/classification is reasonable
- whether the priority is in the right range
- whether the draft flags `blocked`, `needs-product-decision`, `needs-spec`, or duplicate risk correctly
- whether the reply stays concise and uses the required bullet-field draft format

---

## Case 1: Clear iOS UI bug

### Raw input
> iOS 設定頁的主圖示目前靠左，應該要置中，附截圖。

### Expected judgment
- Draft immediately
- Type: UI bug
- Priority: P2 or P3 depending on impact
- Note evidence as screenshot
- No extra follow-up question

---

## Case 2: Video only, affected element unclear

### Raw input
> 標題：onboarding 頁面怪怪的
> 描述：附影片

### Expected judgment
- Do not dispatch immediately
- Ask one blocking question
- Question should identify which section/component is wrong and what should happen instead

---

## Case 3: Subjective preference without approved spec

### Raw input
> 我覺得首頁 banner 再高一點會比較好看

### Expected judgment
- Classify as `needs-product-decision`
- Do not pretend it is dispatch-ready UX adjustment
- Ask for source of truth or flag decision dependency

---

## Case 4: Feature request without Figma or PRD

### Raw input
> 幫我加一個狀態 badge 在資訊區標題下面

### Expected judgment
- Ask whether there is Figma or product decision support
- If absent, mark as `needs-spec`
- Do not jump straight into implementation-ready ticket

---

## Case 5: Animation speed complaint without spec

### Raw input
> 轉場動畫太快了，感覺不順

### Expected judgment
- Treat as animation-specific intake
- Ask the most blocking animation question if current/expected behavior is unclear
- If reporter cannot define target spec, switch to engineer-proposes-initial-value path

---

## Case 6: Native-style request on likely custom component

### Raw input
> 把這個下拉選單改成 iOS 原生樣式，附截圖

### Expected judgment
- Check whether the component is custom vs native
- If custom, state that this is component replacement, not a simple style tweak
- Reflect higher scope/risk in draft notes

---

## Case 7: Vague UI element naming

### Raw input
> 那個叉叉位置怪怪的

### Expected judgment
- Ask one question for page/component clarification
- Suggest minimal fill-in structure
- Do not fabricate a confident draft

---

## Case 8: Cross-platform mirrored issue

### Raw input
> iOS、Android 都有狀態卡片顏色不一致的問題

### Expected judgment
- Consider whether this is separate implementation, shared design spec, or shared backend data issue
- Do not automatically split or merge without stating the basis

---

## Case 9: Possible duplicate

### Raw input
> 首頁提示區塊又出現了，跟上次很像，附一樣的畫面

### Expected judgment
- Flag possible duplicate or follow-up-to-existing-issue risk
- Still produce usable draft if issue is understandable

---

## Case 10: Sensitive data present

### Raw input
> 某筆交易案例的使用者反映被重複扣款，附帶聯絡資訊與截圖

### Expected judgment
- Warn about sensitive data first
- Ask whether to de-identify before proceeding or continue directly
- Do not echo full sensitive details into the draft unnecessarily

---

## Case 11: Destructive flow

### Raw input
> 使用者按取消操作後要直接清空暫存內容

### Expected judgment
- Draft possible, but suggest confirmation dialog in acceptance criteria
- Do not force it as a hard block

---

## Case 12: Versioned platform API

### Raw input
> iOS 26 的 Liquid Glass 選單想套到這個頁面

### Expected judgment
- Verify release/version reality first
- Consider app minimum supported iOS version
- Include fallback behavior in acceptance criteria if needed

---

## Case 13: Background image seam

### Raw input
> 這個背景看起來有拼接感

### Expected judgment
- Ask first whether the background is intended as tiled repeat or single full-screen image
- Do not jump to implementation blame too early

---

## Case 14: Multi-item mixed batch

### Raw input
> 1. 詳細頁標題消失
> 2. 表單頁偶發閃退
> 3. 想把等待動畫改柔和一點

### Expected judgment
- Enter batch mode
- #1 and #2 likely draft immediately
- #3 likely needs animation/spec judgment
- Keep item numbering clear

---

## Case 15: Reporter role affects wording

### Raw input
> 我是設計師，這個按鈕看起來不對，想調成稿上的樣子

### Expected judgment
- Detect designer role from context
- Avoid telling the user to go ask design
- Ask whether Figma/frame exists or how they plan to provide spec
