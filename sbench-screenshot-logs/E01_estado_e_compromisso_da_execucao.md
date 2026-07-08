# E01: Estado e Compromisso da Execucao

## Diferenca sintetizada

O BDI representa explicitamente o estado e o compromisso ativo da execucao, enquanto Codex e OpenCode representam esse compromisso de forma operacional, por transcript, mensagens, eventos ou checklist.

## Diferencas originais absorvidas

| # | Diferenca no documento |
|---:|---|
| 1 | Estado deliberativo |
| 6 | Intencao ativa |
| 18 | Plano do runtime vs checklist de trabalho |

## O que mostra

Mostra a diferenca entre um trace com estado deliberativo explicito e traces baseados em interacao operacional. No BDI aparecem `Beliefs`, `Desires`, `Intentions` e plano ativo. No Codex aparecem thread, turno, mensagem e comandos. No OpenCode aparecem steps e `todowrite`, que funcionam como checklist operacional, nao como desejo/intencao/plano BDI.

## Task

`incident_staffing_plan`

## Fontes

| Harness | Log | Linhas |
|---|---|---:|
| BDI | `runs/20260615T221949Z/entries/incident_staffing_plan/bdi/r3/stdout.log` | 13-26 |
| Codex | `runs/20260615T221949Z/entries/incident_staffing_plan/codex/r3/stdout.log` | 1-10 |
| OpenCode | `runs/20260615T221949Z/entries/incident_staffing_plan/opencode/r3/stdout.log` | 2-5 |

## BDI

```text
States before starting BDI cycle
Beliefs: 5 items
Desires: 1 items | Desire 'desire_8113beaf' pending
Intentions: 0 items

--- BDI Cycle Start ---
No current intentions, but active/pending desires exist.
Generating intentions...

...

Generated 1 high-level intentions.
Desire 'desire_8113beaf' status updated to DesireStatus.ACTIVE
Desires: 1 items | Desire 'desire_8113beaf' active

Intentions: 1 items |
  Desire 'desire_8113beaf'
  Intention 'Inspect the task instructions and local non-hidden files...'
  Plan active
  Plan Step 1/1: Inspect the task instructions...
```

## Codex

```json
{"type":"thread.started"}
{"type":"turn.started"}

{"type":"item.completed","item":{"type":"agent_message",
  "text":"I'm reading the task files in this workspace first..."}}

...

{"type":"item.started","item":{"type":"command_execution",
  "command":"/bin/zsh -lc pwd","status":"in_progress"}}

...

{"type":"item.completed","item":{"type":"command_execution",
  "command":"/bin/zsh -lc 'rg --files'",
  "exit_code":0,"status":"completed"}}
```

## OpenCode

```json
{"type":"step_start"}

{"type":"text",
  "text":"Reviewing the task files first, then I'll produce the requested deliverables under answer/."}

{"type":"tool_use","part":{"tool":"todowrite",
  "input":{"todos":[
    {"content":"Read task.md and local context files...","status":"in_progress"},
    {"content":"Create deliverables in answer/...","status":"pending"},
    {"content":"Verify deliverables match the task instructions","status":"pending"}
  ]}}}

{"type":"step_finish","part":{"reason":"tool-calls"}}
```

## Takeaway

BDI mostra estado deliberativo explicito. Codex mostra transcript operacional. OpenCode mostra steps e checklist operacional, mas nao desejo/intencao/plano BDI.
