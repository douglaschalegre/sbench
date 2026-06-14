---
title: Import Codex Token Usage
labels:
  - needs-triage
status: draft
type: AFK
user_stories_covered: 16-28, 32, 46, 50, 53
---

## What to build

Extend the cross-harness results importer with Codex token usage parsing. Codex turn completion events should populate normalized token columns while preserving cached input and reasoning token counts.

## Acceptance criteria

- [ ] Codex turn completion events populate input, cached input, output, and reasoning token fields.
- [ ] Codex total token usage is derived consistently from the available Codex usage fields.
- [ ] Codex LLM call count is derived from turn completion events.
- [ ] The execution row records a Codex-specific token usage source identifier.
- [ ] Missing Codex usage imports successfully with token usage marked unavailable and token fields left null.
- [ ] Transaction items include Codex token availability, token buckets, cache-token availability, and LLM-call bucket where available.
- [ ] Tests cover Codex turn completion usage with cached input and reasoning token counts.

## Blocked by

- 015-import-common-execution-rows-to-sqlite.md
