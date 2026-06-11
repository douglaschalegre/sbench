---
title: Add OpenCode Harness Adapter
labels:
  - needs-triage
status: completed
type: AFK
user_stories_covered: 6, 15, 26-29, 33, 38, 42-43, 46, 48
---

## What to build

Add an OpenCode harness adapter to the SBench orchestrator. The adapter should construct and run non-interactive OpenCode commands for selected task folders while preserving the fair-run rule that OpenCode only receives the relevant task fixture and writes deliverables into that task's `answer/` folder.

## Acceptance criteria

- [x] OpenCode command construction uses non-interactive execution through `opencode run`.
- [x] OpenCode receives the selected model and standard SBench task prompt shape.
- [x] The OpenCode directory is set to the selected task folder.
- [x] OpenCode is configured for unattended execution with auto-approved permissions.
- [x] OpenCode permission scope is limited by task-directory execution and does not add broader writable directories.
- [x] OpenCode command construction does not expose `evaluation/`, `.prd/`, `issues/`, `protocol/`, templates, previous answers, or hidden expected answers.
- [x] The orchestrator detects a missing OpenCode CLI before starting a selected OpenCode batch.
- [x] OpenCode run settings are recorded in run metadata.
- [x] OpenCode JSON output is captured when requested or available.
- [x] The adapter integrates with orchestrator timeout handling, logging, summary generation, and canonical `rN` answer archiving.
- [x] Tests verify OpenCode command construction, missing-binary detection, task-directory scoping, auto-approval settings, absence of broader writable directories, optional JSON capture, and metadata capture without invoking the real OpenCode CLI.

## Blocked by

- 011-record-run-lifecycle-logs-and-summary.md
