# E02: Cronologia Operacional e Evidencia Bruta

## Diferencas cobertas

| # | Diferenca no documento |
|---:|---|
| 10 | Cronologia de acoes |
| 11 | Progresso operacional |
| 13 | Evidencia bruta vs estado interpretado |

## O que mostra

Mostra que Codex e OpenCode preservam melhor a cronologia bruta de acoes, como comandos, patches, leituras e arquivos criados. O BDI tambem registra ferramentas e resultados, mas a acao aparece encapsulada no ciclo deliberativo e resumida por estados semanticos, como passo bem-sucedido e desejo satisfeito.

## Task

`incident_staffing_plan`

## Fontes

| Harness | Log | Linhas |
|---|---|---:|
| BDI | `runs/20260615T221949Z/entries/incident_staffing_plan/bdi/r3/stdout.log` | 27, 32-39 |
| Codex | `runs/20260615T221949Z/entries/incident_staffing_plan/codex/r3/stdout.log` | 23-35 |
| OpenCode | `runs/20260615T221949Z/entries/incident_staffing_plan/opencode/r3/stdout.log` | 20-29 |

## BDI

```text
bdi.agent.run.completed run_index=7
  Task: Inspect the task instructions and local non-hidden files...
  tool_calls: run_in_task(...)
  assistant: Done - inspected task files and created deliverables.

Plan Step 1 successful.
Plan for desire 'desire_8113beaf' completed all Plan Steps

Desire 'desire_8113beaf' status updated to DesireStatus.ACHIEVED
Desire 'desire_8113beaf' satisfied.
Reason: task files were inspected and required deliverables were created.
```

## Codex

```json
{"type":"item.completed","item":{"type":"agent_message",
  "text":"I've resolved the candidate pool. I'm creating the answer/ deliverables now..."}}

{"type":"item.started","item":{"type":"file_change",
  "changes":[
    {"path":".../answer/access_resolution.md","kind":"add"},
    {"path":".../answer/candidate_screen.md","kind":"add"},
    {"path":".../answer/staffing_assignment.md","kind":"add"}
  ],"status":"in_progress"}}

{"type":"item.completed","item":{"type":"file_change","status":"completed"}}

{"type":"item.completed","item":{"type":"command_execution",
  "command":"sed -n '1,220p' answer/access_resolution.md",
  "exit_code":0,"status":"completed"}}
```

## OpenCode

```json
{"type":"tool_use","part":{"tool":"apply_patch",
  "input":{"patchText":"*** Add File: .../answer/access_resolution.md\n..."}}}

{"type":"step_finish","part":{"reason":"tool-calls"}}

{"type":"tool_use","part":{"tool":"read",
  "input":{"filePath":".../answer/candidate_screen.md"}}}

{"type":"tool_use","part":{"tool":"read",
  "input":{"filePath":".../answer/staffing_assignment.md"}}}

{"type":"tool_use","part":{"tool":"todowrite",
  "input":{"todos":[{"status":"completed"},{"status":"completed"},{"status":"completed"}]}}}
```

## Takeaway

Codex e OpenCode preservam melhor a trilha operacional bruta. BDI tambem registra acoes, mas elas aparecem dentro do ciclo deliberativo e sao resumidas por estados semanticos.
