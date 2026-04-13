# Evidence and Spec Rules

Use this file when deciding whether the report has enough evidence and valid source of truth.

## Core normalization rules

- Separate actual behavior from expected behavior.
- Flag contradictions between title and description.
- When bug vs feature is unclear, do not over-infer product intent.
- If the title says an element "appears", first verify whether the real issue is that it should not exist.
- If the user provides app version, build number, or environment, include it. If not, do not ask for it.
- Ask at most one follow-up question, and only the most blocking one.

## Source-of-truth rules

- If expected behavior depends on design or product intent, require a source of truth such as Figma with node-id, PRD, or confirmed product decision.
- If the request is feature addition or UX adjustment with no valid source of truth, ask one question:
  - 這個功能有 Figma 或產品決策支持嗎？有的話附上；沒有的話票會標 `needs-spec`，派工前需先補。
- A Figma link is valid only when it includes a clear `node-id` or equivalent frame anchor and the report identifies the target frame or component.
- A root project link without a target frame is weak evidence. Ask for the specific frame.

## Preference vs decision

- If the report uses subjective language such as 「會比較好」「我認為」「建議」「比較好看」「偏好」 or `better` / `prefer`, and there is no approved spec, classify as `needs-product-decision`, not dispatch-ready UX adjustment.
- If the report is exploratory or half-formed, such as 「在想」「是不是」「會不會」「好像」「有沒有辦法」「可不可以考慮」 or `maybe` / `wondering if`, classify as `needs-product-decision`.

## Evidence rules

- A video alone is insufficient when the issue remains unclear.
- A video without timestamp, screen marking, or explicit symptom description is weak evidence.
- If a UI visual issue is reported with no screenshot, suggest attaching one, but do not block the flow.
- If screenshots or video exist, mention them as evidence in the draft and attach them when the execution path supports attachments.

## Platform/version compatibility rules

- If the report references a specific OS version, API, or design language, verify release status with web search before relying on it.
- After confirming availability, check the app's minimum supported version and include fallback behavior if needed.
- When a feature depends on a versioned API, acceptance criteria should explicitly cover both target-version behavior and fallback behavior on older supported versions.
