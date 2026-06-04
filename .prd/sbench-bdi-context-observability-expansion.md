---
title: SBench BDI Context and Observability Expansion
labels:
  - needs-triage
status: draft
---

## Problem Statement

SBench currently compares agent harnesses on small local operations tasks. The current smoke suite is useful for checking whether each harness can read local files, resolve stale sources, perform simple calculations, and produce named workplace deliverables. However, the first results show that BDI has longer wait time on every current task.

That result is not enough to evaluate the main BDI hypothesis. The BDI harness is expected to be more useful when the task pressures long-running deliberation, context management, goal stability, plan repair, and execution observability. The current SBench protocol starts every run in a fresh session, disables retained memory where possible, uses short tasks, and evaluates mostly final artifacts. Those choices intentionally make the comparison simple and fair, but they also remove the conditions where explicit Beliefs, Desires, Intentions, Plans, Plan Steps, and Plan Step History should matter.

The user needs SBench to evolve beyond a smoke suite so that it can test whether BDI offers advantages that are not captured by elapsed time alone. In particular, the benchmark should reveal whether BDI can manage important context through beliefs, preserve an active goal and intention across long work, repair plans without discarding useful progress, and expose a clearer execution trace than harnesses whose goals and intentions remain implicit in model reasoning or informal to-do lists.

## Solution

Expand SBench into a multi-track benchmark while preserving the current smoke suite as the baseline. The new benchmark should keep the same local-file, framework-neutral design, but add task families that create context pressure, staged updates, recoverable plan failures, distractor goals, partial work resumption, and trace observability checks.

The expanded suite should compare harnesses on both task outcomes and deliberative behavior. Time should remain recorded, but it should no longer be the only practical signal. The benchmark should also capture completion quality, context retention, goal stability, plan repair, evidence discipline, and trace observability.

The smoke track should continue to run the existing short tasks under strict fresh-session rules. New tracks should introduce controlled pressure without requiring browser automation, external services, or hosted infrastructure. Each new track should remain solvable from local plain-text, Markdown, and CSV files, and hidden expected answers should remain outside the agent-facing task folder.

The expanded SBench should include these conceptual modules:

- Benchmark Track Model: defines separate tracks such as smoke, long context, replanning, recovery, and observability.
- Task Fixture Pack: owns local files, visible instructions, staged facts, distractors, stale sources, and expected source conflicts.
- Context Pressure Fixture: creates enough local evidence and phase history to test whether important facts survive long execution.
- Scenario Event Layer: introduces controlled updates, contradictions, or failed assumptions that require plan repair.
- Deliverable Contract: defines exact output artifacts and required facts without revealing scoring details.
- Evaluation Contract: defines hidden checkpoints for correctness, context retention, goal stability, plan repair, and trace observability.
- Run Protocol: defines when to use strict fresh-session runs and when to use context-pressure runs.
- Trace Capture: records native harness logs or state summaries in a framework-neutral way after the run.
- Result Capture Schema: stores elapsed time, completion, accuracy, trace quality, operational friction, and context-management signals.

The deepest module should be the Evaluation Contract. It should expose a small scoring interface while hiding expected answers and detailed validation logic from the agent. This lets SBench add new task families without changing how agents are prompted.

## User Stories

1. As a benchmark author, I want to preserve the current smoke suite, so that existing results remain comparable.
2. As a benchmark author, I want to add a long-context track, so that SBench can test behavior under context pressure.
3. As a benchmark author, I want to add a replanning track, so that SBench can test whether agents recover from changed assumptions.
4. As a benchmark author, I want to add a recovery track, so that SBench can test whether agents preserve useful partial work.
5. As a benchmark author, I want to add an observability track, so that SBench can test whether harness execution state is understandable after the run.
6. As a benchmark author, I want each new track to remain local-file only, so that the benchmark stays lightweight.
7. As a benchmark author, I want hidden expected answers to remain outside agent-facing folders, so that agents cannot optimize directly for the rubric.
8. As a benchmark author, I want tasks to avoid saying that they are benchmark tasks, so that harness behavior remains natural.
9. As a benchmark author, I want tasks to include enough evidence to be solved deterministically, so that scoring remains credible.
10. As a benchmark author, I want long-context tasks to place important facts early in the evidence set, so that context retention can be measured.
11. As a benchmark author, I want long-context tasks to include many irrelevant but plausible files, so that agents must select durable facts instead of copying everything.
12. As a benchmark author, I want context-pressure tasks to require final use of facts discovered in early phases, so that lost context becomes visible.
13. As a benchmark author, I want tasks to include stale source conflicts, so that source reliability remains part of the suite.
14. As a benchmark author, I want staged tasks to introduce updates after initial work, so that plan repair can be evaluated.
15. As a benchmark author, I want staged tasks to keep the top-level objective stable, so that goal commitment can be evaluated.
16. As a benchmark author, I want staged tasks to change the best plan without changing the goal, so that BDI plan repair can be compared to full replanning.
17. As a benchmark author, I want distractor tasks to include plausible secondary requests, so that goal drift can be measured.
18. As a benchmark author, I want distractor tasks to require explicit scope control, so that agents are not rewarded for doing extra unrelated work.
19. As a benchmark author, I want recovery tasks to start with partially correct artifacts, so that agents must audit before rewriting.
20. As a benchmark author, I want recovery tasks to include both correct and incorrect prior work, so that useful progress preservation can be measured.
21. As a benchmark author, I want recovery tasks to score whether correct prior work was preserved, so that agents are not rewarded for unnecessary rework.
22. As a benchmark author, I want recovery tasks to score whether incorrect prior work was corrected, so that agents still need to improve the final outcome.
23. As a benchmark author, I want observability tasks to capture native harness traces, so that explicit BDI state can be compared against implicit reasoning traces.
24. As a benchmark author, I want trace scoring to identify current goal, current intention, active plan, current step, and reason for reconsideration, so that BDI interpretability is directly measured.
25. As a benchmark author, I want trace scoring to avoid requiring private model reasoning, so that the comparison remains fair and reproducible.
26. As a benchmark author, I want trace scoring to work for harnesses with only to-do tools or logs, so that non-BDI agents can still receive partial credit.
27. As a benchmark runner, I want strict fresh-session runs to remain available, so that basic harness competence can still be compared.
28. As a benchmark runner, I want context-pressure runs to be separate from strict smoke runs, so that the two results are not conflated.
29. As a benchmark runner, I want result capture to include elapsed time, so that BDI overhead remains visible.
30. As a benchmark runner, I want result capture to include number of model calls where available, so that overhead can be compared more precisely.
31. As a benchmark runner, I want result capture to include token usage where available, so that context efficiency can be evaluated.
32. As a benchmark runner, I want result capture to include checkpoint correctness, so that quality remains the primary outcome.
33. As a benchmark runner, I want result capture to include context retention score, so that important lost facts are visible.
34. As a benchmark runner, I want result capture to include goal stability score, so that drift from the original task is visible.
35. As a benchmark runner, I want result capture to include plan repair score, so that recovery from changed assumptions is visible.
36. As a benchmark runner, I want result capture to include trace observability score, so that interpretability is evaluated directly.
37. As a benchmark runner, I want operational friction to remain recorded, so that framework usability remains part of the comparison.
38. As a BDI researcher, I want the benchmark to test explicit beliefs, so that BDI context management can be evaluated.
39. As a BDI researcher, I want the benchmark to test explicit desires and intentions, so that commitment semantics can be evaluated.
40. As a BDI researcher, I want the benchmark to test plan repair separately from goal abandonment, so that BDI lifecycle behavior can be evaluated.
41. As a BDI researcher, I want the benchmark to test Plan Step History usefulness, so that completed progress preservation can be evaluated.
42. As a BDI researcher, I want the benchmark to distinguish slower execution from worse execution, so that BDI overhead is interpreted correctly.
43. As a BDI researcher, I want the benchmark to report quality per elapsed minute, so that speed and correctness can be compared together.
44. As a BDI researcher, I want the benchmark to report quality per model call where available, so that deliberative overhead can be studied.
45. As a harness evaluator, I want non-BDI harnesses to be scored on the same observable outputs, so that the comparison remains fair.
46. As a harness evaluator, I want non-BDI harnesses to receive trace credit when their logs expose task state, so that BDI is not given automatic credit by definition.
47. As a harness evaluator, I want final artifact scoring to remain independent of trace scoring, so that interpretability does not hide incorrect work.
48. As a future maintainer, I want new task families to follow the same fixture and evaluation structure, so that the suite can grow without redesign.
49. As a future maintainer, I want manual scoring to be convertible into deterministic checks, so that automation can be added later.
50. As a future maintainer, I want the expanded benchmark to remain small enough to run manually at first, so that implementation does not block experimentation.
51. As a future maintainer, I want track definitions to be explicit, so that results from different pressure modes are not compared accidentally.
52. As a future maintainer, I want expected answers to remain auditable by humans, so that benchmark credibility is maintained.

## Implementation Decisions

- Keep the existing smoke suite unchanged as the baseline track.
- Add benchmark tracks instead of replacing the current task model.
- Use local plain-text, Markdown, and CSV fixtures for all new tasks.
- Keep browser automation, hosted services, external web access, and containerized infrastructure out of the expansion.
- Continue requiring named deliverables under an agent-created answer folder.
- Continue allowing scratch files while scoring only required deliverables and relevant trace records.
- Introduce long-context tasks that are larger than the current smoke tasks and require facts from early evidence to be used in final deliverables.
- Introduce staged replanning tasks where new visible evidence changes the correct plan but not the top-level objective.
- Introduce recovery tasks where existing partial deliverables must be reviewed, preserved where correct, and corrected where wrong.
- Introduce distractor-goal tasks where agents must avoid doing plausible but out-of-scope work.
- Introduce observability scoring that uses native harness logs or state summaries produced during normal operation.
- Treat trace observability as an independent score, not as a substitute for answer correctness.
- Score BDI trace quality using observable state such as active desire, active intention, active plan, current step, plan history, belief updates, and reconsideration reason.
- Score non-BDI trace quality using comparable observable state such as to-do entries, task plans, tool traces, summaries, or logs.
- Avoid requiring access to private model chain-of-thought for any harness.
- Add a context retention checkpoint for facts discovered early and required late.
- Add a goal stability checkpoint for whether the original task objective remains controlling after distractors or updates.
- Add a plan repair checkpoint for whether the agent updates strategy without discarding correct completed work.
- Add a progress preservation checkpoint for whether correct partial artifacts survive recovery tasks.
- Add run protocol variants for strict smoke comparison and context-pressure comparison.
- Keep strict smoke runs fresh-session and memory-disabled where possible.
- Permit context-pressure runs to intentionally create longer histories or larger file sets, while still documenting exactly what was exposed.
- Record elapsed time for every run, but interpret it alongside correctness, context retention, and observability scores.
- Record model call count and token usage when the harness exposes those values.
- Record setup friction and output friction for every harness.
- Prefer manual checkpoint evaluation first, with deterministic evaluation deferred until scoring stabilizes.
- Keep expected answers and scoring checkpoints hidden from agent-facing task folders.
- Ensure each task can be solved by a careful human from visible files alone.

## Testing Decisions

Good tests for this expansion should verify externally observable benchmark behavior rather than internal implementation details. Tests should confirm that the task folders are solvable, that hidden expected answers are not exposed, that deliverable contracts are clear, and that scoring checkpoints distinguish the intended behaviors.

- Test that each new task has a visible instruction, visible evidence files, and a deliverable contract.
- Test that each new task has hidden expected answers outside the agent-facing fixture.
- Test that every required deliverable has objective required facts.
- Test that long-context tasks require at least one early-discovered fact in a final deliverable.
- Test that replanning tasks include a visible update that changes the correct plan without changing the top-level goal.
- Test that recovery tasks include partial work with both correct and incorrect content.
- Test that distractor tasks include out-of-scope requests that should not appear as completed core work.
- Test that observability scoring can be applied without private model reasoning.
- Test that BDI and non-BDI harnesses can both receive partial observability credit from native traces.
- Test that result records can capture elapsed time, completion, correctness, context retention, goal stability, plan repair, trace observability, and operational friction.
- Test that strict smoke results and context-pressure results are labeled as different tracks.
- Test that manual scoring checkpoints can be converted into deterministic checks later.

Prior art exists in the current SBench smoke suite, manual checklist, expected-answer notes, strict fair-run protocol, result capture template, and deterministic evaluator spike notes. The expansion should reuse those conventions before introducing new ones.

## Out of Scope

- Proving that BDI is always faster than other harnesses.
- Optimizing BDI runtime or changing BDI implementation code.
- Replacing the current smoke suite.
- Publishing the PRD or issues to GitHub.
- Building a full deterministic evaluator in the first expansion step.
- Adding browser automation, workplace apps, hosted services, or containers.
- Using external web access as part of task solving.
- Requiring private chain-of-thought or hidden model reasoning from any harness.
- Giving BDI automatic credit for being BDI without observable evidence.
- Changing the existing completed result archive.

## Further Notes

The current SBench results are still useful. They show that BDI has measurable overhead on short tasks. The expanded benchmark should not hide that result. Instead, it should add task conditions where BDI's architectural tradeoff can be evaluated fairly.

The safest research claim is not that BDI is faster. The safer claim is that BDI may provide better governance for long-running agent tasks: explicit context as beliefs, explicit goal commitment as intention, explicit strategy as plan, explicit progress as plan-step history, and explicit reconsideration when assumptions fail.

The first useful implementation slice should be one long-context task and one observability scoring addition. That slice would directly test the strongest BDI hypothesis while keeping the benchmark small enough to run manually.
