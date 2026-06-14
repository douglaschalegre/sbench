---
title: Import OpenCode Token Usage
labels:
  - needs-triage
status: draft
type: AFK
user_stories_covered: 16-28, 33-34, 46, 50, 53
---

## What to build

Extend the cross-harness results importer with OpenCode token usage parsing. OpenCode mixed stdout logs should be parsed tolerantly, and step completion token objects should be aggregated into normalized execution-level token columns.

## Acceptance criteria

- [ ] OpenCode stdout parsing skips non-JSON noise without failing the import.
- [ ] OpenCode step completion events with token objects populate total, input, output, reasoning, cache read, and cache write token fields.
- [ ] OpenCode LLM call count is derived from step completion events that include token objects.
- [ ] The execution row records an OpenCode-specific token usage source identifier.
- [ ] Missing OpenCode token events import successfully with token usage marked unavailable and token fields left null.
- [ ] Transaction items include OpenCode token availability, token buckets, cache-token availability, and LLM-call bucket where available.
- [ ] Tests cover mixed non-JSON and JSON stdout, multiple step completion events, and missing token events.

## Blocked by

- 015-import-common-execution-rows-to-sqlite.md
