# Figuras contendo somente logs

As quatro figuras foram refeitas para conter exclusivamente logs, sem títulos, legendas, explicações, numeração de linhas ou diagramas. A identificação da harness deve ficar na legenda do artigo, fora da imagem.

- `01-codex-log`: inspeção dos arquivos gerados e término do turno.
- `02-opencode-log`: checklist concluído e término do step.
- `03-bdi-log`: plano concluído, objetivo pendente, segundo ciclo e objetivo atingido.
- `04-bdi-log-dark`: mesmo trecho BDI em fundo escuro.

Cada figura tem fontes HTML e TXT, PNG em resolução dupla e PDF com texto vetorial. Para o artigo, prefira os PDFs de fundo branco. O fundo escuro é uma alternativa para apresentação.

Os JSONs foram indentados para leitura. Codex, linha 38, e os eventos OpenCode usam uma seleção dos campos originais, preservando hierarquia e valores. O evento final Codex está completo. Os trechos BDI são literais. Linhas omitidas entre trechos são separadas por espaço em branco, sem marcadores acrescentados. `provenance.json` identifica as fontes, os hashes e as linhas selecionadas.

A figura BDI mostra recuperação de um plano insuficiente, que apenas inspecionou os arquivos. Esse trecho não demonstra uma atualização externa tardia como causa do segundo ciclo. O estado achieved é uma avaliação do runtime. Os exemplos não estabelecem superioridade de correção em relação às outras harnesses.

Regeneração:

```sh
python3 artifacts/article-traces/generate.py
node artifacts/article-traces/export.mjs /caminho/para/playwright/index.mjs
```

O argumento pode ser omitido se playwright estiver instalado no ambiente Node. O exportador usa Google Chrome instalado e verifica overflow em 1100 e 390 pixels. Edite o gerador para refinar os arquivos sem perder mudanças na regeneração.
