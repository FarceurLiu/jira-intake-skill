# UI and Animation Rules

Use this file for UI-heavy reports, component interpretation, animation behavior, and implementation-scope judgment.

## UI and component rules

- If the report identifies a page and UI component, normalize the requested action as one of: remove, add, adjust, fix, investigate.
- If the report uses vague UI names such as 「叉叉」「那個東西」「那邊」「那個按鈕」, stop and ask for page, component, and what looks wrong.
- For micro UI adjustments such as spacing, padding, color, font weight, radius, animation feel, alignment, require at least: page, component, current state, target state, source of truth, acceptance method. Otherwise classify as `blocked` or `needs-product-decision`.
- When the issue mentions a background image seam or tiling artifact, ask first whether the asset is intended to repeat as tiles or display as a single full-screen image.

## Native vs custom component rules

- When a request says "switch to native style", verify whether the current component is already native.
- If the screenshot or description indicates a custom component, state clearly that this is a component replacement, not a simple style tweak.
- Use screenshots not only as evidence, but also to infer whether a component is native or custom. This affects effort and risk.

## Animation rules

- For animation issues, require three things: current behavior, expected behavior, and start/end states of each concurrent animation.
- If any of the three is missing, mark as `blocked` and ask the single most blocking question.
- If the reporter does not know the target animation spec, switch to: engineer proposes initial value, reporter validates after implementation.
- Do not hardcode animation numbers in the skill. Let engineering choose a reasonable starting point by animation type.

## Cross-ticket and cross-platform rules

- If similar items appear across iOS, Android, Web, or API, first decide whether they are separate implementation issues, a shared spec issue, or a shared backend/data root cause.
- If the new item overlaps strongly with an existing ticket in page, component, Figma node, attachment, wording, or symptom, mark it as `possible-duplicate` or `possible-follow-up-to-existing-issue`.
