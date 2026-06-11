---
title: Connect BDI Toy Runner Adapter
labels:
  - needs-triage
status: completed
type: AFK
user_stories_covered: 30-33, 39, 46, 48, 51-52
---

## What to build

Connect BDI to the SBench orchestrator through the existing toy runner in the `pydantic-ai-bdi` repository. SBench should own run orchestration, logs, metadata, timeouts, and canonical answer archiving so BDI, Codex, and OpenCode results are comparable through one workflow.

## Acceptance criteria

- [x] BDI command construction points to a configurable `pydantic-ai-bdi` repository path.
- [x] The orchestrator detects a missing BDI repository path before starting a selected BDI batch.
- [x] BDI execution delegates to the existing toy runner rather than replacing BDI internals in this slice.
- [x] BDI output archiving is handled by SBench through canonical `answers/<task_id>/<model_path>/<harness>/rN/` destinations.
- [x] BDI run metadata records the command invocation, repository path, task ID, harness, model, track, timeout, logs, exit code, and archive path.
- [x] BDI runs integrate with orchestrator timeout handling, logging, summary generation, continue-on-failure behavior, and stop-on-first-failure behavior.
- [x] BDI command construction is explicit enough to audit exactly what was run.
- [x] Tests verify BDI command construction, missing-repository detection, metadata capture, and integration with canonical archiving without invoking the real BDI toy runner.

## Blocked by

- 011-record-run-lifecycle-logs-and-summary.md
