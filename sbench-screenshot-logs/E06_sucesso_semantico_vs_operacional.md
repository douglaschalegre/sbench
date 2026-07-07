# E06: Sucesso Semantico vs Sucesso Operacional

## Diferencas cobertas

| # | Diferenca no documento |
|---:|---|
| 7 | Avaliacao semantica dos passos |
| 15 | Tipo de sucesso observado |

## O que mostra

Mostra a diferenca entre sucesso semantico e sucesso operacional. No BDI, ha avaliacao explicita sobre se o passo e o desejo foram satisfeitos. No Codex, o sucesso aparece principalmente como comandos com `exit_code: 0`, mudancas de arquivo e verificacoes. No OpenCode, aparece como ferramentas concluidas, steps finalizados e `todos` completos.

## Task

`incident_staffing_plan`

## Fontes

| Harness | Log | Linhas |
|---|---|---:|
| BDI | `runs/20260615T221949Z/entries/incident_staffing_plan/bdi/r3/stdout.log` | 28, 32, 36-39 |
| Codex | `runs/20260615T221949Z/entries/incident_staffing_plan/codex/r3/stdout.log` | 14-25, 28-34 |
| OpenCode | `runs/20260615T221949Z/entries/incident_staffing_plan/opencode/r3/stdout.log` | 20-21, 29-30 |

## BDI

```text
Evaluate if the step successfully achieved its original objective.

assistant: {"success": true,
  "reason": "The step reports that it inspected the task files
  and created the required deliverables..."}

Plan Step 1 successful.

Assess whether the Desire is satisfied after a completed Intention.

Desire 'desire_8113beaf' status updated to DesireStatus.ACHIEVED
Desire 'desire_8113beaf' satisfied.
Reason: task files were inspected and required deliverables were created.
```

## Codex

```json
{"type":"command_execution",
  "command":"sed -n '1,260p' availability_notes.md",
  "exit_code":0,"status":"completed"}

{"type":"command_execution",
  "command":"sed -n '1,220p' output_contract.md",
  "exit_code":0,"status":"completed"}

{"type":"file_change",
  "changes":[{"path":".../answer/access_resolution.md","kind":"add"}],
  "status":"completed"}

{"type":"command_execution",
  "command":"find answer -maxdepth 1 -type f | sort",
  "aggregated_output":"answer/access_resolution.md\nanswer/candidate_screen.md\nanswer/staffing_assignment.md\n",
  "exit_code":0,"status":"completed"}
```

## OpenCode

```json
{"type":"tool_use","part":{"tool":"apply_patch",
  "state":{"status":"completed"}}}

{"type":"step_finish","part":{"reason":"tool-calls"}}

{"type":"tool_use","part":{"tool":"todowrite",
  "state":{"status":"completed"},
  "input":{"todos":[
    {"status":"completed"},
    {"status":"completed"},
    {"status":"completed"}
  ]}}}
```

## Takeaway

BDI registra julgamento semantico sobre passo e desejo. Codex e OpenCode registram sucesso operacional de comandos, ferramentas, arquivos e checklist.
