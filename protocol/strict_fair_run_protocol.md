# Strict Fair-Run Protocol

Use this protocol to compare `pydantic-ai-bdi`, OpenClaw, Hermes Agent, or another framework on the same SBench task under comparable conditions.

## Core Rules

- Do not tell the agent it is being evaluated, benchmarked, scored, or compared.
- Expose only the relevant task folder, such as `tasks/vendor_selection`, to the agent.
- Do not expose `evaluation/`, `issues/`, `protocol/`, `templates/`, `PRD.to-prd.md`, or hidden expected-deliverable notes during the run.
- Use the same model and comparable model settings across frameworks.
- Start a fresh session for every framework-task run.
- Disable persistent memory, retained conversation history, learned skills, or framework-specific long-term context where possible.
- Use a 10-minute timeout per task.
- Keep the task local-file only; do not add external web access or extra data unless the task folder explicitly asks for it.

## Run Setup

Record setup details before starting:

- Framework name and version, if known.
- Model name and provider.
- Task folder path.
- Whether memory or learned skills were disabled, unavailable, or not applicable.
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

## After The Run

- Copy or transcribe the produced named deliverables from `answer/` into a result record.
- Score the run manually using `evaluation/manual_checklist.md` and the relevant hidden expected-deliverable note.
- Score each required deliverable independently, even when later deliverables are missing or wrong.
- Record artifact validity separately from work correctness.
- Record evidence discipline, contradiction handling, elapsed time, and operational friction.
- Do not let one framework's output or feedback influence a later framework's fresh run.
