---
title: Label The Smoke Baseline Track
labels:
  - needs-triage
status: draft
type: AFK
user_stories_covered: 1, 27-29, 37, 50-51
---

## What to build

Make the existing smoke suite explicitly identifiable as the `smoke` baseline track without changing the current smoke tasks or completed result archive. A runner should be able to run the existing tasks exactly as before, record them as smoke-track results, and avoid comparing them accidentally with context-pressure runs.

## Acceptance criteria

- [ ] The existing smoke task folders remain unchanged in behavior and deliverable expectations.
- [ ] The suite documentation identifies the current tasks as the `smoke` baseline track.
- [ ] The strict fair-run protocol records the selected benchmark track for each run.
- [ ] The result capture template includes a track field that can distinguish `smoke` from future context-pressure tracks.
- [ ] The documentation warns not to conflate strict smoke results with expanded context-pressure results.
- [ ] The change does not move hidden expected answers into any agent-facing task folder.

## Blocked by

None - can start immediately.
