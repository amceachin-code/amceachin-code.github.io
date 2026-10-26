# Lessons

## 2026-10-16: Check new heading levels in dark mode

- What happened: the tools page got new h3 sub-headings. They looked fine in a light-mode build but were invisible on the live site for visitors whose OS is in dark mode.
- Why: `custom.css` keeps the page white under `.dark`, but the theme's dark prose styles still recolor headings. Only h2 had a pinned color.
- Follow-up: page titles (h1) had the same bug on every page; fixed in the same rule.
- Rule: when adding a heading level or prose element the site has not used before, check it with dark mode emulated, not just light mode.

## 2026-10-25: "descending order" meant the item numbers, not the sort
- What happened: asked to fix journal articles "not in descending order," I checked the year sort, found it correct, and reported nothing to fix. The user meant the list numbers, which counted 1, 2, 3 instead of N, N-1, ... 1.
- Why: I picked one reading of "order" and verified that reading instead of asking or checking the other visible ordering in the list.
- Rule: when a request about "order" could mean the sort or the numbering, check both in the rendered output, or ask.
- Also: enumitem does not evaluate arithmetic placed directly in a `label`. Register a counter style with `\AddEnumerateCounter` and use it like `\arabic*`.
