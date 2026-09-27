# SBench auditability experiment interface and measurement procedure

This document describes the implemented SBench experiment interface as inspected on 26 September 2026, at repository revision `cb6dbb82d7d77f72ea836127c817e8324527397f`. It provides a methods description and a technical measurement specification for use in a scientific article. The participant interface is in Portuguese. English translations below explain the instrument; they do not imply that participants received an English version. The description concerns implemented behavior, without asserting that participant recruitment, data collection, or statistical analysis has already occurred.

## 1. Purpose and experimental unit

SBench presents previously recorded agent execution traces to human participants to study their auditability. Participants inspect a trace, identify evidence of the agent's activity and objective, and report confidence, perceived cognitive effort, ease of finding evidence, and whether the relevant information is explicit or requires inference across parts of the trace. The interface records both submitted responses and selected interactions during inspection.

The unit of response is one participant's assessment of one trace. A session contains three sequential trace assessments, with one trace from each of BDI, Codex, and OpenCode. The interface does not execute agents during the assessment. Agent execution duration is metadata attached to an existing trace and is distinct from the time a participant spends inspecting it. Evidence identification is a human judgment; the application does not compare selected lines with a reference answer or compute evidence correctness.

## 2. Trace preparation and assignment

### 2.1 Source material and preprocessing

A preparation script recursively discovers files named `stdout.log` under the repository's `runs` directory. For each trace, it reads the adjacent `metadata.json`, obtains the corresponding task statement from `tasks/<task>/task.md`, and copies a processed log into `experiment-frontend/public/data/logs`. A generated manifest provides the trace identifier, run identifier, task, framework, repetition, URL, agent execution duration in seconds, execution status, and model.

Preprocessing removes exact occurrences of the full task statement and its JSON-escaped representation, replacing them with `[texto literal do enunciado removido para o experimento]`, meaning that the literal task statement was removed for the experiment. It also removes ANSI color sequences matched by the script. These operations do not remove every paraphrase or partial quotation of the task statement, nor do they constitute general anonymization. The task title remains visible in the interface. The participant therefore judges the available execution record with some task context still present.

Trace identifiers combine the run, task, framework, and repetition. Manifest entries are sorted lexicographically by identifier. For each session position, the application selects the first manifest entry matching its assigned framework, configured task, and repetition. Run identifier and model are not additional selection criteria. If several runs match that combination, selection follows manifest order rather than random sampling. Reproducing the study therefore requires retaining the exact manifest and processed trace files used during collection.

### 2.2 Session configuration and framework order

The researcher enters a participant code, selects one of three Latin-square rows, selects a repetition, and specifies three distinct tasks in order. The code is converted to uppercase and must contain at least three non-whitespace characters. The default task sequence is Incident Staffing Plan, Travel Reimbursement Audit, and Vendor Selection. The default repetition is the last element of the lexicographically sorted repetition list in the manifest. These defaults are configurable before starting.

| Assigned row | Trace 1 | Trace 2 | Trace 3 |
| --- | --- | --- | --- |
| 1 | BDI | Codex | OpenCode |
| 2 | Codex | OpenCode | BDI |
| 3 | OpenCode | BDI | Codex |

Tasks follow their configured positions while frameworks rotate across positions. With the same ordered task set across all three rows, each framework occurs once at each position and once with each task across a complete square. Each participant sees three different tasks, rather than the same task under all frameworks. The cyclic square balances framework position across the three rows; it does not balance every possible directed framework transition.

The UI labels the rows as participants 1, 2, and 3. These are assignment categories, not a database-enforced limit of three people. Multiple sessions can use the same row. Assignment to rows is manual; the application does not randomize participants or enforce equal row counts. It also does not verify at configuration time that all three requested task/framework/repetition combinations exist. The study configuration must use a complete catalog.

## 3. Participant procedure and visual presentation

### 3.1 Configuration and mandatory practice

The welcome screen presents a researcher configuration panel and an interactive tutorial. At desktop widths, the panels appear side by side. The tutorial is disabled until configuration is confirmed. It uses a separate four-line example describing an agent starting an analysis, finding a requirement in `task.md`, creating a report, and completing execution.

Participants must select exactly example lines 2 and 3 and add them as an evidence reference. They then choose any value on a five-point practice scale and classify the evidence as directly stated or inferred by combining parts. Tutorial progress advances through these three actions, and the session-start button remains disabled until all are complete. Practice responses stay in the tutorial's component state and are not included in the experimental session or telemetry payload. The experimental session identifier and start timestamp are created when the participant starts after practice.

The welcome screen also offers continuation or discarding of a locally stored session. Continuing uses the stored assessment state rather than creating a new session.

### 3.2 Assessment screen

The main assessment uses a light, warm background with dark green controls and orange accents. The trace appears in a dark panel with monospaced text, while the questionnaire uses a light panel with separate bordered question cards. The configured fonts are Inter for controls and body text, Newsreader for display headings, and IBM Plex Mono for trace text, with fallback fonts.

On desktop screens, the trace is on the left and the questionnaire on the right. The layout allocates columns in a 1.35:0.65 ratio, subject to a 390-pixel minimum width for the questionnaire. Both panels have their own scrolling areas, so the questions remain accessible while the participant navigates a long trace. Below 1,024 pixels, the layout stacks the panels; the stylesheet gives the trace panel a height of 58 viewport-height units with a 480-pixel minimum. Thus the same instrument supports narrower screens, but the physical presentation and navigation burden may differ across devices.

A header shows the participant code, current trace number, session progress, a return-to-start control, and an elapsed-time display at supported widths. The timer refreshes once per second. A second strip shows the task title, repetition and model at supported widths, and the number of newline-delimited trace entries. A framework-specific color marker is also present: pale purple for BDI, pale green for Codex, and pale orange for OpenCode. The strip does not print the framework name, but the stable marker and log contents mean that the implementation does not establish complete framework blinding.

There is no separate task-statement panel. Participants inspect the processed log while answering the questionnaire, and may revise evidence and answers before completing that trace. Completion advances to the next trace; the interface provides no dedicated control for reopening a previously completed assessment.

### 3.3 Trace rendering and navigation

The viewer splits the processed text on newline characters and assigns one-based line numbers. A source line that begins with an opening brace or bracket is parsed as JSON when possible, formatted with indentation, and displayed with escaped newlines and tabs expanded. Each such record retains its original source-line number even if it occupies many visual lines. Consequently, a recorded line reference identifies a newline-delimited record in the processed file, not a typographic line on the screen. A trailing newline can also produce an empty final entry in the displayed count.

The toolbar provides a case-insensitive substring search, a matching-line counter, previous/next match controls, and a line-wrap toggle. Search operates on the source-line strings before display formatting. A line containing several occurrences contributes one match. Matching rows receive background highlighting. Navigation wraps through the match list and smoothly scrolls the selected row into the center of the trace viewport. Word wrapping is initially enabled.

Clicking a trace row toggles its selection. Shift-click extends selection over the inclusive range between an anchor line and the clicked line, retaining other selected lines. Adjacent selected lines are grouped into ranges. A persistent selection bar displays these ranges and provides controls to add them as references or clear the temporary selection. Orange indicates temporary selection; green indicates an added reference. Adding references clears the temporary selection.

The questionnaire displays retained references as removable line or range labels. Participants may add several disjoint ranges, remove references, or explicitly indicate that they found no references. Selecting the no-reference control clears all retained references and temporary selection. Adding evidence subsequently turns the no-reference flag off. The tool does not prevent overlapping or repeated references, although its unique-line metric deduplicates their coverage.

## 4. Questionnaire and response requirements

The questionnaire contains four numbered sections but five required response components: an evidence response, confidence, cognitive effort, ease, and directness. A progress indicator displays the number completed out of five. There are no default scale values or default directness choice. The trace-completion button is enabled only after all five components are present. Optional notes do not contribute to this count.

| Section and field | Original Portuguese wording | English translation and response |
| --- | --- | --- |
| 1. Esforço para auditar | Aponte para a primeira linha do log que deixa claro para você em qual atividade o agente está trabalhando e qual o objetivo dele. | Point to the first log line that makes clear to you which activity the agent is working on and what its objective is. Participants add one or more line references, or choose `Não encontrei referências`, meaning “I did not find references.” |
| 2. Confiança subjetiva, confidence | O quão confiante você ficou da sua resposta? | How confident were you in your answer? Integer scale from 1, `Nada confiante`, not at all confident, to 5, `Muito confiante`, very confident. |
| 2. Confiança subjetiva, cognitive effort | Qual a sua percepção de esforço cognitivo para encontrar o resultado? | What is your perception of the cognitive effort required to find the result? Integer scale from 1, `Muito baixa`, very low, to 5, `Muito alta`, very high. |
| 3. Localização da evidência | Qual a sua percepção do quão fácil foi encontrar essa informação? | How easy did you find it to locate this information? Integer scale from 1, `Muito difícil`, very difficult, to 5, `Muito fácil`, very easy. |
| 4. Inferência necessária | A resposta estava… | The answer was… Options are `Explícita`, explicit, and `Dispersa`, dispersed. Explanatory text asks whether the answer appears directly in the log or requires combining its parts. Values are stored as `direct` and `inferred`, respectively. |
| Optional notes | Observações sobre o trace | Observations about the trace. Free text with a prompt to record something not covered above. |

Although question 1 requests the first informative line, the interaction supports multiple lines and ranges. The collected evidence response can therefore be a set of locations, rather than a single first-line answer. A no-reference response still requires the remaining ratings and binary directness classification; the instrument offers no “not applicable” option for these fields.

The three scales are individual five-point ratings with endpoint labels. Higher values indicate more confidence, greater cognitive effort, and greater ease, respectively. Cognitive effort therefore has the opposite favorable direction from confidence and ease. The implementation does not administer a named multi-item workload instrument or compute a composite score.

## 5. Recorded data and metric definitions

### 5.1 Time base and assessment boundaries

Session and trace timestamps use the browser's wall clock, represented as ISO date-time strings. Each trace response is initialized with `startedAt` when its assessment is initialized, before the log fetch completes. Event offsets are computed in milliseconds as the browser's current `Date.now()` value minus the parsed trace start timestamp. Events also store an absolute `at` timestamp.

Timing therefore includes log loading, reading, searching, evidence selection, questionnaire completion, and interruptions. It continues across returns to the welcome screen and later resumption because the original start timestamp is retained. There is no active-time counter, idle detection, focus-based pause, or monotonic performance-clock measurement. Clock changes on the client can affect elapsed values.

Clicking the trace-completion button sets `completedAt` and, if not already present, `readingCompletedAt` to the same timestamp. The UI does not provide a separate “finished reading” action. These fields therefore do not distinguish reading time from answering time. Trace assessment duration can be calculated as completion minus start. The completion screen sums these per-trace durations; that sum excludes configuration and tutorial time and should not be confused with agent execution duration.

### 5.2 Exported derived metrics

Derived metrics are calculated in the browser when the completion payload is constructed. Missing ratings or classifications are represented as `null` in derived output, although normal UI completion requires them. The following names reproduce the exported schema.

| Identifier and exported field | Operational definition | Interpretation |
| --- | --- | --- |
| M1.1 `m1_1_firstEvidenceDeltaMs` | `deltaMs` of the first reference in the final retained reference array; `null` if none remain. | Time to addition of the first retained reference, in milliseconds. It is neither the earliest line number nor necessarily the first evidence ever added. |
| M1.1 `m1_1_noReferencesFound` | Final no-reference flag, defaulting to false. | An explicit response that no references were found. |
| M1.2 `m1_2_selectedLines` | Size of the union of inclusive line ranges in the final reference array. | Number of distinct source-line records retained as evidence. Temporary selections and removed references do not contribute. |
| M1.2 `m1_2_viewedLines` | Number of distinct line identifiers across `lines_viewed` events. | Viewport exposure count; it does not demonstrate reading or comprehension. |
| M1.2 `m1_2_selectionInteractions` | Count of `line_selection` events. | Click-based selection actions, including deselection and Shift-click. One action can select many lines. |
| M2.1 `m2_1_confidence` | Final confidence rating, 1–5. | Self-reported confidence. |
| M2.2 `m2_2_cognitiveLoad` | Final `difficulty` rating, 1–5. | Self-reported cognitive effort; the export calls it cognitive load. |
| M3.1 `m3_1_evidenceDeltasMs` | Addition-time offsets of all final retained references, in array order. | Cumulative times from trace start, not intervals between successive references. Several ranges added together share a timestamp. |
| M3.2 `m3_2_positionChanges` | Count incremented for each accepted `scroll` event and each `search_navigation` event. | A count of recorded navigation events, not spatial distance or distinct visited positions. |
| M3.2 `m3_2_eventCounts` | Frequency map over all recorded telemetry event types. | Interaction counts. A type that never occurred may be absent rather than explicitly zero. |
| M3.3 `m3_3_ease` | Final ease rating, 1–5. | Self-reported ease of locating the information. |
| M4.1 `m4_1_directness` | Final `direct` or `inferred` value. | Participant classification of how the answer was expressed. |
| M4.2 `m4_2_classificationDeltaMs` | Offset of the last `answer_changed` event tagged `M4.1`. | Time from trace start to the most recent classification-button click, rather than duration spent on the classification question. |

The response also stores `firstEvidenceAt`, which is set on the first addition and retained after references are removed or cleared. This field can differ from M1.1. The original first-addition latency can be recovered from the earliest `evidence_added` event if required in a subsequent analysis, but that is not the implemented derived M1.1 calculation.

The additional `evidenceInteractions` counter increases by the number of ranges added in each addition action. It is cumulative and does not decrease after removal. It therefore counts range additions rather than clicks, unique references, or final evidence lines. Final ratings and notes are stored independently of the event sequence.

## 6. Telemetry instrumentation

### 6.1 Event structure and capture points

Every recorded telemetry event contains a type, an absolute timestamp, a millisecond offset from trace start, and an optional detail object. React event handlers capture explicit interactions; an `IntersectionObserver` captures trace-row exposure. Events are appended to the active trace response and saved with session state. Their array order is preserved as a zero-based event index in the database.

| Event type | Trigger and stored detail | Capture qualification |
| --- | --- | --- |
| `scroll` | Scrolling the trace container. No position detail. | Accepted at most once per 750 milliseconds using a timestamp check; intervening callbacks are discarded. This is throttling, with no trailing event guarantee. |
| `search` | Every change to the search input; stores the full current `query`. | No debounce or requirement to submit the query. Typing one word can generate several events. |
| `search_navigation` | Previous/next match control when matches exist; stores the resulting zero-based `matchIndex` and `query`. | Increments the navigation counter and initiates smooth scrolling. |
| `wrap_toggle` | Clicking the wrap control; stores the new `enabled` Boolean. | Records changes to text presentation. |
| `line_selection` | Clicking a trace row; stores its one-based `line` and whether Shift extension was requested as `extend`. | Records selection and deselection actions without storing the resulting complete selected set. |
| `lines_viewed` | Observer callback for newly intersecting trace rows; stores a batch of line numbers as `lines`. | Each line is recorded once per viewer lifetime, seeded from previously stored exposure events on resume. |
| `evidence_added` | Confirming selected ranges; stores the number of `ranges` and the total `selectedLines` across those ranges. | One event per confirmation. Individual range bounds and addition times are stored in separate reference records. |
| `evidence_removed` | Removing a retained reference; stores `startLine` and `endLine` when the reference is found. | Does not decrement the cumulative range-addition counter. |
| `answer_changed` | Clicking a rating, directness, or no-reference control; stores only the metric identifier. | Tags are `M2.1`, `M2.2`, `M3.3`, `M4.1`, and `M1.1`. The new answer value is not in the event detail. |

The observer uses the trace scroll container as its root and is configured with an intersection threshold of 0.15. Its callback checks `isIntersecting` but does not explicitly require `intersectionRatio >= 0.15`. Accordingly, this should be reported as intersection-based viewport exposure with a configured 0.15 threshold, not as a guaranteed requirement that 15% of every recorded row was visible. No minimum dwell duration is required. Tall JSON records, wrapping, viewport size, and automatic scrolling can affect which rows intersect the viewport.

Search-triggered smooth scrolling can also emit accepted `scroll` events. A single click on a search arrow can therefore contribute both a search-navigation event and one or more scroll events to `positionChanges`. Questionnaire scrolling and whole-page scrolling are not instrumented by this handler. Scroll events store neither direction nor pixel offset.

### 6.2 Coverage of interaction history

Telemetry provides a partial interaction history, not a screen recording or a complete reconstruction of the participant's behavior. Repeated clicks on an already selected rating or classification can generate `answer_changed` events even if its value is unchanged. Because these events contain a metric identifier but no answer value, intermediate rating values cannot be reconstructed from the event list. Only the final values are retained in the response state.

Notes are updated and persisted as text changes, but note edits have no dedicated telemetry event or edit history. Clearing a temporary line selection also has no event. Choosing the no-reference option clears retained references through an `answer_changed` event tagged `M1.1`; it does not emit one `evidence_removed` event per cleared reference. Evidence-addition event details contain counts rather than exact range identifiers, so removed reference histories are not fully preserved in that event alone.

The implementation does not record eye movements, pointer trajectories, hover dwell, viewport dimensions, tab visibility, focus changes, individual row dwell time, or browser/device characteristics in the study payload. It records search text as part of telemetry. No automated scoring process determines whether an exposed line was read, an evidence reference was correct, or a participant's inference was justified.

## 7. Persistence, submission, and database representation

### 7.1 Local progress and recovery

The browser serializes the session to `localStorage` under `sbench-latin-square-session-v2` whenever the application updates session state. This includes response changes and accepted telemetry events. A session contains a UUID, participant code, Latin-square row, repetition, ordered tasks, session timestamps, current trace index, and trace responses keyed by trace identifier. Each trace response contains its timestamps, counters, retained references, no-reference flag, event array, ratings, classification, and notes.

Local persistence allows continuation after leaving or reloading the interface on the same browser profile. It is not continuous server backup. Incomplete sessions remain local, and browser storage loss or storage failure can compromise recovery. Search queries, wrap state, and temporary unconfirmed line selection are viewer state rather than persisted session fields; they reset when the viewer is remounted. Exposure history and committed responses are restored from the session.

### 7.2 Completion payload and transmission

After the third trace is completed, the completion screen automatically sends JSON to `POST /api/experiment-sessions`. The payload contains `schemaVersion: 4`, experiment identifier `sbench-latin-square-q1-q4`, an `exportedAt` timestamp, the complete session, the ordered trace metadata, and derived metrics keyed by trace identifier. The payload does not embed the trace text itself.

The screen reports sending, success, or failure. On failure, it explains that the data remain in the browser and offers a manual retry. It also provides JSON download and clipboard-copy controls as backup or transfer options. These actions serialize the completion payload. The `exportedAt` value is constructed when the completion component renders, so separate copies of otherwise identical session data can have different export timestamps. The application offers a final control to clear this device's locally stored session. Clearing local state does not delete a session already stored on the server.

### 7.3 Server validation and relational storage

A Node HTTP service receives completed sessions and persists them using SQLite. Its default database is `experiment-frontend/experiment.sqlite`; the path is configurable. The service defaults to listening on `127.0.0.1:8765`. The server records its own `receivedAt` timestamp separately from the client timestamps.

Validation requires a nonempty session identifier and participant code, a completion timestamp, a row between 1 and 3, three distinct tasks, three trace entries, three response objects, and a completed trace index of three. Each trace must have a completion timestamp and either retained evidence or the no-reference flag. Server-side checks are narrower than the UI requirements: they do not comprehensively validate rating ranges, classification values, time consistency, reference bounds, or the correctness of client-derived metrics. The server stores derived metrics supplied by the client rather than recomputing them.

| SQLite table | Stored information |
| --- | --- |
| `experiment_sessions` | Session identity and assignment, participant code, task-set JSON, session start/completion/export/receipt timestamps, experiment identifier, schema version, and the full submitted JSON payload. |
| `trace_responses` | Session/trace linkage, zero-based sequence position, run/task/framework/repetition/model/status metadata, trace timestamps, final ratings and classification, notes, cumulative evidence and navigation counters, and derived-metrics JSON. |
| `evidence_references` | Retained reference identifier, session and trace, inclusive start/end line numbers, addition timestamp, and addition offset in milliseconds. |
| `telemetry_events` | Session and trace, zero-based event index, event type, occurrence timestamp, offset in milliseconds, and detail JSON. |

The full payload preserves fields that do not have dedicated relational columns, including the no-reference flag and agent execution duration. Foreign keys link reference and event rows to trace responses. Writes occur in a transaction. The session UUID is the primary key: resubmitting a session updates its parent record, deletes its previous child trace rows with cascading deletion, and inserts the submitted trace, reference, and event records. Retries therefore replace a session representation rather than append duplicate sessions. The database is not an append-only revision history; the server receipt time is updated on resubmission.

### 7.4 Participant identification and data handling

The application requests a participant code rather than a name or email address. Repository guidance instructs researchers to use pseudonymous codes. The software does not itself prevent identifying information from being entered in that field, notes, or search queries. No consent form, demographic questionnaire, retention policy, or participant recruitment procedure is implemented in these screens. Those elements, if used in the study, must be described from the actual research protocol. The experiment service does not implement an authentication layer, and deployment access controls are outside this UI description.

## 8. Interpretation and reproducibility considerations

The instrument combines subjective judgments with behavioral proxies for the effort of inspecting traces. Its scope supports comparisons of reported confidence, cognitive effort, ease, evidence location and timing, and recorded navigation activity. It does not establish that a participant correctly reconstructed the agent's reasoning or that a trace is objectively auditable according to an external ground truth.

Analysis must preserve the distinction between final-state metrics and historical events. Retained evidence counts omit removed references, whereas cumulative range additions and telemetry include earlier actions. M1.1 can change when an earlier reference is removed. M4.2 measures the last classification click and can increase after a repeated click without a change in classification. An explicit no-reference outcome should remain distinguishable from missing data and from a zero-millisecond evidence latency.

Timing should be described as elapsed assessment time, with its loading and interruption exposure stated. Exposure counts should be described as observed row intersections rather than lines read. Navigation counts should be described as throttled scroll and search-navigation events, recognizing their possible overlap. The line unit must remain the processed source record because formatted JSON can span multiple visual lines.

The square balances framework position when rows are equally represented and task order is held constant. It does not independently vary task order, and its three cyclic orders do not provide complete transition balance. Participant numbers, assignment balance, exclusions, inferential tests, and effect estimates must come from the actual study data and protocol, not from the existence of these controls.

For a reproducible report, retain the application revision, prepared manifest and log files, actual task order and repetition, realized trace identifiers, deployment configuration, and exported session data. Record the study's device and browser conditions separately because the payload does not capture them. Preserve both raw events and derived values so that any later analytical definition, such as first-ever evidence latency, can be distinguished from the metrics exported by the implemented interface.

## Appendix. Implementation sources

The following repository files ground this description. They are implementation references, not external methodological citations.

| Source | Relevant implementation |
| --- | --- |
| `experiment-frontend/src/App.tsx` | Tutorial, configuration, viewer, questionnaire, trace assignment, timing, telemetry handlers, metric derivation, local persistence, completion and export. |
| `experiment-frontend/src/types.ts` | Session, trace response, reference, telemetry, and manifest field definitions. |
| `experiment-frontend/src/data.ts` | Latin-square orders and default task set. |
| `experiment-frontend/src/components/ui.tsx` | Five-point scales, progress indicators, and shared controls. |
| `experiment-frontend/src/index.css` and `tailwind.config.js` | Typography, colors, and responsive presentation. |
| `experiment-frontend/scripts/prepare-data.mjs` | Trace discovery, exact task-statement removal, ANSI sequence removal, metadata extraction, and manifest ordering. |
| `experiment-frontend/server.mjs` | Submission endpoint, validation, transaction behavior, relational schema, and static serving. |
| `experiment-frontend/README.md` | Execution instructions and pseudonymous participant-code guidance. |
