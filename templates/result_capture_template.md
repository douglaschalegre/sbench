# SBench Result Capture Template

Use one copy of this template for one framework-task run. The fields are framework-neutral and can be used for `pydantic-ai-bdi`, OpenClaw, Hermes Agent, or another framework.

## Run Metadata

| Field | Value |
| --- | --- |
| Run ID |  |
| Date |  |
| Benchmark track | derived from task registry |
| Framework |  |
| Framework version or commit |  |
| Model |  |
| Model settings |  |
| Task ID |  |
| Exposed task folder |  |
| Fresh session used |  |
| Memory or learned skills disabled |  |
| Timeout | 10 minutes |
| Start time |  |
| End time |  |
| Elapsed time |  |

## Completion

| Check | Value | Notes |
| --- | --- | --- |
| Finished within timeout |  |  |
| All required deliverables produced |  |  |
| Some required deliverables produced |  |  |
| Extra scratch files produced |  |  |
| Run stopped early or failed |  |  |

## Trace Observability

Record only observable harness or agent state. Do not request or paste private chain-of-thought.

| Field | Value | Notes |
| --- | --- | --- |
| Trace source |  | Native logs, JSON events, BDI state summary, to-do list, tool trace, run summary, or none. |
| Trace available |  | yes / partial / no |
| Trace artifact path or transcript location |  |  |
| Trace limitations |  | Missing steps, summarized state only, no reconsideration events, etc. |
| Current goal observable |  |  |
| Current intention or task commitment observable |  |  |
| Active plan observable |  |  |
| Current step observable |  |  |
| Completed-step history observable |  |  |
| Reason for reconsideration observable |  |  |
| Private reasoning excluded |  | Confirm no private chain-of-thought was required. |
| Trace scored independently from artifact correctness |  |  |

## Produced Deliverables

List each required deliverable and paste or summarize its contents.

| Deliverable | Produced | Notes |
| --- | --- | --- |
|  |  |  |

## Produced Artifact Contents

```text

```

## Artifact Validity

| Check | Pass/Fail/N/A | Notes |
| --- | --- | --- |
| Required `answer/` paths are present |  |  |
| Files are readable Markdown, CSV, or text |  |  |
| Required sections, columns, or labels are present |  |  |
| Task-specific facts are present |  |  |

## Manual Scoring Notes

| Category | Pass/Fail/Partial/N/A | Notes |
| --- | --- | --- |
| Work correctness |  |  |
| Evidence discipline |  |  |
| Contradiction or stale-source handling |  |  |
| Arithmetic accuracy |  |  |
| Rejection or exclusion reasons |  |  |
| Trace observability |  | Score independently from correctness when traces exist. |
| Unsupported assumptions are limited and explicit |  |  |
| Required deliverables are independently scorable |  |  |

## Operational Friction

| Topic | Notes |
| --- | --- |
| Setup friction before run |  |
| Prompting or adapter friction |  |
| File access friction |  |
| Deliverable production friction |  |
| Timeout or cancellation friction |  |
| Other observations |  |

## Evaluator Summary

Overall status: `pass` / `partial` / `fail` / `invalid`

Notes:
