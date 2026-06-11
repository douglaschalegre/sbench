---
title: Record Run Lifecycle Logs And Summary
labels:
  - needs-triage
status: completed
type: AFK
user_stories_covered: 14-20, 36-37, 40-41, 50
---

## What to build

Add process execution lifecycle handling to the orchestrator so every selected harness-task run produces diagnosable logs and deterministic metadata. A runner should be able to see which runs succeeded, failed, timed out, produced answers, and where the archived answers and logs were written.

## Acceptance criteria

- [x] Each harness-task run records stdout and stderr logs under a dedicated run record area.
- [x] JSON event logs are captured when a selected harness exposes them or the orchestrator requests them.
- [x] Run metadata records benchmark track, task ID, harness, model, command invocation, start time, end time, elapsed time, timeout status, exit code, answer archive path, and log paths.
- [x] The configured timeout is applied consistently across harnesses by default.
- [x] Timeout can be overridden from the command line.
- [x] A timeout is recorded distinctly from a nonzero process exit.
- [x] Failed or incomplete runs continue to the next selected matrix entry by default.
- [x] A stop-on-first-failure option stops the batch after the first failed, timed-out, or incomplete run.
- [x] The run summary is machine-readable and deterministic enough for later evaluator automation.
- [x] Task-local scratch files are handled according to an explicit policy so they do not pollute later runs.
- [x] Tests cover success, timeout, nonzero exit, missing answer files, continue-on-failure behavior, stop-on-first-failure behavior, and deterministic summary generation without invoking real harnesses.

## Blocked by

- 009-add-orchestrator-cli-list-and-dry-run.md
- 010-archive-answers-with-canonical-rn-runs.md
