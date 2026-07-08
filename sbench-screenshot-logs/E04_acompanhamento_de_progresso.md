# E04: Acompanhamento de Progresso

## Diferenca sintetizada

O acompanhamento de progresso muda conforme o harness: BDI acompanha plano e intencao no runtime, OpenCode acompanha uma checklist operacional, e Codex acompanha progresso por narrativa e eventos.

## Diferencas originais absorvidas

| # | Diferenca no documento |
|---:|---|
| 6 | Intencao ativa |
| 11 | Progresso operacional |
| 18 | Plano do runtime vs checklist de trabalho |

## O que mostra

Mostra a diferenca entre plano como estado do runtime e checklist como organizacao operacional. No BDI, a intencao e o plano estao associados ao desejo. No Codex, o progresso aparece em mensagens narrativas e eventos de arquivo. No OpenCode, o progresso aparece em `todowrite` com itens `in_progress`, `pending` e `completed`.

## Task

`community_workshop_replan`

## Fontes

| Harness | Log | Linhas |
|---|---|---:|
| BDI | `runs/20260615T221949Z/entries/community_workshop_replan/bdi/r3/stdout.log` | 53-59, 63-70 |
| Codex | `runs/20260615T221949Z/entries/community_workshop_replan/codex/r3/stdout.log` | 25-32, 37-41 |
| OpenCode | `runs/20260615T221949Z/entries/community_workshop_replan/opencode/r3/stdout.log` | 18, 31, 34-35 |

## BDI

```text
Generated 1 high-level intentions.
Desire 'desire_a35bca05' status updated to DesireStatus.ACTIVE

Intentions: 1 items |
  Desire 'desire_a35bca05'
  Intention 'Create and verify the required room-planning deliverables...'
  Plan active
  Plan Step 1/1: Create and verify...

...

Plan Step 1 successful.
Plan for desire 'desire_a35bca05' completed all Plan Steps
Intentions: 1 items | ... Plan completed
```

## Codex

```json
{"type":"agent_message",
  "text":"I've resolved the initial and updated room logic. I'm creating the answer/ packet now..."}

...

{"type":"file_change","changes":[
  {"path":".../answer/initial_room_plan.md","kind":"add"},
  {"path":".../answer/update_response.md","kind":"add"},
  {"path":".../answer/final_room_plan.md","kind":"add"}
]}

...

{"type":"agent_message",
  "text":"The review packet is written. I'm doing a quick verification pass..."}
```

## OpenCode

```json
{"tool":"todowrite","input":{"todos":[
  {"content":"Derive initial valid room assignments and budget from planning files",
   "status":"in_progress"},
  {"content":"Apply staged facility update and identify preserved vs replaced assignments",
   "status":"pending"},
  {"content":"Create answer/ deliverables with initial, update, and final room plans",
   "status":"pending"}
]}}

...

{"tool":"todowrite","input":{"todos":[
  {"content":"Derive initial valid room assignments and budget from planning files",
   "status":"completed"},
  {"content":"Apply staged facility update and identify preserved vs replaced assignments",
   "status":"completed"},
  {"content":"Create answer/ deliverables with initial, update, and final room plans",
   "status":"completed"}
]}}
```

## Takeaway

No BDI, plano e intencao fazem parte do runtime deliberativo e estao associados ao desejo. No OpenCode, `todowrite` e uma checklist operacional. No Codex, progresso aparece como narrativa e eventos.
