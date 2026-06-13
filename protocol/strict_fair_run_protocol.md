# Strict Fair-Run Protocol

Use this protocol to compare `pydantic-ai-bdi`, OpenClaw, Hermes Agent, or another framework on the same SBench task under comparable conditions.

This protocol is the current protocol for the `smoke` baseline track. Future context-pressure tracks should use their own documented run rules or explicitly state how they extend this protocol.

Current `smoke` task IDs are listed in the README track registry. They are `vendor_selection`, `travel_reimbursement_audit`, and `incident_staffing_plan`.

## Core Rules

- Do not tell the agent it is being evaluated, benchmarked, scored, or compared.
- Expose only the relevant task folder, such as `tasks/vendor_selection`, to the agent.
- Do not expose `evaluation/`, `issues/`, `protocol/`, `templates/`, `PRD.to-prd.md`, or hidden expected-deliverable notes during the run.
- Record the benchmark track for the run. Use `smoke` for the current baseline tasks.
- Use the same model and comparable model settings across frameworks.
- Start a fresh session for every framework-task run.
- Disable persistent memory, retained conversation history, learned skills, or framework-specific long-term context where possible.
- Use a 10-minute timeout per task.
- Keep the task local-file only; do not add external web access or extra data unless the task folder explicitly asks for it.
- Do not compare `smoke` results with future context-pressure results as if they used the same pressure mode.
- Preserve native harness traces, JSON event logs, BDI state summaries, to-do lists, tool traces, or comparable run records when they are naturally available, but do not ask the model to reveal private chain-of-thought or hidden reasoning.

## Run Setup

Record setup details before starting:

- Framework name and version, if known.
- Model name and provider.
- Benchmark track, such as `smoke`.
- Task folder path.
- Whether memory or learned skills were disabled, unavailable, or not applicable.
- Trace capture source and destination, if the selected harness can preserve logs, state summaries, event streams, or tool traces.
- Any framework setup friction before the agent starts the task.

## Standard Task Prompt

Use the same prompt shape for each framework, adapting only what is required to point the framework at the task folder:

```text
You are working in the provided folder. Read task.md and the other local files, then complete the requested work. Create the requested `answer/` folder and put all requested deliverables there.
```

Do not include scoring criteria, expected answers, hidden checklist items, or comparisons to other frameworks in the prompt.

## During The Run

- Start the timer when the agent receives the standard task prompt.
- Do not provide hints about stale sources, expected totals, or correct candidates beyond what is already in the task folder.
- If the agent asks for clarification, answer only with information already visible in the task folder or say that no additional information is available.
- Stop the run at 10 minutes, even if the agent has not finished.
- Preserve the produced `answer/` folder and any scratch file exactly as written.
- Preserve stdout, stderr, JSON events, tool-call logs, BDI state summaries, to-do lists, or other observable state records that the harness already produces.

## After The Run

- Copy or transcribe the produced named deliverables from `answer/` into a result record.
- Score the run manually using `evaluation/manual_checklist.md` and the relevant hidden expected-deliverable note.
- Score each required deliverable independently, even when later deliverables are missing or wrong.
- Record artifact validity separately from work correctness.
- Record trace source, trace availability, and trace limitations separately from artifact correctness.
- Record evidence discipline, contradiction handling, elapsed time, and operational friction.
- Do not let one framework's output or feedback influence a later framework's fresh run.

## Trace And State Preservation

Trace observability scoring is framework-neutral and optional for runs where observable traces or state summaries exist.

Acceptable trace sources include native harness logs, JSON event streams, BDI state summaries, BDI belief/desire/intention/plan snapshots, plan-step history, to-do lists, task plans, tool traces, file-access logs, run summaries, or comparable records produced during normal execution.

Do not prompt the model to disclose private chain-of-thought. Score only externally observable state or summaries that the framework, adapter, or agent explicitly records as part of normal task execution.

When traces are available, preserve the raw file or transcript next to the result record and summarize these fields in the result capture template:

- Trace source.
- Trace availability.
- Trace limitations.
- Which observable goal, intention or task commitment, active plan, current step, completed-step history, and reconsideration signals can be inspected.

Trace quality does not replace final answer correctness. A run with excellent traces and wrong deliverables should be scored as wrong on artifact correctness while receiving trace observability credit.

## Staged Update Tasks

Some context-pressure tasks include a staged update that should not be visible at the start of the run. Use the same staged-update procedure for every framework being compared.

For `community_workshop_replan`:

- Start from a fresh run folder that contains the task's initial files but withholds `staged_update/` from the agent.
- Start the timer when the agent receives the standard task prompt.
- Introduce `staged_update/05_facility_update_2026-06-10.md` after `answer/initial_room_plan.md` exists or after four minutes, whichever comes first.
- Introduce the update by copying or pasting the update content into the visible task folder as `facility_update_2026-06-10.md`, then tell the agent: `A coordinator update has been added to the task folder. Continue the same objective and update the requested deliverables.`
- Do not give hints about which parts of the initial plan should be preserved or changed.
- Score whether the agent repairs the plan while preserving correct completed work.
