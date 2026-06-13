---
title: SBench Benchmark Run Orchestrator
labels:
  - needs-triage
status: draft
---

## Problem Statement

SBench currently has a practical execution gap. The BDI harness can run all SBench tasks from the `pydantic-ai-bdi` repository with one command through the existing toy runner. Codex and OpenCode, however, still require manual task-by-task execution. That manual workflow is manageable for the current small smoke suite, but it will become infeasible as SBench expands with long-context, replanning, recovery, distractor-goal, and observability tasks.

The user needs a single benchmark entry point that can run the selected SBench tasks across the selected harnesses, preserve fair-run constraints, archive answers automatically, capture logs, and keep result paths consistent with the current answer archive convention. Without this, benchmark expansion will increase operational friction and make repeated comparisons difficult to reproduce.

The current answer archive uses incremental run folders such as `r1`, `r2`, and `r3`. Those are not arbitrary manual labels; they represent the run number for a given task, model, and harness. The orchestrator must preserve this convention by automatically selecting the next available run number when saving outputs.

## Solution

Create a benchmark orchestrator in the SBench repository. The orchestrator should provide one command that runs a selected matrix of harnesses and tasks. The first supported harnesses are BDI, Codex, and OpenCode only.

The orchestrator should discover task folders from SBench, execute each selected task in a fresh harness invocation, enforce per-task timeout behavior, capture stdout/stderr or JSON events, archive produced `answer/` files, and write a machine-readable run summary. It should keep agent-facing exposure limited to the relevant task folder and should not expose `evaluation/`, `.prd/`, `issues/`, `protocol/`, templates, previous answers, or hidden expected answers during a run.

Codex and OpenCode should be run through their non-interactive CLIs. Codex should run with its working directory set to the task folder and with approval disabled for automation. OpenCode should run with its directory set to the task folder and auto-approved permissions, but the permission scope should be limited to that task directory by not adding additional writable directories. BDI should be run through the SBench toy runner in the `pydantic-ai-bdi` repository; the BDI runner should later become CLI-parameterized by the companion BDI PRD.

The orchestrator should centralize output archiving. Harnesses should write deliverables into `tasks/<task_id>/answer/` during execution. After each task run, the orchestrator should move or copy those produced deliverables into `answers/<task_id>/<model>/<harness>/rN/`, where `rN` is the next incremental run folder for that exact task, model, and harness. The orchestrator should then clean the task-local `answer/` directory before the next run to prevent cross-harness contamination.

The orchestrator should also create run-level logs and metadata records under a dedicated run record area. Those records should include the task-derived benchmark track, task ID, harness, model, command invocation, start time, end time, elapsed time, timeout status, exit code, answer archive path, and log paths.

## User Stories

1. As a benchmark runner, I want one SBench command to run the benchmark matrix, so that I do not need to invoke every harness and task manually.
2. As a benchmark runner, I want to select `bdi`, `codex`, and `opencode`, so that the initial automation covers the currently relevant harnesses.
3. As a benchmark runner, I want to select one harness, several harnesses, or all supported harnesses, so that I can rerun only the comparisons I need.
4. As a benchmark runner, I want to select one task, several tasks, or all task folders, so that I can run small experiments or the whole suite.
5. As a benchmark runner, I want task discovery to use folders with `task.md`, so that new SBench tasks are picked up without changing runner code.
6. As a benchmark runner, I want the runner to preserve the standard SBench prompt shape, so that harnesses receive comparable instructions.
7. As a benchmark runner, I want every harness-task run to start from a clean `answer/` folder, so that previous outputs do not contaminate the current run.
8. As a benchmark runner, I want produced answers archived automatically, so that I do not need to run `move_answers.sh` by hand after each task.
9. As a benchmark runner, I want answer archives to use `answers/<task>/<model>/<harness>/rN/`, so that the current archive structure remains intact.
10. As a benchmark runner, I want `rN` to be selected incrementally, so that repeated runs do not overwrite earlier results.
11. As a benchmark runner, I want the next run number to be computed per task, model, and harness, so that `r3` for one task does not force `r3` everywhere else.
12. As a benchmark runner, I want the runner to detect existing `r1`, `r2`, and `r3` folders, so that it can choose the next available folder correctly.
13. As a benchmark runner, I want the runner to refuse to overwrite existing answer archives unless explicitly allowed, so that benchmark results are not lost.
14. As a benchmark runner, I want each task run to have stdout and stderr logs, so that failures can be diagnosed later.
15. As a benchmark runner, I want JSON event logs captured when a harness exposes them, so that trace analysis can be added later.
16. As a benchmark runner, I want a run summary file, so that I can see which tasks passed, timed out, failed, or produced outputs.
17. As a benchmark runner, I want per-task elapsed time recorded automatically, so that timing tables do not depend on manual timing.
18. As a benchmark runner, I want timeout status recorded automatically, so that unfinished runs are visible.
19. As a benchmark runner, I want the configured timeout to be the same across harnesses by default, so that the comparison remains fair.
20. As a benchmark runner, I want to override timeout from the command line, so that context-pressure tracks can use longer limits when needed.
21. As a benchmark runner, I want the task-derived benchmark track recorded, so that smoke and context-pressure results are not conflated.
22. As a benchmark runner, I want Codex to run non-interactively, so that it can be included in unattended benchmark batches.
23. As a benchmark runner, I want Codex to use the task folder as its working directory, so that it only sees the intended fixture.
24. As a benchmark runner, I want Codex to run with approval disabled for automation, so that a batch does not stop waiting for manual confirmation.
25. As a benchmark runner, I want Codex sandbox settings recorded, so that permission choices are transparent.
26. As a benchmark runner, I want OpenCode to run non-interactively, so that it can be included in unattended benchmark batches.
27. As a benchmark runner, I want OpenCode to use the task folder as its directory, so that it only sees the intended fixture.
28. As a benchmark runner, I want OpenCode auto-approval to be limited by task-directory scope, so that automation does not unnecessarily expose the whole SBench repository.
29. As a benchmark runner, I want OpenCode run settings recorded, so that permission choices are transparent.
30. As a benchmark runner, I want BDI to be included in the same orchestration command, so that BDI, Codex, and OpenCode are comparable in one workflow.
31. As a benchmark runner, I want the orchestrator to call the BDI toy runner from the BDI repository, so that existing BDI behavior can be reused.
32. As a benchmark runner, I want BDI output archiving to be handled by SBench, so that all harness outputs share one archive convention.
33. As a benchmark runner, I want harness command construction to be explicit, so that I can audit exactly what was run.
34. As a benchmark runner, I want a dry-run mode, so that I can inspect the planned matrix and commands before spending model budget.
35. As a benchmark runner, I want a list mode, so that I can see discovered tasks and supported harnesses.
36. As a benchmark runner, I want failed harness-task runs to continue to the next selected run by default, so that one failure does not waste the whole batch.
37. As a benchmark runner, I want an option to stop on first failure, so that debugging sessions can fail fast.
38. As a benchmark runner, I want missing CLI binaries to be detected before a batch starts, so that configuration errors are caught early.
39. As a benchmark runner, I want missing repository paths to be detected before a batch starts, so that BDI integration failures are caught early.
40. As a benchmark runner, I want task-local scratch files preserved or recorded according to policy, so that agent behavior can be inspected after a run.
41. As a benchmark runner, I want task-local scratch files not to pollute later runs, so that every harness starts from the same fixture state.
42. As a benchmark runner, I want the runner to avoid exposing hidden expected answers, so that benchmark integrity is preserved.
43. As a benchmark runner, I want the runner to avoid exposing previous answer archives, so that agents cannot copy prior outputs.
44. As a benchmark runner, I want model name normalization for archive paths, so that model identifiers with slashes do not break paths.
45. As a benchmark runner, I want display model names recorded separately from path-safe model names, so that reports remain readable.
46. As a benchmark maintainer, I want harness adapters to be isolated behind small interfaces, so that adding another harness later does not rewrite the whole runner.
47. As a benchmark maintainer, I want archive planning to be testable without running agents, so that overwrite prevention can be trusted.
48. As a benchmark maintainer, I want command construction to be testable without invoking Codex or OpenCode, so that CLI changes can be caught cheaply.
49. As a benchmark maintainer, I want task cleanup to be testable on temporary fixtures, so that contamination prevention can be trusted.
50. As a benchmark maintainer, I want run summary generation to be deterministic, so that later evaluator automation can consume it.
51. As a BDI researcher, I want all harnesses to be run through the same SBench orchestration layer, so that differences are less likely to come from manual execution mistakes.
52. As a BDI researcher, I want operational friction to be reduced, so that expanded benchmark runs remain feasible.

## Implementation Decisions

- Build the orchestrator in the SBench repository rather than inside any one harness repository.
- Support only BDI, Codex, and OpenCode in the first implementation.
- Use a command-line interface that accepts selected harnesses, selected tasks, model, track, timeout, and dry-run options.
- Discover tasks by scanning task directories that contain `task.md`.
- Use the standard SBench task prompt from the run protocol for Codex and OpenCode.
- Keep BDI execution delegated to the BDI toy runner initially.
- Centralize answer archiving in the SBench orchestrator.
- Treat `tasks/<task_id>/answer/` as the temporary task-local output directory for one harness-task run.
- Clean or recreate the task-local `answer/` directory before each harness-task run.
- Archive produced deliverables after each harness-task run.
- Use `answers/<task_id>/<model_path>/<harness>/rN/` as the answer archive convention.
- Compute `rN` by scanning existing run folders for the same task, model path, and harness, then selecting the next integer.
- Preserve existing run folders and avoid overwriting them by default.
- Record display model names and path-safe model names separately when needed.
- Capture stdout, stderr, exit code, start time, end time, elapsed time, timeout status, command, task ID, harness, model, track, and archive path in run metadata.
- Prefer a run-record directory for logs and summaries instead of mixing logs into answer folders.
- Use Codex non-interactive execution through `codex exec`.
- Set Codex working directory to the task folder.
- Configure Codex for automation with no approval prompts.
- Use a Codex sandbox mode that permits writing answer files in the task folder.
- Use OpenCode non-interactive execution through `opencode run`.
- Set OpenCode directory to the task folder.
- Use OpenCode auto-approved permissions for unattended execution, while limiting scope to the task directory.
- Do not pass additional writable directories to OpenCode in the first implementation.
- Capture OpenCode JSON output when requested or available.
- Detect required CLI binaries before executing selected harnesses.
- Detect required repository paths before executing BDI.
- Continue after individual task failures by default.
- Provide an option to stop after the first failure.
- Provide dry-run output that shows the planned matrix, archive destinations, and commands without invoking agents.
- Do not perform manual or deterministic scoring in the first orchestrator implementation.
- Do not move hidden expected answers or scoring checklists into agent-facing folders.

## Testing Decisions

Good tests should verify runner behavior without spending model budget or invoking real agent harnesses. Tests should focus on task discovery, command construction, cleanup, archive planning, run metadata, and failure handling.

- Test that task discovery returns folders containing `task.md` and ignores non-task folders.
- Test that harness selection accepts `bdi`, `codex`, and `opencode` and rejects unsupported harness names.
- Test that archive planning chooses `r1` when no prior runs exist.
- Test that archive planning chooses `r3` when `r1` and `r2` already exist.
- Test that archive planning is scoped per task, model, and harness.
- Test that existing archive directories are not overwritten by default.
- Test that model names are converted into path-safe archive path segments when needed.
- Test that the task-local `answer/` directory is cleaned before a run.
- Test that produced answer files are archived into the selected `rN` directory.
- Test that missing answer files are recorded as an incomplete run rather than silently treated as success.
- Test that Codex command construction includes non-interactive execution, model, task directory, sandbox, and no-approval settings.
- Test that OpenCode command construction includes non-interactive execution, model, task directory, format, and auto-approval settings.
- Test that OpenCode command construction does not add broader writable directories.
- Test that BDI command construction points to the BDI repository and runner entry point.
- Test dry-run mode without invoking any harness process.
- Test run summary generation for success, timeout, and nonzero-exit cases.
- Test that one failed run does not prevent later matrix entries unless stop-on-failure is enabled.

Prior art exists in SBench's current answer archive layout, `move_answers.sh`, the strict fair-run protocol, and the result capture template. The orchestrator should reuse those conventions rather than inventing a separate result structure.

## Out of Scope

- Supporting harnesses beyond BDI, Codex, and OpenCode in the first implementation.
- Implementing manual scoring or deterministic evaluation.
- Changing the task fixtures themselves.
- Changing hidden expected answers.
- Running browser automation or external services.
- Giving agents access to the whole SBench repository during task execution.
- Exposing `evaluation/`, `.prd/`, `issues/`, `protocol/`, templates, previous answers, or hidden expected answers to agents.
- Optimizing BDI internals.
- Replacing the BDI toy runner in the first SBench orchestrator slice.
- Publishing issues or results to GitHub.

## Further Notes

The first useful slice is a dry-run-capable orchestrator that can run Codex and OpenCode task-by-task automatically, archive outputs with incremental `rN`, and record logs. BDI can be connected through the existing toy runner first, then improved once the BDI toy runner accepts CLI parameters.

The important fairness constraint is directory scope. Codex and OpenCode automation may need no-approval or auto-approval flags, but their working directory should be the task folder and they should not receive additional writable directories. This keeps unattended execution practical while preserving the SBench rule that each run sees only the relevant task fixture.
