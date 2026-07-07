# SBench

SBench is a local-file smoke suite for comparing agent frameworks on small operations tasks. Each task is self-contained and asks the agent to produce multiple semi-structured workplace deliverables under an `answer/` folder from local evidence only, so partial progress can be scored independently.

## Layout

- `tasks/`: agent-facing task fixture folders. Expose only one task folder to an agent run.
- `evaluation/`: hidden expected answers, manual checklist, and future evaluator notes. Do not expose these files to agents.
- `protocol/`: fair-run instructions for comparing frameworks consistently.
- `templates/`: reusable result capture documents.
- `issues/`: local implementation issue specs.

## Benchmark Tracks

SBench currently has these tracks:

- `smoke`: the baseline local operations smoke track. It uses the existing short tasks under strict fresh-session rules.
- `long_context`: a local operations track with larger evidence sets, distractors, early facts that must be used late, and context-retention scoring.
- `replanning`: a staged local operations track where a visible update changes the best plan while the top-level objective stays stable.
- `recovery`: a local operations track that starts with partially correct prior artifacts and scores preservation plus correction.
- `distractor_goal`: a local operations track with a stable core objective and plausible out-of-scope secondary requests.

Context-pressure tracks, including `long_context` and future replanning, recovery, or observability runs, should be labeled separately in protocols and result records. Do not compare smoke-track results with context-pressure results as if they used the same pressure mode.

Trace observability can be scored after any run when native harness logs, BDI state summaries, to-do lists, tool traces, or comparable records are available. Trace observability is recorded separately from final answer correctness.

The orchestrator derives each task's track from this registry. A run that selects all tasks can include multiple tracks, and each per-task result records its own track.

## Track Registry

| Task ID | Track | Task folder |
| --- | --- | --- |
| `vendor_selection` | `smoke` | `tasks/vendor_selection` |
| `travel_reimbursement_audit` | `smoke` | `tasks/travel_reimbursement_audit` |
| `incident_staffing_plan` | `smoke` | `tasks/incident_staffing_plan` |
| `clinic_rollout_plan` | `long_context` | `tasks/clinic_rollout_plan` |
| `community_workshop_replan` | `replanning` | `tasks/community_workshop_replan` |
| `grant_closeout_recovery` | `recovery` | `tasks/grant_closeout_recovery` |
| `shelter_restock_scope` | `distractor_goal` | `tasks/shelter_restock_scope` |

For strict smoke comparison runs, follow `protocol/strict_fair_run_protocol.md` and record each run with `templates/result_capture_template.md`.

## Benchmark Orchestrator

Install project dependencies with uv:

```sh
uv sync
```

Run the test suite:

```sh
uv run test
```

Inspect the current task and harness matrix without running agents:

```sh
uv run sbench --list
```

Preview a planned benchmark matrix without invoking any harness:

```sh
uv run sbench --dry-run --model gpt-5.2 --harness codex,opencode --task vendor_selection
```

Preview the Textual progress UI with simulated task updates only:

```sh
uv run sbench --progress-preview
```

Run the benchmark through uv so it uses the synced project environment:

```sh
uv run sbench --run --model openai/gpt-5.4
```

Interactive `--run` executions show a Textual progress UI when stdout is a terminal. Textual is managed by uv through `pyproject.toml` and `uv.lock`.
