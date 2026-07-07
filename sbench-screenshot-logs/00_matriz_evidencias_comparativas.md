# Matriz de Evidencias Comparativas

Fonte comum:

- `run_id`: `20260615T221949Z`
- repeticao: `r3`
- raiz dos logs: `/Users/douglas/code/masters/sbench/runs/20260615T221949Z/entries`

## Exemplos Propostos

| Exemplo | Diferencas cobertas | Task | O que mostra |
|---|---:|---|---|
| `E01_estado_inicial_vs_transcript.md` | 1, 6, 18 | `incident_staffing_plan` | BDI tem `Beliefs/Desires/Intentions`; Codex tem transcript; OpenCode tem step/todos |
| `E02_cronologia_operacional.md` | 10, 11, 13 | `incident_staffing_plan` | Codex/OpenCode mostram acoes brutas melhor; BDI encapsula acoes no ciclo |
| `E03_replanejamento.md` | 3, 4, 7, 16 | `community_workshop_replan` | BDI volta desejo para `pending`; Codex/OpenCode continuam por transcript/todos |
| `E04_plano_runtime_vs_checklist.md` | 6, 11, 18 | `community_workshop_replan` | BDI tem plano ligado a desejo; OpenCode tem checklist; Codex tem narrativa |
| `E05_controle_de_escopo.md` | 5, 9, 17 | `shelter_restock_scope` | BDI guarda escopo como crenca; outros mostram escopo por arquivos/artefatos |
| `E06_sucesso_semantico_vs_operacional.md` | 7, 15 | `incident_staffing_plan` | BDI avalia sucesso semantico; Codex/OpenCode mostram status operacional |
| `E07_termino_da_execucao.md` | 2, 8, 15 | `incident_staffing_plan` | BDI termina com `achieved`; Codex `turn.completed`; OpenCode `reason: stop` |
| `E08_granularidade_do_custo.md` | 14 | `incident_staffing_plan` | BDI custo por chamadas internas; Codex por turno; OpenCode por steps |

## Diferencas Sem Print Proprio Por Enquanto

| Diferenca | Motivo |
|---|---|
| 12: onde esta a explicacao | Depende da comparacao geral entre exemplos |
| 13: evidencia bruta vs estado interpretado | Entra em `E02` e `E05` |
| 16: auditabilidade de erro | Entra em `E03` |
| 17: estabilidade de objetivo | Entra em `E05` |
| 19: confiabilidade do trace | E cautela metodologica, nao uma linha especifica do log |

## Consolidacao Recomendada

| Grupo | Diferencas | Exemplo principal |
|---|---|---|
| Estado, intencao e plano | 1, 6, 18 | `E01`, `E04` |
| Objetivo atingido e termino | 2, 8, 15 | `E07` |
| Plano, satisfacao e reparo | 3, 4, 7, 16 | `E03`, `E06` |
| Fatos, escopo e estabilidade | 5, 9, 17 | `E05` |
| Cronologia e evidencia bruta | 10, 11, 13 | `E02` |
| Custo | 14 | `E08` |
| Sintese/cautela | 12, 19 | slide interpretativo, sem snippet proprio |

## Como Usar

Cada arquivo `E0X` contem:

- diferencas cobertas;
- task usada;
- caminhos e linhas de origem;
- trecho BDI;
- trecho Codex;
- trecho OpenCode;
- takeaway para o slide.

Os trechos foram reformatados para print screen. Para auditoria, conferir os caminhos e linhas indicados no topo de cada arquivo.
