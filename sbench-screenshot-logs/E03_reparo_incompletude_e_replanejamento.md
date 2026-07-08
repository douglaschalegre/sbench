# E03: Reparo, Incompletude e Replanejamento

## Diferenca sintetizada

O BDI torna explicita a diferenca entre executar um plano e satisfazer o objetivo, permitindo observar incompletude e replanejamento; Codex e OpenCode deixam esse reparo mais dependente da sequencia operacional.

## Diferencas originais absorvidas

| # | Diferenca no documento |
|---:|---|
| 3 | Plano concluido vs objetivo satisfeito |
| 4 | Replanejamento |
| 7 | Avaliacao semantica dos passos |
| 16 | Auditabilidade de erro |

## O que mostra

Mostra a mesma situacao de reparo nos tres harnesses. No BDI, o plano termina, mas o desejo volta para `pending` porque o objetivo ainda nao foi satisfeito; em seguida uma nova intencao e criada. No Codex, o reparo aparece como continuidade do transcript. No OpenCode, o reparo aparece por leitura da atualizacao, `todowrite` e escrita dos artefatos.

## Task

`community_workshop_replan`

## Fontes

| Harness | Log | Linhas |
|---|---|---:|
| BDI | `runs/20260615T221949Z/entries/community_workshop_replan/bdi/r3/stdout.log` | 29-59 |
| Codex | `runs/20260615T221949Z/entries/community_workshop_replan/codex/r3/stdout.log` | 23-31, 37-41 |
| OpenCode | `runs/20260615T221949Z/entries/community_workshop_replan/opencode/r3/stdout.log` | 14, 18, 22, 26-31 |

## BDI

```text
Plan Step 1 successful.
Plan for desire 'desire_a35bca05' completed all Plan Steps

Intention ... Plan completed
Completed final step. Intention ... finished.

Desire 'desire_a35bca05' status updated to DesireStatus.PENDING
Desires: 1 items | Desire 'desire_a35bca05' pending

Desire 'desire_a35bca05' is not satisfied and its plan is exhausted;
returning to PENDING for replanning.

Reason: deliverables in answer/ were not created or verified.

...

Cycle 2/30
Generated 1 high-level intentions.
Desire 'desire_a35bca05' status updated to DesireStatus.ACTIVE

Intention 'Create and verify the required room-planning deliverables...'
Plan active
```

## Codex

```json
{"type":"item.completed","item":{"type":"command_execution",
  "command":"sed -n '1,220p' staged_update/05_facility_update_2026-06-10.md",
  "aggregated_output":"Bay Workshop is closed... Delta Annex has been released..."}}

...

{"type":"item.completed","item":{"type":"agent_message",
  "text":"I've resolved the initial and updated room logic. I'm creating the answer/ packet now..."}}

...

{"type":"item.completed","item":{"type":"file_change",
  "changes":[
    {"path":".../answer/initial_room_plan.md","kind":"add"},
    {"path":".../answer/update_response.md","kind":"add"},
    {"path":".../answer/final_room_plan.md","kind":"add"}
  ]}}
```

## OpenCode

```json
{"type":"tool_use","part":{"tool":"read",
  "input":{"filePath":".../staged_update/05_facility_update_2026-06-10.md"},
  "output":"Bay Workshop is closed... Delta Annex has been released..."}}

...

{"type":"tool_use","part":{"tool":"todowrite",
  "input":{"todos":[
    {"content":"Derive initial valid room assignments...","status":"in_progress"},
    {"content":"Apply staged facility update and identify preserved vs replaced assignments","status":"pending"},
    {"content":"Create answer/ deliverables...","status":"pending"}
  ]}}}

...

{"type":"tool_use","part":{"tool":"apply_patch",
  "input":{"patchText":"*** Add File: .../answer/update_response.md\n..."}}}
```

## Takeaway

BDI mostra replanejamento como transicao de estado. Codex e OpenCode mostram o reparo pela sequencia de leitura, escrita, verificacao e checklist.
