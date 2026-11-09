# SBench: executar o experimento online

Cada convite identifica uma participação e fixa código pseudônimo, posição no quadrado latino, execução, réplica e três tarefas. O participante informa o código antes do tutorial. A API consulta essa configuração no banco e valida as respostas contra ela.

## Preparar o banco

Use Node.js 22.13 ou posterior da série 22 e um banco Turso **libSQL**, compatível com `@libsql/client`. O mesmo cliente permite desenvolvimento com um arquivo SQLite local.

Execute os comandos nesta pasta:

```bash
npm ci
cp .env.example .env
```

Preencha `.env` com as credenciais do Turso e a origem da aplicação:

| Variável | Valor |
| --- | --- |
| `TURSO_DATABASE_URL` | URL `libsql://...` fornecida pelo Turso |
| `TURSO_AUTH_TOKEN` | Token com permissão de leitura e escrita |
| `APP_ORIGIN` | Origem HTTPS do frontend, sem barra final ou caminho |
| `ADMIN_PASSWORD` | Senha de administrador para `/setup` |

Nenhuma dessas variáveis usa o prefixo `VITE_`. O frontend chama `/api` na mesma origem. A API usa um cookie `HttpOnly`, com um token aleatório cujo hash fica no banco, e não precisa de `SESSION_SECRET`.

Crie as tabelas e importe os traces:

```bash
npm run experiment -- migrate
npm run experiment -- import public/data/manifest.json
```

A migração cria tabelas ausentes e preserva os registros existentes. A importação pode ser repetida com o mesmo catálogo. Para alterar um trace já importado, use um novo ID. Catálogo e logs ficam no banco; o build não publica `public/data`.

Para preservar as respostas locais, prepare uma cópia em modo WAL antes do upload. Pare a coleta local durante a transferência para não gerar respostas depois dessa cópia.

```bash
python3 scripts/prepare_turso_upload.py experiment.sqlite experiment.turso.sqlite
```

Importe **`experiment.turso.sqlite`** ao criar o banco libSQL no Turso. O importador exige `journal_mode=WAL`. O script preserva o original, inclui transações pendentes no WAL e executa um checkpoint na cópia para que o arquivo principal contenha todos os dados. Ele recusa sobrescrever um destino existente; para gerar outra cópia, escolha um novo nome.

Confira o número de sessões após a importação. A aplicação não transfere automaticamente as respostas locais para o banco remoto. Referência: [preparação do SQLite para upload no Turso](https://turso.tech/blog/migrating-and-importing-sqlite-to-turso-just-got-easier).

## Gerenciar participantes pela interface

Configure `ADMIN_PASSWORD` nas variáveis de ambiente do servidor. Na Vercel, adicione a senha em Production e faça um novo deploy. Use a senha escolhida para o administrador; não a inclua no frontend nem no repositório.

1. Acesse `https://seu-experimento.vercel.app/setup`.
2. Entre com a senha de administrador.
3. Preencha o código pseudônimo, a posição no quadrado latino, a execução, a réplica, as três tarefas e a validade.
4. Clique em **Criar convite** e copie o endereço e o código para o participante.

A lista permite consultar, editar, revogar e excluir convites. A edição e a exclusão só são permitidas antes do primeiro acesso. Depois dele, revogue o convite para bloquear o acesso e crie outro se precisar mudar a configuração. A exclusão nunca remove respostas de uma participação iniciada.

O código aparece apenas ao ser gerado. Se perdê-lo antes do primeiro acesso, use **Gerar novo código**. O código anterior deixa de funcionar. Ao editar a configuração, o código existente continua válido.

O acesso administrativo dura até oito horas e usa um cookie separado do participante. **Sair do administrador** encerra essa sessão. Alterar `ADMIN_PASSWORD` no servidor invalida as sessões administrativas existentes. Sem essa variável, a API administrativa permanece bloqueada.

Depois de preparar o banco e importar os traces, o cadastro de participantes não exige comandos no servidor. O banco local deste repositório já inclui a tabela `admin_sessions`. A API aplica a migração de forma idempotente ao iniciar na Vercel, inclusive em bancos da versão anterior.

## Cadastrar uma participação pelo terminal

Copie `invitation.example.json` para `invitation.local.json`. Preencha:

- `participantCode`: código pseudônimo, com 3 a 64 letras, números, `_` ou `-`.
- `group`: posição 1, 2 ou 3 no quadrado latino.
- `runId` e `repetition`: execução e réplica presentes no catálogo importado.
- `taskSet`: três tarefas diferentes, na ordem das atividades.
- `expiresAt`: validade do convite em ISO 8601, com fuso horário.

Gere o convite:

```bash
npm run experiment -- invite invitation.local.json
```

O comando verifica a existência dos três traces na ordem do quadrado latino. Ele retorna `invitationId`, `sessionId`, o endereço da aplicação e um código de acesso aleatório. Guarde o código e envie o endereço e o código individualmente ao participante. O banco guarda apenas o hash do código.

O primeiro acesso registra `started_at` e abre uma sessão de acesso de até 12 horas, limitada pela validade do convite. Esse horário inclui o tutorial; os tempos de leitura de cada trace continuam registrados separadamente. O mesmo código volta à mesma participação e mantém o mesmo `sessionId`. Não compartilhe um convite entre participantes.

Para invalidar um convite e todas as suas sessões de acesso:

```bash
npm run experiment -- revoke ID_DO_CONVITE
```

Uma nova tentativa experimental deve receber um novo convite.

## Publicar na Vercel

1. Importe este repositório e configure **Root Directory** como `experiment-frontend`.
2. Use o preset Vite e Node.js 22.x. O `vercel.json` configura o build e a pasta `dist`.
3. Configure `TURSO_DATABASE_URL`, `TURSO_AUTH_TOKEN`, `APP_ORIGIN` e `ADMIN_PASSWORD` no ambiente Production.
4. Execute a migração e a importação usando o mesmo banco antes de distribuir os convites.
5. Faça o deploy. Abra a URL, entre com um convite e confira a participação atribuída.

As rotas de `api/[...path].js` rodam como Vercel Functions. Catálogo, logs e envio de respostas exigem autenticação; a tela de entrada e os arquivos de interface são públicos. Respostas autenticadas usam `Cache-Control: private, no-store`.

Para Preview, use um banco separado e configure `APP_ORIGIN` para a origem HTTPS daquele deployment. A API rejeita POSTs de outras origens.

## Executar localmente

Para usar Turso, mantenha as credenciais em `.env` e defina `APP_ORIGIN=http://127.0.0.1:4173`.

Para usar apenas SQLite local, os comandos administrativos aceitam `--database`:

```bash
npm run experiment -- migrate --database experiment.sqlite
npm run experiment -- import public/data/manifest.json --database experiment.sqlite
npm run experiment -- invite invitation.local.json --database experiment.sqlite
```

Inicie a API e o Vite em terminais separados:

```bash
npm run server -- --database experiment.sqlite
npm run dev
```

O Vite encaminha `/api` para `http://127.0.0.1:8765`. Para usar Turso na API local, omita `--database`.

## Verificar a implementação

```bash
npm run test:server
python3 -m unittest discover -s tests -p 'test_prepare_turso_upload.py'
npm run lint
npm run build
```

Os testes usam SQLite local com o mesmo cliente libSQL. Eles cobrem persistência idempotente, convites inválidos e expirados, revogação, logout, origem do pedido, restrição de traces, tentativa de alterar a atribuição, autenticação administrativa e CRUD de convites.

## Dados coletados

A atribuição e as sessões de acesso ficam no banco desde a entrada. O progresso em andamento fica em `localStorage`, separado por `sessionId`; retome no mesmo navegador. Ao concluir, a API grava as respostas em uma transação. Uma participação já concluída pode ser recuperada do banco em outro navegador.

O JSON continua disponível para download se o envio falhar. O limite de envio da API é 4 MB, abaixo do limite da Vercel. Para uma sessão que exceda esse limite, guarde o JSON e ajuste a coleta antes de continuar o estudo.

As tabelas são:

- `experiment_invitations`: atribuição, hash do código, validade e revogação.
- `access_sessions`: hash dos tokens de acesso dos participantes e expiração.
- `admin_sessions`: hash dos tokens administrativos, vínculo com a senha atual e expiração.
- `trace_catalog`: metadados e texto dos traces privados.
- `experiment_sessions`: metadados e payload JSON das participações concluídas.
- `trace_responses`, `evidence_references` e `telemetry_events`: respostas, evidências e interações normalizadas.

Use códigos pseudônimos. Mantenha cópias de segurança do banco e trate os códigos de convite como credenciais.

Referências: [cliente TypeScript do Turso](https://docs.turso.tech/sdk/ts/reference) e [Node.js na Vercel](https://vercel.com/docs/functions/runtimes/node-js).
