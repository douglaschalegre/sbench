---
title: Generate Apriori Transaction Items
labels:
  - needs-triage
status: draft
type: AFK
user_stories_covered: 39-43, 49
---

## What to build

Generate stable Apriori-ready transaction items from normalized execution rows. The generated items should represent common benchmark facts and bucketed numeric values without embedding raw high-cardinality numbers.

## Acceptance criteria

- [ ] Transaction items are generated for task, track, harness, orchestrator status, timeout state, elapsed bucket, deliverable completion, and archived-file-count bucket.
- [ ] Transaction items are generated for token usage availability and token buckets when token data is available.
- [ ] Transaction items are generated for LLM-call and tool-call buckets when those values are available.
- [ ] Raw continuous values such as elapsed seconds, token totals, and call counts are not emitted directly as item names.
- [ ] Regenerating items for an execution replaces stale items instead of appending duplicates.
- [ ] Tests verify generated item sets from normalized execution records rather than raw logs.

## Blocked by

- 016-detect-archived-deliverable-completion.md
- 017-import-bdi-token-usage.md
- 018-import-codex-token-usage.md
- 019-import-opencode-token-usage.md
