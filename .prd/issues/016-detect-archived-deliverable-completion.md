---
title: Detect Archived Deliverable Completion
labels:
  - needs-triage
status: draft
type: AFK
user_stories_covered: 13-15, 39-43, 47
---

## What to build

Extend the SQLite import path so each execution can report whether the archived answer files satisfy the visible task deliverable contract. The importer should compare required `answer/` filenames from the task contract with archived filenames recorded by the orchestrator and generate deliverable-related transaction items.

## Acceptance criteria

- [ ] Required deliverable filenames are extracted from visible task deliverable contracts without reading hidden evaluation files.
- [ ] The importer stores `deliverables_present` as true when all required deliverables are archived.
- [ ] The importer stores `deliverables_present` as false when at least one required deliverable is missing from archived outputs.
- [ ] The importer stores `deliverables_present` as null when required deliverables cannot be determined.
- [ ] Archived file count remains available alongside deliverable completion.
- [ ] Transaction items include deliverable completion and archived-file-count bucket items.
- [ ] Tests cover all-present, partially-present, missing, and unknown-contract cases.

## Blocked by

- 015-import-common-execution-rows-to-sqlite.md
