# SBench — interface do experimento

Módulo independente para conduzir o experimento de auditabilidade. Cada um dos sete grupos avalia as sete atividades; a ordem dos frameworks segue a rotação BDI → Codex → OpenCode, com deslocamento conforme o grupo (os grupos 4–7 repetem o ciclo). O progresso fica no navegador e sessões concluídas são persistidas em SQLite.

## Executar

```bash
corepack npm install
npm run prepare-data
npm run dev
```

Em outro terminal, inicie a API local:

```bash
npm run server
```

No desenvolvimento, o Vite encaminha `/api` para `http://127.0.0.1:8765`.

O script `prepare-data` cria um catálogo estático em `public/data` a partir de `../runs`. Essa pasta é gerada e não é versionada.

## Produção

```bash
npm run build
npm run server
```

O servidor Node entrega `dist/`, recebe sessões concluídas em `POST /api/experiment-sessions` e cria `experiment.sqlite` nesta pasta. É possível alterar o arquivo com `node server.mjs --database caminho/experimento.sqlite`.

## Privacidade e coleta

- O progresso é salvo em `localStorage` no dispositivo.
- Ao final, a sessão é enviada à API e gravada de forma idempotente no SQLite.
- O JSON pode ser baixado como cópia de segurança se a API estiver indisponível.
- Identifique participantes com códigos pseudônimos, nunca com nome ou e-mail.

## Schema SQLite

- `experiment_sessions`: metadados e payload JSON integral.
- `trace_responses`: respostas e métricas principais de cada trace.
- `evidence_references`: intervalos de linhas selecionados como evidência.
- `telemetry_events`: sequência completa de interações da interface.
