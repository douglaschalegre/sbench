# SBench — interface do experimento

Frontend independente para conduzir o experimento de auditabilidade em quadrado latino. Os dados ficam apenas no navegador e podem ser exportados em JSON.

## Executar

```bash
corepack npm install
npm run prepare-data
npm run dev
```

O script `prepare-data` cria um catálogo estático em `public/data` a partir de `../runs`. Essa pasta é gerada e não é versionada.

## Produção

```bash
npm run build
npm run preview
```

O resultado em `dist/` é totalmente estático. Publique a pasta junto com os logs gerados ou execute `prepare-data` antes de cada build.

## Privacidade e coleta

- Nenhuma resposta é enviada pela rede.
- O progresso é salvo em `localStorage` no dispositivo.
- Ao final, o participante baixa um arquivo JSON para entrega ao pesquisador.
- Identifique participantes com códigos pseudônimos, nunca com nome ou e-mail.
