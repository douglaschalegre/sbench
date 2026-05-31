# Add Incident Staffing Plan Tracer Task

## Type

AFK

## User Stories Covered

1-14, 19, 28-31, 32, 35, 37-39, 48-49

## What to build

Build the third complete SBench task slice: a local-file Incident Staffing Plan fixture that can be given to any agent framework as a standalone folder. The agent should read staffing rules, schedule data, availability notes, and the newest access update; then choose primary and backup responders and write `answer.json` using the shared SBench JSON shape.

This slice should be independently runnable and manually scoreable.

## Acceptance criteria

- [ ] An `incident_staffing_plan` task folder exists with all agent-facing fixture files.
- [ ] The task instruction asks the agent to choose primary and backup responders and write only `answer.json`.
- [ ] The fixture includes coverage rules, schedule data, availability notes, and a newer access update.
- [ ] The correct answer depends on using the latest access update.
- [ ] The expected primary responder is `Ben`.
- [ ] The expected backup responder is `Deepa`.
- [ ] The fixture includes ineligible candidates with clear reasons such as unavailable, over limit, missing access, or role-rule mismatch.
- [ ] The task has a hidden local expected-answer note outside the agent-facing task folder.
- [ ] The task can be completed by reading local files only.

## Blocked by

- 001-add-vendor-quote-selection-tracer-task.md
