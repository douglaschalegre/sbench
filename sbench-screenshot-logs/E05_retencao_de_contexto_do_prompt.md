# E05: Retencao de Contexto do Prompt

## Diferenca sintetizada

O BDI torna observavel quais fatos e restricoes do prompt/tarefa foram retidos como crencas e reinseridos nos prompts internos. Codex e OpenCode exigem seguir o transcript, leituras de arquivos, mensagens, checklist e verificacoes para reconstruir o contexto mantido.

## Diferencas originais absorvidas

| # | Diferenca no documento |
|---:|---|
| 5 | Fatos acumulados |
| 17 | Estabilidade de objetivo |

## O que mostra

Mostra como seguir, no log, o que foi retido do prompt e dos arquivos da tarefa. No BDI, o contexto aparece como `Current Beliefs` e volta explicitamente nos prompts internos seguintes. No Codex e no OpenCode, a retencao precisa ser reconstruida pela sequencia de leituras, mensagens de progresso, checklist e verificacoes de artefatos.

Cautela: isso mede rastreabilidade do contexto retido, nao correcao externa do contexto retido.

## Task

`community_workshop_replan`

## Fontes

| Harness | Log | Linhas |
|---|---|---:|
| BDI | `runs/20260615T221949Z/entries/community_workshop_replan/bdi/r3/stdout.log` | 53, 58-60, 67, 70 |
| Codex | `runs/20260615T221949Z/entries/community_workshop_replan/codex/r3/stdout.log` | 14, 24-25, 39, 41 |
| OpenCode | `runs/20260615T221949Z/entries/community_workshop_replan/opencode/r3/stdout.log` | 4, 14, 17-18, 27, 31, 34 |

## BDI

```text
Current Beliefs:
  required_deliverables:
    answer/initial_room_plan.md; answer/update_response.md; answer/final_room_plan.md
    Certainty: 0.99

  task_constraints:
    Use only local files; assign exactly one valid room to each of 3 sessions;
    hard requirements are availability, capacity, equipment/traits, cost <= $800;
    if update invalidates part of plan, repair only affected assignment
    Certainty: 0.96

  source_files_reviewed:
    00_room_request.md; 01_planning_rules.md; 02_sessions.csv;
    03_room_options.csv; 04_initial_facility_note_2026-06-01.md;
    staged_update/05_facility_update_2026-06-10.md; output_contract.md
    Certainty: 0.98

  initial_room_plan:
    S-101 -> Harbor Hall; S-102 -> Bay Workshop; S-103 -> Cedar Room;
    total $700
    Certainty: 0.78

  facility_update_impact:
    Bay Workshop unavailable; preserve S-101 and S-103;
    replace S-102 with Delta Annex; final total $770
    Certainty: 0.78

...

Intention 'Create and verify the required room-planning deliverables...
preserving unaffected valid assignments while repairing the invalidated session assignment.'

...

Current known information (beliefs):
  required_deliverables: answer/initial_room_plan.md; answer/update_response.md; answer/final_room_plan.md
  task_constraints: use local files; assign exactly one valid room; cost <= $800; repair only affected assignment
  source_files_reviewed: 00_room_request.md; 01_planning_rules.md; 02_sessions.csv; ...
  initial_room_plan: S-101 -> Harbor Hall; S-102 -> Bay Workshop; S-103 -> Cedar Room; total $700
  facility_update_impact: Bay Workshop unavailable; preserve S-101 and S-103; replace S-102 with Delta Annex

...

Desire 'desire_a35bca05' satisfied.
Reason: task files were reviewed, deliverables were created,
and the repaired final plan satisfies the stated constraints while preserving unaffected assignments.
```

## Codex

```json
{"type":"command_execution","command":"sed -n '1,220p' task.md",
  "aggregated_output":"The top-level objective stays the same throughout: leave behind a room assignment package for all three sessions."}

...

{"type":"command_execution","command":"sed -n '1,220p' staged_update/05_facility_update_2026-06-10.md",
  "aggregated_output":"The workshop objective has not changed: cover all three sessions with valid rooms and stay within the $800 ceiling."}

...

{"type":"agent_message",
  "text":"I've resolved the initial and updated room logic. I'm creating the answer/ packet now with the initial plan, the update repair note, and the final preserved plan."}

...

{"type":"command_execution","command":"sed -n '1,220p' answer/final_room_plan.md",
  "aggregated_output":"Objective Check: The same workshop objective is still covered... Preserved Work: S-101 -> Harbor Hall and S-103 -> Elm Room."}

...

{"type":"agent_message",
  "text":"After the 2026-06-10 facility update, only S-102 needed repair, so the final plan preserves the other two assignments..."}
```

## OpenCode

```json
{"tool":"read","input":{"filePath":".../task.md"},
  "output":"The top-level objective stays the same throughout: leave behind a room assignment package for all three sessions."}

...

{"tool":"read","input":{"filePath":".../staged_update/05_facility_update_2026-06-10.md"},
  "output":"The workshop objective has not changed: cover all three sessions with valid rooms and stay within the $800 ceiling."}

...

{"type":"text",
  "text":"Planning the deliverables now: derive the initial valid assignments... then apply the dated facility update while preserving unaffected assignments."}

...

{"tool":"todowrite","input":{"todos":[
  {"content":"Derive initial valid room assignments and budget from planning files","status":"in_progress"},
  {"content":"Apply staged facility update and identify preserved vs replaced assignments","status":"pending"},
  {"content":"Create answer/ deliverables with initial, update, and final room plans","status":"pending"}
]}}

...

{"tool":"read","input":{"filePath":".../answer/final_room_plan.md"},
  "output":"Continuity Notes: The same workshop objective is still covered... Preserved work from the initial plan: S-101 stayed in Harbor Hall and S-103 stayed in Elm Room..."}

...

{"type":"text","metadata":{"openai":{"phase":"final_answer"}},
  "text":"Preserved assignments: S-101 -> Harbor Hall, S-103 -> Elm Room. Repaired assignment: S-102 moved from Bay Workshop to Delta Annex..."}
```

## Takeaway

BDI mostra o contexto retido como crencas reinjetadas nos prompts internos. Codex e OpenCode tambem permitem seguir o contexto retido, mas pela continuidade do transcript: leituras, mensagens, checklist, verificacoes e resposta final. A evidencia mostra o que foi retido, nao garante que o conteudo retido esteja correto.
