---
title: SBench Cross-Harness SQLite Results Store
labels:
  - needs-triage
status: draft
---

## Problem Statement

SBench currently records benchmark executions as local run folders, per-entry metadata files, archived answer folders, stdout logs, stderr logs, and harness-specific trace formats. That structure is useful for human inspection and debugging, but it is awkward for machine-learning workflows that need a normalized table of comparable observations.

The user wants to run association-rule mining, including Apriori, over benchmark execution data. Apriori needs repeated transactions with consistent items. Today, cross-harness facts such as task, track, status, elapsed-time bucket, timeout state, deliverable completion, archive size, token usage, and LLM call count must be reconstructed from scattered metadata and logs. Token data is especially fragmented because BDI, Codex, and OpenCode expose different JSON shapes and different token component names.

The user needs a local SQLite database that imports SBench orchestrator entries into a shared cross-harness result schema. BDI, Codex, and OpenCode should each produce rows with the same core columns, even when individual token subfields are only available from some harnesses. Missing values should represent unavailable data rather than false or zero values.

## Solution

Create a local SQLite-backed results store for SBench benchmark executions. The results store should scan orchestrator run entries, normalize common execution metadata, parse harness stdout logs for token and LLM-call usage, compute derived feature buckets, and store Apriori-ready transaction items.

Each execution should become one normalized row representing one task, one harness, one model, one archive run, and one orchestrator run. Common fields should come from orchestrator metadata. Deliverable completion should be derived from the task deliverable contract and archived answer files. Token usage should be derived by harness-specific parsers behind a common token-usage interface.

The database should preserve raw numeric values for analysis while generating categorical item rows for Apriori. For example, elapsed time and token totals should be stored as raw values on the execution row and as bucketed items in the transaction item table. The importer should be rerunnable and idempotent so local experiments can refresh the database after new benchmark runs.

The feature should treat final answer correctness as out of scope. A successful orchestrator status means the harness process completed and produced archivable artifacts; it does not mean the answer is correct. Future evaluator results can be added as a separate layer.

## User Stories

1. As a benchmark runner, I want to import SBench orchestrator entries into SQLite, so that benchmark data is queryable without manually opening run folders.
2. As a benchmark runner, I want one execution row per harness-task archive run, so that every benchmark attempt is represented consistently.
3. As a benchmark runner, I want BDI, Codex, and OpenCode executions to share the same database columns, so that cross-harness comparisons are straightforward.
4. As a benchmark runner, I want task ID stored for every execution, so that association rules can include task identity.
5. As a benchmark runner, I want benchmark track stored for every execution, so that smoke, long-context, replanning, recovery, and distractor-goal runs are not conflated.
6. As a benchmark runner, I want harness name stored for every execution, so that rules can include or exclude harness-specific patterns.
7. As a benchmark runner, I want model name stored for every execution, so that model-level differences can be analyzed.
8. As a benchmark runner, I want orchestrator status stored for every execution, so that successful, failed, incomplete, and timed-out runs can be mined separately.
9. As a benchmark runner, I want timeout state stored as a normalized boolean, so that timeout behavior can be used as an Apriori item.
10. As a benchmark runner, I want elapsed seconds stored as a raw value, so that later reports can compute accurate timing summaries.
11. As a benchmark runner, I want elapsed-time buckets generated automatically, so that Apriori can use timing categories rather than continuous values.
12. As a benchmark runner, I want archived file count stored for every execution, so that output volume can be compared across harnesses.
13. As a benchmark runner, I want required deliverables detected from the task contract, so that deliverable completion can be derived consistently.
14. As a benchmark runner, I want a `deliverables_present` feature, so that Apriori can relate completed output contracts to runtime and token patterns.
15. As a benchmark runner, I want missing deliverable information represented explicitly, so that incomplete outputs do not look equivalent to complete outputs.
16. As a benchmark runner, I want token usage stored when a harness exposes it, so that model cost pressure can be analyzed alongside elapsed time.
17. As a benchmark runner, I want total token count stored as a normalized field, so that all harnesses have one comparable token metric when available.
18. As a benchmark runner, I want input token count stored separately, so that context-loading pressure can be analyzed.
19. As a benchmark runner, I want output token count stored separately, so that answer verbosity and reasoning overhead can be analyzed.
20. As a benchmark runner, I want reasoning token count stored when available, so that hidden reasoning budget can be analyzed without relying on private chain-of-thought.
21. As a benchmark runner, I want cached input token count stored when available, so that cache effects do not disappear from the dataset.
22. As a benchmark runner, I want cache read token count stored when available, so that harnesses exposing cache reads can be compared more precisely.
23. As a benchmark runner, I want cache write token count stored when available, so that future cache-writing behavior can be tracked.
24. As a benchmark runner, I want audio token fields stored as nullable columns, so that the schema can preserve BDI-exposed usage fields without pretending they apply to all harnesses.
25. As a benchmark runner, I want LLM call count stored for every execution when available, so that deliberative overhead can be compared across harnesses.
26. As a benchmark runner, I want tool call count stored when available, so that tool-heavy executions can be identified.
27. As a benchmark runner, I want token usage availability stored explicitly, so that missing token data does not become a misleading zero.
28. As a benchmark runner, I want the source of token usage stored, so that I can audit which parser populated the usage fields.
29. As a benchmark runner, I want BDI token usage parsed from its final aggregate run event, so that current BDI logs contribute complete usage metrics.
30. As a benchmark runner, I want BDI per-agent call events usable as a fallback, so that partial BDI logs can still produce token totals when no final aggregate exists.
31. As a benchmark runner, I want older BDI logs without token usage to import successfully with null token fields, so that historical results remain usable.
32. As a benchmark runner, I want Codex token usage parsed from turn completion events, so that cached input and reasoning token counts are preserved.
33. As a benchmark runner, I want OpenCode token usage parsed from step completion events, so that per-step token data becomes a run-level aggregate.
34. As a benchmark runner, I want OpenCode logs parsed tolerantly, so that non-JSON noise before JSON events does not break imports.
35. As a benchmark runner, I want raw stdout and stderr paths retained in the database, so that suspicious rows can be traced back to source artifacts.
36. As a benchmark runner, I want archive path retained in the database, so that produced deliverables can be inspected after querying.
37. As a benchmark runner, I want imports to be idempotent, so that rerunning the importer refreshes rows rather than duplicating executions.
38. As a benchmark runner, I want import warnings recorded separately, so that parser gaps are visible without failing the entire import.
39. As a benchmark runner, I want transaction items generated from normalized rows, so that Apriori can run without custom log parsing.
40. As a benchmark runner, I want common Apriori items generated for task, track, harness, status, timeout, elapsed bucket, deliverable completion, token buckets, and LLM-call buckets, so that rules use consistent vocabulary.
41. As a benchmark runner, I want raw numeric token values and bucketed token items stored separately, so that both statistical analysis and Apriori mining are supported.
42. As a benchmark runner, I want unavailable token subfields left null, so that missing data is not confused with measured zero usage.
43. As a benchmark runner, I want generated items to avoid embedding raw high-cardinality numbers, so that Apriori outputs stay interpretable.
44. As a benchmark runner, I want the database to be local-only, so that benchmark artifacts and hidden evaluation data are not published accidentally.
45. As a benchmark maintainer, I want the importer to use the existing task registry and orchestrator metadata vocabulary, so that the results store aligns with the rest of SBench.
46. As a benchmark maintainer, I want the token parsers isolated behind a deep module, so that harness-specific log formats can change without rewriting the database layer.
47. As a benchmark maintainer, I want the deliverable completion detector isolated behind a deep module, so that output-contract parsing can be tested independently.
48. As a benchmark maintainer, I want the SQLite store isolated behind a small interface, so that schema creation and upsert behavior can be tested independently.
49. As a benchmark maintainer, I want the Apriori item builder isolated behind a small interface, so that bucket rules can evolve without touching run parsing.
50. As a benchmark maintainer, I want parser behavior covered with compact fixture logs, so that changes to BDI, Codex, or OpenCode output formats are caught cheaply.
51. As a BDI researcher, I want token totals and LLM-call counts from BDI runs, so that BDI overhead can be compared to non-BDI harnesses.
52. As a BDI researcher, I want BDI-specific state to remain outside the core cross-harness schema, so that common rows do not privilege BDI-specific concepts.
53. As a harness evaluator, I want cross-harness token fields to be normalized without losing harness-specific subfields, so that comparisons remain fair and auditable.
54. As a future evaluator author, I want correctness data left as a later extension, so that this database can first stabilize around observable run facts.
55. As a future maintainer, I want schema migrations to be considered from the start, so that new usage fields can be added without rebuilding the database manually.

## Implementation Decisions

- Build a cross-harness results importer that scans orchestrator entries rather than harness-specific raw output directories.
- Treat one orchestrator entry as one execution transaction for downstream Apriori mining.
- Keep the core execution schema harness-neutral and reserve harness-specific interpretation for parser internals.
- Use orchestrator metadata as the authoritative source for task, track, harness, model, status, timeout, elapsed time, archive path, and log paths.
- Derive `elapsed_bucket` from elapsed seconds using stable bucket thresholds suitable for Apriori.
- Derive `archived_file_count` from the archived paths recorded by the orchestrator.
- Derive `deliverables_present` by comparing archived answer filenames to required deliverable filenames from the task deliverable contract.
- Store `deliverables_present` as nullable when required deliverables cannot be determined.
- Store token usage as raw numeric columns in the execution row.
- Store token usage availability as an explicit boolean feature.
- Store token usage source as a short parser identifier, such as BDI aggregate, BDI event fallback, Codex turn usage, OpenCode step aggregate, or unavailable.
- Normalize token fields across harnesses as total, input, output, reasoning, cached input, cache read, cache write, input audio, output audio, cache audio read, LLM calls, and tool calls.
- Use null for token fields that a harness does not expose.
- Do not convert unavailable token fields into zero.
- For BDI, prefer the final aggregate run event for token usage and LLM-call count.
- For BDI, use per-agent completed events only as a fallback when the final aggregate is missing.
- For Codex, parse turn completion usage and preserve cached input and reasoning token counts.
- For OpenCode, parse step completion token objects and aggregate them to execution-level token totals.
- Use tolerant JSON-line parsing for harness stdout logs because some logs contain non-JSON lines before structured events.
- Keep import warnings separate from execution rows so parser limitations can be reviewed without dropping execution data.
- Build a SQLite store module that owns schema creation, schema versioning, and idempotent upserts.
- Build a token usage extractor module with one parser adapter per supported harness.
- Build a deliverable contract reader module that extracts required answer filenames from visible task contracts.
- Build an execution normalizer module that combines metadata, deliverable information, and token usage into one normalized record.
- Build an Apriori item builder module that turns normalized execution rows into stable categorical items.
- Keep raw numeric values on execution rows and bucketed values in transaction items.
- Generate transaction items for task, track, harness, status, timeout, elapsed bucket, deliverable completion, archived file count bucket, token availability, token total bucket, input token bucket, output token bucket, reasoning token bucket, cache token availability, LLM-call bucket, and tool-call bucket where available.
- Keep the database local and do not publish records to any external service.
- Do not read hidden expected-answer files as part of this importer.
- Do not infer answer correctness from orchestrator success.
- Design the importer so it can be run repeatedly after new benchmark runs.

## Testing Decisions

- Good tests should verify externally observable behavior: given representative metadata, task contracts, and stdout logs, the importer should produce expected database rows and transaction items.
- Tests should avoid asserting private helper behavior when a public importer or parser contract can be tested instead.
- The SQLite store should be tested with temporary databases to verify schema creation, idempotent upsert behavior, and transaction item replacement.
- The execution normalizer should be tested with representative orchestrator metadata for successful, failed, timed-out, and incomplete runs.
- The elapsed bucket builder should be tested at bucket boundaries.
- The deliverable contract reader should be tested against current SBench task contracts and should verify that required answer filenames are discovered without hidden evaluation files.
- The deliverable completion detector should be tested with all-present, partially-present, missing, and unknown-contract cases.
- The BDI token parser should be tested with the current aggregate run event format.
- The BDI token parser should be tested with per-agent completed events as fallback input.
- The BDI token parser should be tested with older logs that have no token events, producing unavailable token usage rather than zero usage.
- The Codex token parser should be tested with turn completion usage that includes cached input and reasoning token counts.
- The OpenCode token parser should be tested with mixed non-JSON and JSON stdout lines.
- The OpenCode token parser should be tested with multiple step completion events and should aggregate token fields correctly.
- The token parser suite should verify that unavailable subfields are null while measured zero values remain zero.
- The Apriori item builder should be tested with normalized execution records rather than raw logs.
- The Apriori item builder should verify that raw continuous numbers are bucketed and not emitted directly as high-cardinality items.
- Prior art for these tests exists in the orchestrator tests, which already exercise run metadata, summary generation, archive behavior, timeouts, incomplete answers, and JSON event capture without invoking real harnesses.

## Out of Scope

- Scoring final answer correctness is out of scope.
- Deterministic evaluation against hidden expected answers is out of scope.
- LLM-based judging is out of scope.
- Publishing the PRD, database, imported results, or issues to GitHub is out of scope.
- Changing the benchmark tasks or deliverable contracts is out of scope.
- Changing harness command invocation behavior is out of scope.
- Changing the existing answer archive convention is out of scope.
- Reprocessing raw BDI output directories that do not correspond to orchestrator entries is out of scope for the first implementation.
- Storing private model reasoning or requiring private chain-of-thought is out of scope.
- Running Apriori itself is out of scope for the first storage slice, except for generating transaction items suitable for Apriori.
- Building a dashboard or UI is out of scope.
- Supporting harnesses beyond BDI, Codex, and OpenCode is out of scope for the initial implementation.

## Further Notes

The highest-risk part of this feature is token normalization. BDI, Codex, and OpenCode expose useful token data, but they do not expose exactly the same fields. The database should preserve all observed token components while keeping cross-harness columns stable. Missing data should remain null and should also be reflected by explicit availability items.

The second major risk is learning harness-format artifacts instead of benchmark behavior. Apriori item generation should distinguish common cross-harness features from parser availability features. Harness-specific fields should not be smuggled into the common schema as if they apply to every harness.

This PRD intentionally focuses on observable run facts: task, track, status, elapsed time, timeout, deliverable presence, archive count, token usage, and LLM-call count. Correctness, evidence discipline, source-conflict handling, and trace observability can be added later as separate evaluator-backed data layers.
