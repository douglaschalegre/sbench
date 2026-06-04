---
title: Add Trace Observability Scoring
labels:
  - needs-triage
status: draft
type: AFK
user_stories_covered: 5, 23-26, 36, 38-39, 41, 45-47
---

## What to build

Add a framework-neutral trace observability scoring path that can be applied after a run using native harness logs, BDI state summaries, to-do lists, tool traces, or comparable run records. The score should make execution state more inspectable without requiring private model reasoning and without substituting trace quality for final answer correctness.

## Acceptance criteria

- [ ] The run protocol explains how to preserve native harness traces or state summaries after a run when available.
- [ ] The result capture template includes fields for trace source, trace availability, and trace limitations.
- [ ] The manual checklist can score whether a trace exposes current goal, current intention or equivalent task commitment, active plan, current step, completed-step history, and reason for reconsideration.
- [ ] BDI-specific observable state such as beliefs, desires, intentions, plans, plan steps, plan-step history, belief updates, and reconsideration reason can receive trace credit.
- [ ] Non-BDI observable state such as to-do entries, task plans, summaries, tool traces, or logs can receive comparable partial trace credit.
- [ ] Trace scoring explicitly avoids private chain-of-thought or hidden model reasoning.
- [ ] Trace observability is recorded independently from artifact correctness.
- [ ] The long-context task has enough trace-scoring guidance to be evaluated with this observability path.

## Blocked by

- 001-label-smoke-baseline-track.md
- 002-add-long-context-fixture-slice.md
