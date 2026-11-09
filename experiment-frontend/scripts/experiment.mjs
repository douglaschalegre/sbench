import { readFile, realpath } from 'node:fs/promises'
import { dirname, resolve, sep } from 'node:path'
import { openDatabase, migrate } from '../database.mjs'
import { createInvitation } from '../access.mjs'

const args = process.argv.slice(2)
const databaseIndex = args.indexOf('--database')
const databasePath = databaseIndex < 0 ? undefined : args.splice(databaseIndex, 2)[1]
if (databaseIndex >= 0 && !databasePath) throw new Error('Informe o caminho após --database.')
const [command, input] = args
const database = await openDatabase(databasePath)
try {
  if (command === 'migrate') {
    await migrate(database)
    console.log('Schema atualizado; registros existentes preservados.')
  } else if (command === 'import') {
    const manifestPath = resolve(input)
    const directory = await realpath(dirname(manifestPath))
    const manifest = JSON.parse(await readFile(manifestPath, 'utf8'))
    if (!Array.isArray(manifest.entries) || !manifest.entries.length) throw new Error('Catálogo vazio ou inválido.')
    for (const entry of manifest.entries) {
      if (!entry.id || !entry.url?.startsWith('/data/')) throw new Error('Entrada inválida no catálogo.')
      const path = await realpath(resolve(directory, entry.url.slice('/data/'.length)))
      if (!path.startsWith(directory + sep)) throw new Error('Log fora da pasta do catálogo.')
      const content = await readFile(path, 'utf8')
      const existing = await database.execute({ sql: 'SELECT content, metadata_json FROM trace_catalog WHERE trace_id = ?', args: [entry.id] })
      if (existing.rows[0] && (existing.rows[0].content !== content || existing.rows[0].metadata_json !== JSON.stringify(entry))) throw new Error(`Trace ${entry.id} já existe com conteúdo diferente; use um novo ID.`)
      await database.execute({ sql: 'INSERT INTO trace_catalog VALUES (?, ?, ?) ON CONFLICT(trace_id) DO NOTHING', args: [entry.id, JSON.stringify(entry), content] })
    }
    console.log(`${manifest.entries.length} traces importados.`)
  } else if (command === 'invite') {
    const config = JSON.parse(await readFile(resolve(input), 'utf8'))
    const invitation = await createInvitation(database, config)
    console.log(JSON.stringify({ ...invitation, url: process.env.APP_ORIGIN ?? 'http://127.0.0.1:4173' }, null, 2))
  } else if (command === 'revoke') {
    const result = await database.execute({ sql: 'UPDATE experiment_invitations SET revoked_at = ? WHERE invitation_id = ?', args: [new Date().toISOString(), input] })
    if (!result.rowsAffected) throw new Error('Convite não encontrado.')
    console.log('Convite revogado, incluindo todas as sessões de acesso.')
  } else {
    throw new Error('Uso: experiment.mjs migrate | import manifest.json | invite config.json | revoke invitation-id [--database arquivo.sqlite]')
  }
} finally {
  database.close()
}
