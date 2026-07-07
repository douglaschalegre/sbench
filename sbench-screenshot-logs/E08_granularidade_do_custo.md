# E08: Granularidade do Custo

## Diferencas cobertas

| # | Diferenca no documento |
|---:|---|
| 14 | Granularidade do custo |

## O que mostra

Mostra em que nivel cada harness torna custo observavel. No BDI, ha custos em chamadas internas do ciclo deliberativo e um agregado final. No Codex, o custo aparece agregado no `turn.completed`. No OpenCode, o custo aparece por `step_finish`, permitindo ver o custo por etapa operacional.

## Task

`incident_staffing_plan`

## Fontes

| Harness | Log | Linhas |
|---|---|---:|
| BDI | `runs/20260615T221949Z/entries/incident_staffing_plan/bdi/r3/stdout.log` | 8-12, 20, 27-29, 36, 50 |
| Codex | `runs/20260615T221949Z/entries/incident_staffing_plan/codex/r3/stdout.log` | 36 |
| OpenCode | `runs/20260615T221949Z/entries/incident_staffing_plan/opencode/r3/stdout.log` | 5, 9, 17, 21, 27, 30, 33 |

## BDI

```text
bdi.agent.run.completed run_index=2
  purpose: resolve belief name `task_file`
  usage: requests=1, tool_calls=0, total_tokens=347

bdi.agent.run.completed run_index=3
  purpose: resolve belief name `answer_folder`
  usage: requests=1, tool_calls=0, total_tokens=345

bdi.agent.run.completed run_index=4
  purpose: resolve belief name `filesystem_mcp_server_name`
  usage: requests=1, tool_calls=0, total_tokens=350

bdi.agent.run.completed run_index=5
  purpose: resolve belief name `terminal_tool_name`
  usage: requests=1, tool_calls=0, total_tokens=360

bdi.agent.run.completed run_index=8
  purpose: evaluate step success
  usage: per-call usage object in trace

bdi.agent.run.completed run_index=11
  purpose: assess desire satisfaction
  usage: per-call usage object in trace

bdi.run.completed
  requests: 14
  tool_calls: 3
  total_tokens: 15204
```

## Codex

```json
{"type":"turn.completed","usage":{
  "input_tokens":73402,
  "cached_input_tokens":59264,
  "output_tokens":2523,
  "reasoning_output_tokens":454
}}
```

## OpenCode

```json
{"type":"step_finish","part":{"reason":"tool-calls",
  "tokens":{"total":7299,"input":7174,"output":111,"reasoning":14}}}

{"type":"step_finish","part":{"reason":"tool-calls",
  "tokens":{"total":7507,"input":760,"output":91,"reasoning":0}}}

{"type":"step_finish","part":{"reason":"tool-calls",
  "tokens":{"total":11369,"input":2131,"output":1012,"reasoning":546}}}

{"type":"step_finish","part":{"reason":"stop",
  "tokens":{"total":12960,"input":598,"output":74,"reasoning":0}}}
```

## Takeaway

BDI permite atribuir custo a partes do ciclo deliberativo. Codex apresenta uso agregado por turno. OpenCode apresenta custo por step operacional.
