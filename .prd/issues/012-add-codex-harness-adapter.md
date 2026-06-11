---
title: Add Codex Harness Adapter
labels:
  - needs-triage
status: completed
type: AFK
user_stories_covered: 6, 22-25, 33, 38, 42-43, 46, 48
---

## What to build

Add a Codex harness adapter to the SBench orchestrator. The adapter should construct and run non-interactive Codex commands for selected task folders while preserving the fair-run rule that Codex only receives the relevant task fixture and writes deliverables into that task's `answer/` folder.

## Acceptance criteria

- [x] Codex command construction uses non-interactive execution through `codex exec`.
- [x] Codex receives the selected model and standard SBench task prompt shape.
- [x] The Codex working directory is set to the selected task folder.
- [x] Codex is configured for unattended automation with no approval prompts.
- [x] Codex sandbox settings allow writing answer files in the task folder.
- [x] Codex command construction does not expose `evaluation/`, `.prd/`, `issues/`, `protocol/`, templates, previous answers, or hidden expected answers.
- [x] The orchestrator detects a missing Codex CLI before starting a selected Codex batch.
- [x] Codex command invocation and sandbox settings are recorded in run metadata.
- [x] The adapter integrates with orchestrator timeout handling, logging, summary generation, and canonical `rN` answer archiving.
- [x] Tests verify Codex command construction, missing-binary detection, task-directory scoping, no-approval settings, sandbox settings, and metadata capture without invoking the real Codex CLI.

## Blocked by

- 011-record-run-lifecycle-logs-and-summary.md
