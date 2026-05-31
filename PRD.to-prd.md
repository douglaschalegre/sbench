# SBench Local Ops Smoke Suite PRD

## Problem Statement

The user wants to compare `pydantic-ai-bdi`, OpenClaw, and Hermes Agent without taking on the setup overhead of a full benchmark environment. Existing benchmark styles such as TheAgentCompany provide useful checkpoint-based structure, but they require containers, services, workplace apps, and local infrastructure that are too heavy for an initial framework comparison.

The user needs a simple benchmark that gives a credible first glimpse into how each framework behaves on the same task type. The benchmark should exercise useful agent capabilities such as reading local files, finding relevant facts, resolving contradictions, doing small calculations, and producing semi-structured workplace deliverables. It should not require a repository, browser automation, hosted services, or framework-specific integrations.

The user also wants evaluation to happen independently after task completion. The agent should not know that it is being evaluated and should not see checkpoints, hidden expected values, or scoring criteria while working.

## Solution

Create SBench, a lightweight local-file smoke benchmark made of three tiny operations-style tasks. Each task is represented by a small fixture pack of plain files. The agent receives only the task instruction and access to the files, then writes multiple named deliverables that resemble real workplace artifacts.

The first smoke suite includes:

1. Vendor Quote Selection
2. Travel Reimbursement Audit
3. Incident Staffing Plan

Each task includes one stale or conflicting source that the agent must resolve using source recency or explicit instruction. Each task is small enough to run manually in a fresh session with a 10-minute timeout, but rich enough to reveal differences in planning, file search, evidence use, arithmetic, source handling, and checkpointable work production.

The benchmark uses per-task deliverable contracts with exact filenames and semi-structured required facts. Evaluation is initially manual and checkpoint-based, with each deliverable scored independently so incomplete runs can receive partial credit. A deterministic evaluator can be added later once the manual checklist stabilizes.

## User Stories

1. As a benchmark author, I want a tiny local-file benchmark, so that I can compare agent frameworks without setting up containers or services.
2. As a benchmark author, I want the same tasks to run across `pydantic-ai-bdi`, OpenClaw, and Hermes Agent, so that framework differences are easier to observe.
3. As a benchmark author, I want each task to use only local plain-text or CSV files, so that setup stays lightweight.
4. As a benchmark author, I want each task to require two or three named deliverables, so that intermediate work is visible and scorable.
5. As a benchmark author, I want deliverables to use exact filenames with semi-structured required facts, so that scoring remains objective without forcing a narrow JSON-only result.
6. As a benchmark author, I want each deliverable to be scored independently, so that incomplete runs can receive useful partial credit.
7. As a benchmark author, I want agents to ground deliverables in local evidence files, so that I can see whether their work is based on the provided fixtures.
8. As a benchmark author, I want agents to make calculations and filtering decisions visible, so that partial reasoning can be evaluated before the final decision.
9. As a benchmark author, I want optional scratch work to be allowed but ignored for scoring unless it contradicts required deliverables, so that agents can work more naturally.
10. As a benchmark author, I want task instructions to avoid mentioning evaluation, so that agents behave naturally.
11. As a benchmark author, I want hidden checkpoints, so that agents cannot optimize directly for the rubric.
12. As a benchmark author, I want evaluation to happen after the run, so that the benchmark mirrors independent assessment.
13. As a benchmark author, I want manual checkpoint scoring for v0, so that I can start comparing frameworks immediately.
14. As a benchmark author, I want checkpoint-style evaluation, so that partial success can be recorded instead of only pass or fail.
15. As a benchmark author, I want a fresh session for every task, so that previous context does not bias results.
16. As a benchmark author, I want the same model used across frameworks, so that the comparison focuses more on framework behavior.
17. As a benchmark author, I want memory and learned skills disabled or avoided, so that frameworks are compared in a strict fair-run mode.
18. As a benchmark author, I want a fixed timeout per task, so that runs are comparable and bounded.
19. As a benchmark author, I want each task to include conflicting or stale information, so that agents must reason about source reliability.
20. As a benchmark author, I want one task focused on vendor selection, so that agents must compare options against requirements and budget.
21. As a benchmark author, I want the vendor task to require use of an updated vendor note, so that stale data handling is tested.
22. As a benchmark author, I want the vendor task to require arithmetic, so that cost computation is evaluated.
23. As a benchmark author, I want the vendor task to require rejection reasons, so that constraint reasoning is visible.
24. As a benchmark author, I want one task focused on reimbursement auditing, so that policy interpretation can be tested.
25. As a benchmark author, I want the reimbursement task to include old and current policy sources, so that conflict resolution is tested.
26. As a benchmark author, I want the reimbursement task to include exclusions, caps, and missing receipts, so that item-level reasoning is tested.
27. As a benchmark author, I want the reimbursement task to require a total, so that arithmetic and policy application can be compared.
28. As a benchmark author, I want one task focused on incident staffing, so that eligibility and scheduling reasoning can be tested.
29. As a benchmark author, I want the staffing task to include access updates, so that agents must use the newest information.
30. As a benchmark author, I want the staffing task to require primary and backup selections, so that agents must satisfy multiple roles.
31. As a benchmark author, I want the staffing task to include ineligible candidates, so that filtering behavior is visible.
32. As a benchmark runner, I want task folders to be independent, so that I can run one task without setting up the whole suite.
33. As a benchmark runner, I want outputs to be copied into framework-specific run records, so that results from different frameworks do not overwrite each other.
34. As a benchmark runner, I want an explicit run protocol, so that I can repeat the comparison consistently.
35. As a benchmark runner, I want clear manual checkpoints, so that scoring is not improvised each time.
36. As a benchmark runner, I want the ability to note operational friction, so that framework setup and prompting burden are captured.
37. As a benchmark runner, I want artifact validity to be scored distinctly from wrong reasoning, so that output-format failures are visible.
38. As a benchmark runner, I want contradiction handling to be scored explicitly, so that stale-source mistakes are not hidden inside a generic accuracy score.
39. As a benchmark runner, I want evidence discipline to be scored explicitly, so that grounded answers can be distinguished from plausible guesses.
40. As a benchmark runner, I want concise outputs, so that frameworks are not rewarded for producing unnecessary files or narrative.
41. As a framework evaluator, I want to compare completion rate, so that I know whether each framework can finish simple local tasks reliably.
42. As a framework evaluator, I want to compare required deliverable validity, so that artifact-production reliability is measured.
43. As a framework evaluator, I want to compare answer accuracy, so that correctness remains the core signal.
44. As a framework evaluator, I want to compare use of evidence, so that file-grounded behavior is measured.
45. As a framework evaluator, I want to compare handling of stale data, so that source-priority reasoning is measured.
46. As a framework evaluator, I want to compare setup friction, so that practical usability is part of the result.
47. As a future maintainer, I want the manual checklist to be convertible into a deterministic evaluator, so that the benchmark can mature without redesigning tasks.
48. As a future maintainer, I want task fixtures to be small and readable, so that expected answers are easy to audit.
49. As a future maintainer, I want expected answers to remain hidden from agents, so that benchmark integrity is preserved.
50. As a future maintainer, I want the suite to allow additional tasks later, so that SBench can grow beyond the initial smoke test.

## Implementation Decisions

- Build SBench as a local-file fixture suite rather than a repository, service environment, or containerized benchmark.
- Use three independent operations-style tasks for the first suite instead of one large combined task.
- Keep each task intentionally small, with roughly four to five visible files per task.
- Require each task to include one stale or conflicting source that must be resolved correctly.
- Require agents to produce multiple named deliverables for each task.
- Use per-task deliverable contracts with exact filenames and semi-structured required facts.
- Keep final decision artifacts separate from intermediate source-resolution, screening, or calculation artifacts.
- Allow optional scratch files, but score the required deliverables.
- Hide expected values and scoring checkpoints from the agent during execution.
- Use manual checkpoint evaluation for the initial version.
- Treat a deterministic evaluator as a future enhancement after manual scoring stabilizes.
- Use a strict fair-run protocol for the initial comparison: same model, fresh sessions, no retained memory, no learned skills, and fixed timeout.
- Track operational friction as part of comparison, because setup and prompting burden are important framework-level differences.
- Treat framework-specific natural-mode features, such as persistent memory or learned skills, as out of scope for the first comparison.

The main conceptual modules are:

- Fixture Pack: owns the task files and deliberately placed stale or conflicting information.
- Task Instruction: presents only the user-facing task request and output requirement.
- Deliverable Contract: defines exact filenames and required facts for each task artifact.
- Run Protocol: defines model/session/time-limit controls for fair framework comparison.
- Manual Evaluation Checklist: defines hidden checkpoints used after completion.
- Results Archive: stores framework outputs and evaluator notes for comparison.

The deepest module should eventually be the evaluation contract. It should expose a simple checklist or scoring interface while hiding the details of exact expected values and task-specific validation logic. This keeps future deterministic evaluation possible without changing how agents are run.

## Testing Decisions

Good tests for SBench should verify externally observable benchmark behavior rather than implementation details. Tests should answer questions such as whether a task can be completed from its visible files, whether the expected deliverables are recoverable, whether the deliverable contract is clear, and whether the manual checkpoints can distinguish partial success from failure.

The initial version uses manual evaluation rather than automated tests. During implementation, the following modules should be tested or reviewed first:

- Fixture Pack: verify each task has enough information to derive the expected answer and no accidental ambiguity.
- Deliverable Contract: verify each task's required artifacts and facts are objective enough to score.
- Manual Evaluation Checklist: verify every checkpoint maps to observable output or evidence.
- Run Protocol: verify the instructions can be given consistently across all frameworks without revealing evaluation details.

Future automated tests may include:

- Required-filename and required-section checks for generated deliverables.
- Golden-answer checks for exact expected facts.
- Evidence filename checks to ensure agents cite relevant local files.
- Arithmetic checks for vendor cost and reimbursement totals.
- Conflict-resolution checks for stale-source handling.

There is no current prior art inside the SBench directory because it starts as an empty benchmark project. The closest prior art is the user's existing work with benchmark task schemas and TheAgentCompany-style checkpoint evaluation, but SBench intentionally reduces that model to a manual, local-file smoke test.

## Out of Scope

- TAC-style service orchestration.
- Browser automation.
- Messaging gateway setup.
- Docker or containerized execution.
- Local web apps or databases.
- Source-code modification tasks.
- Multi-hour or long-horizon tasks.
- LLM-as-judge evaluation.
- Deterministic Python evaluator in the first version.
- Automatic framework runners in the first version.
- Persistent memory, learned skills, and natural long-term agent behavior in the strict comparison mode.
- Publishing benchmark results publicly.

## Further Notes

The initial SBench suite is intentionally a smoke test, not a comprehensive agent benchmark. Its purpose is to reveal early differences in framework ergonomics and reliability before investing in heavier infrastructure.

The first suite should prioritize low setup cost and repeatability over realism. If the smoke suite proves useful, SBench can later add a deterministic evaluator, weighted scoring, more tasks, natural-mode framework runs, or a lightweight runner that standardizes how each framework is invoked.

Issue tracker publication is expected by the `/to-prd` workflow, but no issue tracker configuration or triage label vocabulary is currently present in the SBench project context.
