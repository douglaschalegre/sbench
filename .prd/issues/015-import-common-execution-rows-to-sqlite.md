---
title: Import Common Execution Rows To SQLite
labels:
  - needs-triage
status: draft
type: AFK
user_stories_covered: 1-12, 35-38, 44-45, 48
---

## What to build

Add the first end-to-end SQLite import path for SBench orchestrator entries. A runner should be able to import existing benchmark entry metadata into a local SQLite database and query one normalized execution row per task, harness, model, archive run, and orchestrator run.

## Acceptance criteria

- [ ] The importer discovers orchestrator entry metadata files under run records and ignores raw harness output directories that are not tied to an entry.
- [ ] Each imported execution has a stable execution identifier derived from run ID, task ID, harness, and archive run.
- [ ] The execution row stores task, track, harness, model, orchestrator status, timeout state, timeout seconds, elapsed seconds, archive path, metadata path, stdout log path, and stderr log path.
- [ ] The execution row derives an elapsed-time bucket from elapsed seconds using stable bucket thresholds.
- [ ] The execution row stores archived file count from orchestrator archived paths.
- [ ] Imports are idempotent: rerunning the importer updates the same execution rows rather than duplicating them.
- [ ] The SQLite schema can be created in an empty local database.
- [ ] Tests cover schema creation, idempotent import, elapsed bucket derivation, and common execution fields without invoking real harnesses.

## Blocked by

None - can start immediately
