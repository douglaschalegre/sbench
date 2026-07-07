# E05: Controle de Escopo e Estabilidade de Objetivo

## Diferencas cobertas

| # | Diferenca no documento |
|---:|---|
| 5 | Fatos acumulados |
| 9 | Controle de escopo |
| 17 | Estabilidade de objetivo |

## O que mostra

Mostra como o controle de escopo aparece nos tres traces. No BDI, regras de escopo, objetivo central, pedidos secundarios e exclusoes viram crencas nomeadas com certeza. No Codex e no OpenCode, o escopo e auditavel pela leitura dos arquivos, mensagens e artefatos finais, mas nao aparece como estado persistente do agente.

## Task

`shelter_restock_scope`

## Fontes

| Harness | Log | Linhas |
|---|---|---:|
| BDI | `runs/20260615T221949Z/entries/shelter_restock_scope/bdi/r3/stdout.log` | 56-63, 73-75 |
| Codex | `runs/20260615T221949Z/entries/shelter_restock_scope/codex/r3/stdout.log` | 12-17, 32-33, 38 |
| OpenCode | `runs/20260615T221949Z/entries/shelter_restock_scope/opencode/r3/stdout.log` | 9-15, 18, 29-31, 37 |

## BDI

```text
Current known information (beliefs):
  required_deliverables:
    answer/core_purchase_list.md; answer/scope_control.md; answer/final_restock_note.md
    Certainty: 0.99

  core_task_objective:
    Prepare the Phase 1 purchase packet for the North Shelter restock;
    explicitly document which secondary requests are outside the current packet
    Certainty: 0.96

  supply_request_selection_rules:
    Include only phase=1, approved, medical/shelter/power/water,
    deliverable by need-by date, within $2,200.00 budget
    Certainty: 0.99

  secondary_requests_handling:
    Secondary requests must be recorded as deferred or out of scope
    and not completed as part of the core restock work
    Certainty: 0.98

  out_of_scope_exclusions:
    Do not design banners, draft training agendas, choose media gear,
    or plan phase-two signage
    Certainty: 0.96

Desire 'desire_7238059b' status updated to DesireStatus.ACHIEVED
```

## Codex

```json
{"type":"command_execution","command":"sed -n '1,220p' task.md",
  "aggregated_output":"Do not complete out-of-scope requests as if they are part of the core restock work."}

{"type":"command_execution","command":"sed -n '1,260p' 01_scope_and_purchase_rules.md",
  "aggregated_output":"Do not complete secondary communications, training, media, or phase-two planning requests..."}

{"type":"command_execution","command":"sed -n '1,260p' answer/scope_control.md",
  "aggregated_output":"Out-of-scope requests were not completed as part of the restock packet."}

{"type":"agent_message",
  "text":"Secondary requests were recorded as defer or out of scope without being completed."}
```

## OpenCode

```json
{"tool":"read","input":{"filePath":".../task.md"},
  "output":"Do not complete out-of-scope requests as if they are part of the core restock work."}

{"tool":"read","input":{"filePath":".../01_scope_and_purchase_rules.md"},
  "output":"Do not complete secondary communications, training, media, or phase-two planning requests..."}

{"tool":"todowrite","input":{"todos":[
  {"content":"Analyze inputs and determine in-scope restock selections","status":"completed"},
  {"content":"Create answer/scope_control.md documenting packet scope boundaries","status":"pending"}
]}}

{"tool":"read","input":{"filePath":".../answer/scope_control.md"},
  "output":"Out-of-scope requests were not completed as part of the restock packet."}
```

## Takeaway

BDI torna as regras de escopo estado persistente. Codex e OpenCode tambem permitem auditar o escopo, mas pela leitura dos arquivos e artefatos finais.
