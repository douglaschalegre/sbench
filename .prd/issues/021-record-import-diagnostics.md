---
title: Record Import Diagnostics
labels:
  - needs-triage
status: draft
type: AFK
user_stories_covered: 27-28, 38, 42, 55
---

## What to build

Add import diagnostics for parser gaps and incomplete source artifacts. The importer should preserve execution rows when possible while recording warnings that explain missing token usage, malformed logs, unknown deliverable contracts, or other non-fatal import limitations.

## Acceptance criteria

- [ ] Import warnings are stored separately from execution rows.
- [ ] Missing stdout logs can produce a warning without preventing common metadata import.
- [ ] Malformed JSON log lines can produce warnings without failing tolerant parsing of later valid lines.
- [ ] Unknown or unparsable deliverable contracts can produce a warning and leave deliverable completion unknown.
- [ ] Missing token usage can produce a warning while keeping token fields null and token usage unavailable.
- [ ] Reimporting an execution replaces stale diagnostics for that execution.
- [ ] Tests cover non-fatal warnings for missing logs, malformed JSON, unknown contracts, and missing token usage.

## Blocked by

- 017-import-bdi-token-usage.md
- 018-import-codex-token-usage.md
- 019-import-opencode-token-usage.md
