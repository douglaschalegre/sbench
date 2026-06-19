---
title: SBench KDD Apriori Progress
labels:
  - kdd
  - apriori
  - benchmark-analysis
status: draft
---

## Problem Statement

SBench is being prepared for a Knowledge Discovery in Databases (KDD) workflow over benchmark execution results. The immediate research goal is to run association-rule mining, including Apriori, over comparable benchmark executions from BDI, Codex, and OpenCode.

The repository already contains benchmark run artifacts, a SQLite results store, and Apriori-ready transaction items. This spec records the current KDD progress so the remaining work can be tracked explicitly.

## Current KDD Status

As of 2026-06-18, the project has completed the data preparation stages of KDD and is ready to begin the data mining stage.

| KDD step | Status | Current repo state |
| --- | --- | --- |
| 1. Data selection | Complete for the current dataset | Benchmark execution artifacts have been selected from `runs/` and imported into `results.sqlite`. |
| 2. Pre-processing | Complete | Raw metadata, logs, task contracts, and answer archives are normalized into one execution table. |
| 3. Transformation | Complete | Normalized execution rows are transformed into Apriori-ready transaction items in `execution_items`. |
| 4. Data mining | Scaffolded | A notebook-based execution path is being introduced, but no curated frequent itemsets or association rules have been accepted yet. |
| 5. Evaluation | Not started | No rule interpretation, support/confidence/lift review, or usefulness validation exists yet. |

## Current Dataset Snapshot

The current local `results.sqlite` database contains:

- `63` imported executions.
- `735` generated transaction items.
- `3` run batches.
- `21` BDI executions.
- `21` Codex executions.
- `21` OpenCode executions.
- Tracks represented: `smoke`, `long_context`, `replanning`, `recovery`, and `distractor_goal`.
- All currently imported executions have `status:success`.
- All currently imported executions have `deliverables_present = 1`.
- All currently imported executions have token usage available.

Verification performed during analysis:

- `uv run python -m unittest tests/test_results_importer.py tests/test_orchestrator.py`
- Result: `53` tests passed.

## KDD Execution Workflow

The repository should track KDD as a reproducible analysis execution, not just as code. A KDD execution means one complete run from the current benchmark results database to mined rules and evaluation notes.

### Proposed Folder

Use a dedicated notebook plus timestamped output folders:

```text
notebooks/
    kdd_apriori_execution.ipynb
    kdd_apriori_outputs/
        <execution-id>/
            dataset_summary.json
            frequent_itemsets.csv
            association_rules.csv
            evaluation_notes.md
```

The notebook is the exploratory phase-4 and phase-5 workspace. It should consume the existing `results.sqlite` database and should not modify benchmark run artifacts.

### Why Use a Notebook First

A notebook is appropriate for the first KDD execution because the thresholds and interpretation criteria are still research decisions.

The notebook should make it easy to:

- Inspect the selected dataset before mining.
- Tune Apriori parameters such as minimum support, confidence, lift, and maximum itemset size.
- Display frequent itemsets and rules immediately.
- Add narrative evaluation notes beside the computed results.
- Export tables once a useful configuration is found.

A CLI command such as `sbench --mine-apriori` can be added later after the notebook workflow stabilizes.

### How to Create a KDD Execution

1. Refresh the normalized results database:

```sh
uv run sbench --import-results --results-db results.sqlite
```

2. Open and run the notebook:

```text
notebooks/kdd_apriori_execution.ipynb
```

3. Set the mining parameters in the notebook:

```python
MIN_SUPPORT = 0.10
MIN_CONFIDENCE = 0.50
MIN_LIFT = 1.00
MAX_ITEMSET_SIZE = 3
DROP_UNIVERSAL_ITEMS = True
```

4. Run the notebook sections in order:

- Load `results.sqlite`.
- Group `execution_items` by `execution_id` to build transactions.
- Inspect item support and optionally drop universal items that appear in every transaction.
- Run Apriori over the transaction sets.
- Generate association rules from frequent itemsets.
- Export results and write evaluation notes.

5. Save outputs under a timestamped execution folder:

```text
notebooks/kdd_apriori_outputs/20260618T000000Z/
```

### KDD Execution Acceptance Criteria

A KDD execution is complete only when it produces:

- A dataset summary with execution count, item count, harness coverage, and track coverage.
- The Apriori parameter values used for the run.
- A frequent-itemsets output table.
- An association-rules output table.
- Evaluation notes explaining which rules are meaningful, trivial, misleading, or inconclusive.
- A statement of dataset limitations, especially if all executions share the same status or deliverable outcome.

## Phase 1: Data Selection

### What Was Selected

The selected data is the set of SBench benchmark execution artifacts produced by orchestrated benchmark runs.

Sources include:

- `runs/*/entries/*/*/*/metadata.json`
- `stdout.log`
- `stderr.log`
- archived answer file paths
- task `output_contract.md` files
- benchmark task and track metadata

Each benchmark execution is treated as one candidate transaction for downstream Apriori mining.

### Slide Summary

Use this message on slides:

> The selected data represents comparable benchmark executions across multiple agent harnesses and benchmark tracks.

Suggested visual:

```text
SBench run folders
    -> metadata + logs + archived answers
    -> selected benchmark executions
```

## Phase 2: Pre-processing

### Purpose

Pre-processing converts scattered raw benchmark artifacts into clean, comparable execution rows in SQLite.

The main difference is between raw extracted data and normalized data.

### Raw Extracted Data

Raw extracted data is copied from many different files, still in its original format.

Examples:

| Source | Raw extracted data |
| --- | --- |
| `metadata.json` | `task_id`, `harness`, `status`, `elapsed_seconds`, `archived_paths` |
| `stdout.log` | token usage events in BDI, Codex, or OpenCode-specific formats |
| `output_contract.md` | required files such as `answer/clinic_screen.md` |
| archived answer paths | produced files from each benchmark run |

Example raw metadata:

```json
{
  "task_id": "clinic_rollout_plan",
  "harness": "bdi",
  "status": "success",
  "elapsed_seconds": 144.076,
  "archived_paths": [
    "answers/.../clinic_screen.md",
    "answers/.../launch_recommendation.md",
    "answers/.../source_resolution.md"
  ]
}
```

This data is useful, but it is scattered across files, varies by harness, and is not yet ready for mining.

### Pre-processed Data

Pre-processed data is stored in `results.sqlite`, mainly in the `executions` table.

The importer:

- Combines data from metadata, logs, task contracts, and archived answers.
- Creates one row per benchmark execution.
- Standardizes data across BDI, Codex, and OpenCode.
- Parses token usage from different harness log formats.
- Preserves missing information as `null` instead of converting it to false or zero.
- Detects whether required deliverables were produced.
- Records import warnings when data is missing or malformed.

Example pre-processed row:

| Column | Value |
| --- | --- |
| `execution_id` | `20260614T221008Z:clinic_rollout_plan:bdi:r1` |
| `task_id` | `clinic_rollout_plan` |
| `track` | `long_context` |
| `harness` | `bdi` |
| `status` | `success` |
| `timed_out` | `false` |
| `elapsed_seconds` | `144.076` |
| `archived_file_count` | `3` |
| `deliverables_present` | `1` |
| `token_usage_available` | `1` |
| `token_usage_source` | `bdi:aggregate_run_event` |
| `token_total` | `22480` |

### Slide Summary

Use this message on slides:

> In phase 2, raw benchmark artifacts were extracted from multiple files and pre-processed into a clean SQLite table where each row represents one comparable benchmark execution.

Key distinction:

- Raw extracted data answers: What information exists in the original files?
- Pre-processed data answers: Can this information be compared consistently across all benchmark executions?

Suggested visual:

```text
Raw files
    -> parser/importer
    -> normalized executions table
```

## Phase 3: Transformation

### Purpose

Transformation converts normalized execution rows into Apriori-compatible transaction items.

Apriori does not work naturally on relational columns such as `task_id = clinic_rollout_plan`. It expects each record to be a transaction, meaning a set of categorical items.

The transformation therefore converts this style of table row:

| Column | Value |
| --- | --- |
| `task_id` | `clinic_rollout_plan` |
| `track` | `long_context` |
| `harness` | `bdi` |
| `status` | `success` |
| `timed_out` | `false` |
| `elapsed_seconds` | `144.076` |
| `deliverables_present` | `1` |
| `archived_file_count` | `3` |
| `token_usage_available` | `1` |
| `token_total` | `22480` |

Into this transaction item set:

```text
task:clinic_rollout_plan
track:long_context
harness:bdi
status:success
timeout:false
elapsed:2-3m
deliverables:present
archived_files:3-5
tokens:available
token_total:10k-25k
```

### Why the Transformation Is Useful

Apriori needs transaction items in a consistent vocabulary so it can discover rules such as:

```text
{track:long_context, harness:opencode} -> {elapsed:1.5-2m}
```

or:

```text
{harness:codex} -> {token_total:50k-100k}
```

The `field:value` format is important because it preserves meaning. For example, `status:success` is clearer and safer than the unqualified value `success`.

Continuous values are bucketed so Apriori does not learn high-cardinality raw numbers:

- `elapsed_seconds = 144.076` becomes `elapsed:2-3m`.
- `archived_file_count = 3` becomes `archived_files:3-5`.
- `token_total = 22480` becomes `token_total:10k-25k`.

Current elapsed-time bucket thresholds are:

- `<1m`
- `1-1.5m`
- `1.5-2m`
- `2-3m`
- `3-5m`
- `>=5m`

Current token-total bucket thresholds are:

- `1-999`
- `1k-10k`
- `10k-25k`
- `25k-50k`
- `50k-100k`
- `>=100k`

For the current dataset, universal items such as `status:success`, `timeout:false`, and `deliverables:present` are useful quality checks but do not distinguish executions. The notebook therefore drops universal items before running Apriori when `DROP_UNIVERSAL_ITEMS = True`.

Raw numeric values remain available in the `executions` table for later statistical analysis, while Apriori receives categorical items from `execution_items`.

### Slide Summary

Use this message on slides:

> The transformation step converts structured execution rows into Apriori-compatible transaction items. This lets the mining algorithm discover associations between benchmark properties such as task, harness, elapsed-time bucket, token usage, and deliverable completion.

Suggested visual:

```text
Normalized execution row
    -> bucketed/categorical features
    -> Apriori transaction
```

## Remaining KDD Work

### Phase 4: Data Mining

Data mining is scaffolded but not complete. The repository now has a notebook path for running Apriori, but no mined output has been accepted as the first KDD execution result yet.

Needed work:

- Run `notebooks/kdd_apriori_execution.ipynb` against the current `results.sqlite`.
- Tune minimum support, confidence, lift, and maximum itemset size.
- Generate frequent itemsets.
- Generate association rules.
- Persist or export mining results for review.
- Decide whether the notebook implementation is enough for the research workflow or whether it should later become a CLI command.

Potential outputs:

- `frequent_itemsets` table or artifact.
- `association_rules` table or artifact.
- CLI command such as `sbench --mine-apriori`.
- CSV, JSON, or Markdown report of discovered rules.

### Phase 5: Evaluation

Evaluation has not started yet.

Needed work:

- Review discovered rules by support, confidence, and lift.
- Remove trivial or non-actionable rules.
- Identify whether rules reflect benchmark behavior, harness artifacts, or dataset imbalance.
- Validate findings against additional benchmark runs.
- Add correctness or evaluator-backed fields later if association rules should include answer quality.

Potential outputs:

- ranked rule report
- notes explaining meaningful patterns
- rejected-rules section for obvious or misleading rules
- follow-up benchmark recommendations

## Tracking Checklist

Completed:

- [x] Select benchmark execution artifacts from SBench run folders.
- [x] Import selected artifacts into a local SQLite database.
- [x] Normalize common execution fields across BDI, Codex, and OpenCode.
- [x] Parse token usage from BDI logs.
- [x] Parse token usage from Codex logs.
- [x] Parse token usage from OpenCode logs.
- [x] Detect deliverable completion from visible task contracts and archived outputs.
- [x] Generate Apriori-ready transaction items.
- [x] Bucket continuous numeric values for Apriori.
- [x] Preserve raw numeric values for later analysis.
- [x] Verify importer and orchestrator behavior with tests.
- [x] Add a notebook scaffold for reproducible KDD executions.
- [x] Add notebook logic using `mlxtend` to load transactions, run Apriori, generate rules, and export outputs.

Remaining:

- [ ] Run the first complete KDD execution from the notebook.
- [ ] Tune and record Apriori thresholds for the first accepted execution.
- [ ] Store or export frequent itemsets and association rules.
- [ ] Evaluate rules using support, confidence, and lift.
- [ ] Interpret which rules are meaningful versus trivial.
- [ ] Validate rules on additional benchmark runs.
- [ ] Decide whether to promote the notebook workflow into a CLI command.
- [ ] Add correctness/evaluator-backed features if rules should include final answer quality.

## Notes and Caveats

- The local issue files for the SQLite/importer slices may still show draft status and unchecked acceptance criteria, but the implementation and tests indicate those slices are functionally present.
- Current imported data is useful for proving the KDD preparation pipeline, but all current executions are successful and have deliverables present. This limits the diversity of rules Apriori can discover until more varied outcomes are imported.
- Running Apriori itself was explicitly out of scope for the first SQLite storage slice. The next story should execute the notebook, export the first mined results, and evaluate the rules.
