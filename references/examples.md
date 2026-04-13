# Examples

## Example 1: Video-only QA report

### Raw input
Title: iOS onboarding screen collapses unexpectedly when re-entering the page
Description: attached video only

### Intake judgment
- Type: unclear, likely bug
- Dispatch status: blocked
- Why: actual behavior is partially visible, but expected behavior and exact affected element are unclear

### Follow-up question (ask only the most blocking one)
- Which section or component is collapsing, and what should it do instead?

## Example 2: Title says page has B

### Raw input
Title: Home page has info banner
Description: simple screenshot

### Intake judgment
- Type: unclear
- Dispatch status: blocked
- Why: unclear whether the info banner is incorrectly shown or should have been added but is missing in some states

### Follow-up question (ask only the most blocking one)
- Is the problem that this page should not show this banner, or that it is missing where it should appear?

## Example 3: C page should add B

### Raw input
Title: Detail page should show status badge
Description: stakeholder says this should be added

### Intake judgment
- Type: feature request or spec correction
- Dispatch status: ready only after expected placement and behavior are clear

### Required normalization
- rewrite title to explicit action
- specify placement, trigger, and acceptance criteria
