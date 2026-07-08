# Catalogo de Evidencias

Fonte comum:

- `run_id`: `20260615T221949Z`
- repeticao: `r3`
- raiz dos logs: `/Users/douglas/code/masters/sbench/runs/20260615T221949Z/entries`

## Diferencas Sintetizadas

| # | Diferenca sintetizada | Snippet | Task | Ideia central |
|---:|---|---|---|---|
| 1 | Estado e compromisso da execucao | `E01_estado_e_compromisso_da_execucao.md` | `incident_staffing_plan` | O BDI explicita estado, objetivo, intencao e plano ativo; Codex/OpenCode registram compromisso por transcript, mensagens ou checklist. |
| 2 | Trilha operacional e evidencia bruta | `E02_trilha_operacional_e_evidencia_bruta.md` | `incident_staffing_plan` | Codex/OpenCode preservam melhor comandos, tools, patches e outputs; BDI resume a acao dentro do ciclo deliberativo. |
| 3 | Reparo, incompletude e replanejamento | `E03_reparo_incompletude_e_replanejamento.md` | `community_workshop_replan` | O BDI mostra plano concluido sem desejo satisfeito e cria nova intencao; Codex/OpenCode evidenciam reparo pela sequencia operacional. |
| 4 | Acompanhamento de progresso | `E04_acompanhamento_de_progresso.md` | `community_workshop_replan` | O BDI acompanha progresso por plano/intencao; OpenCode por checklist; Codex por narrativa e eventos. |
| 5 | Retencao de contexto do prompt | `E05_retencao_de_contexto_do_prompt.md` | `community_workshop_replan` | O BDI mostra contexto retido como crencas reinjetadas nos prompts internos; Codex/OpenCode exigem seguir transcript, leituras, checklist e verificacoes. Isso mede rastreabilidade, nao correcao do contexto. |
| 6 | Criterio de sucesso observado | `E06_criterio_de_sucesso_observado.md` | `incident_staffing_plan` | O BDI registra sucesso semantico de passo/desejo; Codex/OpenCode registram sucesso operacional de comandos/tools/files. |
| 7 | Semantica de termino | `E07_semantica_de_termino.md` | `incident_staffing_plan` | O BDI encerra com `achieved` e estado final; Codex com `turn.completed`; OpenCode com `reason: stop`. |
| 8 | Observabilidade de uso/custo | `E08_observabilidade_do_custo.md` | `incident_staffing_plan` | O BDI permite ver uso/tokens de chamadas deliberativas; Codex agrega por turno; OpenCode distribui por step. Custo monetario exige calculo separado. |

## Rastreabilidade Para as Diferencas Originais

| Diferenca sintetizada | Diferencas originais absorvidas |
|---|---|
| Estado e compromisso da execucao | 1: estado deliberativo; 6: intencao ativa; parte de 18: plano do runtime vs checklist |
| Trilha operacional e evidencia bruta | 10: cronologia de acoes; 13: evidencia bruta vs estado interpretado; parte de 11: progresso operacional |
| Reparo, incompletude e replanejamento | 3: plano concluido vs objetivo satisfeito; 4: replanejamento; 16: auditabilidade de erro; parte de 7: avaliacao semantica |
| Acompanhamento de progresso | 11: progresso operacional; 18: plano do runtime vs checklist; parte de 6: intencao ativa |
| Retencao de contexto do prompt | 5: fatos acumulados; 17: estabilidade de objetivo |
| Criterio de sucesso observado | 7: avaliacao semantica dos passos; 15: tipo de sucesso observado |
| Semantica de termino | 2: objetivos atingidos; 8: termino da execucao; parte de 15: tipo de sucesso observado |
| Observabilidade de uso/custo | 14: granularidade do custo |

## Itens Que Viram Cautela/Sintese

| Item original | Tratamento |
|---|---|
| 12: onde esta a explicacao | Vira interpretacao transversal: BDI concentra explicacao no estado deliberativo; Codex/OpenCode em mensagens, tools e artefatos. |
| 19: confiabilidade do trace | Vira cautela metodologica: mais estrutura observavel nao garante que as crencas ou avaliacoes estejam corretas. |

## Como Usar

Cada arquivo `E0X` contem:

- uma diferenca sintetizada;
- rastreabilidade para as diferencas originais;
- task usada;
- caminhos e linhas de origem;
- trecho BDI;
- trecho Codex;
- trecho OpenCode;
- takeaway para o slide.

Os trechos foram reformatados para print screen. Para auditoria, conferir os caminhos e linhas indicados no topo de cada arquivo.
