---
title: Add Orchestrator CLI List And Dry Run
labels:
  - needs-triage
status: completed
type: AFK
user_stories_covered: 1-6, 21, 33-35
---

## What to build

Add the initial SBench benchmark orchestrator entry point with task discovery, harness selection, task selection, model, track, timeout, list, and dry-run behavior. A runner should be able to inspect the supported harnesses, discovered task folders, planned benchmark matrix, command shapes, and canonical answer archive destinations without invoking any agent harness.

## Acceptance criteria

- [x] The orchestrator exposes one command-line entry point for SBench benchmark runs.
- [x] Task discovery returns task folders that contain `task.md` and ignores non-task folders.
- [x] Harness selection accepts `bdi`, `codex`, and `opencode` and rejects unsupported harness names.
- [x] The command accepts selected tasks, selected harnesses, model, benchmark track, timeout, and dry-run options.
- [x] List mode prints discovered tasks and supported harnesses without running agents.
- [x] Dry-run mode prints the planned task/harness matrix without running agents.
- [x] Dry-run mode shows the planned command shape for each selected matrix entry.
- [x] Dry-run mode shows the planned canonical archive destination under `answers/<task_id>/<model_path>/<harness>/rN/`.
- [x] The standard SBench task prompt shape is represented for Codex and OpenCode command planning.
- [x] Tests cover task discovery, harness selection, option parsing, list mode, and dry-run planning without invoking real harnesses.

## Blocked by

None - can start immediately.
