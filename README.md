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

Context-pressure tracks, including `long_context` and future replanning, recovery, or observability runs, should be labeled separately in protocols and result records. Do not compare smoke-track results with context-pressure results as if they used the same pressure mode.

## Track Registry

| Task ID | Track | Task folder |
| --- | --- | --- |
| `vendor_selection` | `smoke` | `tasks/vendor_selection` |
| `travel_reimbursement_audit` | `smoke` | `tasks/travel_reimbursement_audit` |
| `incident_staffing_plan` | `smoke` | `tasks/incident_staffing_plan` |
| `clinic_rollout_plan` | `long_context` | `tasks/clinic_rollout_plan` |

For strict smoke comparison runs, follow `protocol/strict_fair_run_protocol.md` and record each run with `templates/result_capture_template.md`.

## Benchmark Orchestrator

Inspect the current task and harness matrix without running agents:

```sh
python -m sbench --list
```

Preview a planned benchmark matrix without invoking any harness:

```sh
python -m sbench --dry-run --model gpt-5.2 --track smoke --harness codex,opencode --task vendor_selection
```
