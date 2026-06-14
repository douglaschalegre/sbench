---
title: Verify Full Cross-Harness Import
labels:
  - needs-triage
status: draft
type: AFK
user_stories_covered: 1-55
---

## What to build

Add an end-to-end verification path that imports representative BDI, Codex, and OpenCode orchestrator entries into SQLite and proves that the resulting rows and transaction items are comparable across harnesses.

## Acceptance criteria

- [ ] The verification path imports representative BDI, Codex, and OpenCode entries from existing run artifacts or compact test fixtures.
- [ ] Imported BDI, Codex, and OpenCode rows share the same normalized execution columns.
- [ ] Token usage columns are populated where each harness exposes data and left null where fields are unavailable.
- [ ] Transaction items are generated for each representative execution.
- [ ] The verification demonstrates idempotent import and item regeneration across multiple importer runs.
- [ ] The verification does not read hidden expected-answer files and does not infer final answer correctness.
- [ ] Tests cover the end-to-end import path without invoking real harness processes.

## Blocked by

- 020-generate-apriori-transaction-items.md
- 021-record-import-diagnostics.md
