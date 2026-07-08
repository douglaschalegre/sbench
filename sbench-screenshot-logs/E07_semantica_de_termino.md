# E07: Semantica de Termino

## Diferenca sintetizada

O BDI encerra a execucao com semantica interna de desejo atingido e estado final; Codex encerra o turno; OpenCode encerra o step, exigindo mais apoio da resposta final, artefatos ou status externo para concluir sucesso da tarefa.

## Diferencas originais absorvidas

| # | Diferenca no documento |
|---:|---|
| 2 | Objetivos atingidos |
| 8 | Termino da execucao |
| 15 | Tipo de sucesso observado |

## O que mostra

Mostra como cada harness representa o fim da execucao. No BDI, o termino inclui `DesireStatus.ACHIEVED`, `outcome: achieved`, ciclos, crencas e status dos desejos; isso e uma semantica interna do runtime. No Codex, o fim aparece como resposta final e `turn.completed`. No OpenCode, aparece como resposta final e `step_finish` com `reason: stop`.

## Task

`incident_staffing_plan`

## Fontes

| Harness | Log | Linhas |
|---|---|---:|
| BDI | `runs/20260615T221949Z/entries/incident_staffing_plan/bdi/r3/stdout.log` | 37-50 |
| Codex | `runs/20260615T221949Z/entries/incident_staffing_plan/codex/r3/stdout.log` | 35-36 |
| OpenCode | `runs/20260615T221949Z/entries/incident_staffing_plan/opencode/r3/stdout.log` | 32-33 |

## BDI

```text
Desire 'desire_8113beaf' status updated to DesireStatus.ACHIEVED
Desires: 1 items | Desire 'desire_8113beaf' achieved

Desire 'desire_8113beaf' satisfied.
Reason: task files were inspected, required deliverables were created,
and there are no remaining intentions or indications of missing work.

--- BDI Cycle End (terminal) ---
States after BDI cycle (terminal)
Beliefs: 8 items
Desires: 1 items | Desire 'desire_8113beaf' achieved
Intentions: 0 items

Task result: achieved; cycles=1/30; elapsed_seconds=67

{"type":"bdi.run.completed",
 "outcome":"achieved",
 "bdi":{"beliefs":8,"cycle_count":1,
        "desires":[{"status":"achieved"}],"intentions":0},
 "usage":{"requests":14,"tool_calls":3,"total_tokens":15204}}
```

## Codex

```json
{"type":"item.completed","item":{"type":"agent_message",
  "text":"Completed the task and created the required deliverables under answer/...
  Final assignment is Ben as primary and Deepa as backup."}}

{"type":"turn.completed","usage":{
  "input_tokens":73402,
  "cached_input_tokens":59264,
  "output_tokens":2523,
  "reasoning_output_tokens":454
}}
```

## OpenCode

```json
{"type":"text","metadata":{"openai":{"phase":"final_answer"}},
  "text":"Completed the requested work under answer/...
  Final assignment: Primary Ben, Backup Deepa"}

{"type":"step_finish","part":{
  "reason":"stop",
  "tokens":{"total":12960,"input":598,"output":74,"reasoning":0}
}}
```

## Takeaway

BDI termina com semantica interna de desejo atingido. Codex termina o turno. OpenCode termina o step com `reason: stop`. Sucesso externo da tarefa ainda depende da resposta final, dos artefatos ou de avaliacao externa.
