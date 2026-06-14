---
title: Import BDI Token Usage
labels:
  - needs-triage
status: draft
type: AFK
user_stories_covered: 16-31, 46, 50-52
---

## What to build

Extend the cross-harness results importer with BDI token usage parsing. Current BDI logs should populate normalized token columns from the final aggregate run event, with per-agent completed events used as a fallback when no aggregate is available.

## Acceptance criteria

- [ ] Current BDI aggregate run events populate total, input, output, cached input, cache read, cache write, audio token fields, LLM calls, and tool calls when present.
- [ ] BDI per-agent completed events can be summed as a fallback when the final aggregate event is absent.
- [ ] Older BDI logs without token events import successfully with token usage marked unavailable and token fields left null.
- [ ] Measured zero token subfields remain zero while unavailable token subfields remain null.
- [ ] The execution row records a BDI-specific token usage source identifier.
- [ ] Transaction items include BDI token availability, token buckets, LLM-call bucket, and tool-call bucket where available.
- [ ] Tests cover current aggregate logs, fallback per-agent logs, and no-token BDI logs.

## Blocked by

- 015-import-common-execution-rows-to-sqlite.md
