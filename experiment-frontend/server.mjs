import { createServer } from 'node:http'
import { readFile } from 'node:fs/promises'
import { extname, resolve, sep } from 'node:path'
import { fileURLToPath } from 'node:url'
import { openDatabase, migrate, saveSession } from './database.mjs'
import { assignedSession, authenticate, createInvitation, hash, login, validateAssignment } from './access.mjs'
import { adminLogin, adminToken, authenticateAdmin, listInvitations, updateInvitation, deleteInvitation, rotateInvitationCode, revokeInvitation } from './admin.mjs'
export { openDatabase, migrate, saveSession } from './database.mjs'

const root = fileURLToPath(new URL('.', import.meta.url))

function sendJson(response, status, value) {
  response.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' })
  response.end(JSON.stringify(value))
}

async function body(request) {
  // Below Vercel's request limit; oversized exports remain downloadable in the UI.
  if (request.body !== undefined) {
    if (Buffer.byteLength(JSON.stringify(request.body)) > 4_000_000) throw new Error('Payload excede 4 MB.')
    return typeof request.body === 'string' ? JSON.parse(request.body) : request.body
  }
  let size = 0
  const chunks = []
  for await (const chunk of request) {
    size += chunk.length
    if (size > 4_000_000) throw new Error('Payload excede 4 MB.')
    chunks.push(chunk)
  }
  return JSON.parse(Buffer.concat(chunks).toString('utf8'))
}

export function createApiHandler({ database, appOrigin = process.env.APP_ORIGIN, adminPassword = process.env.ADMIN_PASSWORD }) {
  if (process.env.VERCEL && (!appOrigin || new URL(appOrigin).protocol !== 'https:')) throw new Error('Configure APP_ORIGIN com a origem HTTPS do experimento.')
  const allowedOrigin = new URL(appOrigin ?? 'http://127.0.0.1:4173').origin
  return async (request, response) => {
    response.setHeader('Cache-Control', 'private, no-store')
    response.setHeader('X-Content-Type-Options', 'nosniff')
    const pathname = new URL(request.url, 'http://localhost').pathname
    if (!['GET', 'HEAD', 'OPTIONS'].includes(request.method) && request.headers.origin && request.headers.origin !== allowedOrigin) return sendJson(response, 403, { error: 'Origem não permitida.' })
    try {
      if (request.method === 'GET' && pathname === '/api/health') return sendJson(response, 200, { status: 'ok' })
      if (request.method === 'POST' && pathname === '/api/access') {
        const result = await login(database, (await body(request))?.code)
        if (!result) return sendJson(response, 401, { error: 'Código inválido ou expirado.' })
        const secure = allowedOrigin.startsWith('https://') ? '; Secure' : ''
        response.setHeader('Set-Cookie', `sbench_access=${result.token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=${Math.floor((Date.parse(result.expiresAt) - Date.now()) / 1000)}${secure}`)
        return sendJson(response, 200, { session: assignedSession(result.invitation) })
      }
      if (pathname.startsWith('/api/admin/')) {
        if (!adminPassword) return sendJson(response, 503, { error: 'Acesso administrativo indisponível. Configure ADMIN_PASSWORD no servidor.' })
        const secure = allowedOrigin.startsWith('https://') ? '; Secure' : ''
        if (pathname === '/api/admin/login' && request.method === 'POST') {
          const result = await adminLogin(database, (await body(request))?.password, adminPassword)
          if (!result) return sendJson(response, 401, { error: 'Senha inválida.' })
          response.setHeader('Set-Cookie', `sbench_admin=${result.token}; HttpOnly; SameSite=Strict; Path=/api/admin; Max-Age=28800${secure}`)
          return sendJson(response, 200, { authenticated: true })
        }
        if (!await authenticateAdmin(database, request.headers.cookie, adminPassword)) return sendJson(response, 401, { error: 'Entre como administrador para continuar.' })
        if (pathname === '/api/admin/session' && request.method === 'GET') return sendJson(response, 200, { authenticated: true })
        if (pathname === '/api/admin/logout' && request.method === 'POST') {
          await database.execute({ sql: 'DELETE FROM admin_sessions WHERE token_hash = ?', args: [hash(adminToken(request.headers.cookie))] })
          response.setHeader('Set-Cookie', `sbench_admin=; HttpOnly; SameSite=Strict; Path=/api/admin; Max-Age=0${secure}`)
          return sendJson(response, 200, { authenticated: false })
        }
        if (pathname === '/api/admin/catalog' && request.method === 'GET') {
          const { rows } = await database.execute('SELECT metadata_json FROM trace_catalog')
          return sendJson(response, 200, { entries: rows.map((row) => JSON.parse(row.metadata_json)) })
        }
        if (pathname === '/api/admin/invitations' && request.method === 'GET') return sendJson(response, 200, { invitations: await listInvitations(database) })
        if (pathname === '/api/admin/invitations' && request.method === 'POST') return sendJson(response, 201, await createInvitation(database, await body(request)))
        const match = pathname.match(/^\/api\/admin\/invitations\/([^/]+)(?:\/(revoke|rotate-code))?$/)
        if (match) {
          const id = decodeURIComponent(match[1])
          if (!match[2] && request.method === 'PATCH') return sendJson(response, 200, await updateInvitation(database, id, await body(request)))
          if (!match[2] && request.method === 'DELETE') return sendJson(response, 200, await deleteInvitation(database, id))
          if (match[2] === 'revoke' && request.method === 'POST') return sendJson(response, 200, await revokeInvitation(database, id))
          if (match[2] === 'rotate-code' && request.method === 'POST') return sendJson(response, 200, await rotateInvitationCode(database, id))
        }
        return sendJson(response, 404, { error: 'not found' })
      }
      const invitation = await authenticate(database, request.headers.cookie)
      if (!invitation) return sendJson(response, 401, { error: 'Informe seu código de acesso para continuar.' })
      if (request.method === 'POST' && pathname === '/api/logout') {
        const token = request.headers.cookie.split(';').map((part) => part.trim()).find((part) => part.startsWith('sbench_access='))?.slice(14)
        await database.execute({ sql: 'DELETE FROM access_sessions WHERE token_hash = ?', args: [hash(token)] })
        response.setHeader('Set-Cookie', 'sbench_access=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0')
        return sendJson(response, 200, { saved: true })
      }
      if (request.method === 'GET' && pathname === '/api/access') {
        const { rows } = await database.execute({ sql: 'SELECT payload_json FROM experiment_sessions WHERE session_id = ?', args: [invitation.session_id] })
        return sendJson(response, 200, { session: assignedSession(invitation), completedSession: rows[0] ? JSON.parse(rows[0].payload_json).session : null })
      }
      const traces = JSON.parse(invitation.traces_json)
      if (request.method === 'GET' && pathname === '/api/manifest') return sendJson(response, 200, { generatedAt: invitation.created_at, entries: traces.map((entry) => ({ ...entry, url: `/api/traces/${encodeURIComponent(entry.id)}` })) })
      if (request.method === 'GET' && pathname.startsWith('/api/traces/')) {
        const id = decodeURIComponent(pathname.slice('/api/traces/'.length))
        if (!traces.some((entry) => entry.id === id)) return sendJson(response, 403, { error: 'Trace não atribuído a este participante.' })
        const { rows } = await database.execute({ sql: 'SELECT content FROM trace_catalog WHERE trace_id = ?', args: [id] })
        if (!rows[0]) return sendJson(response, 404, { error: 'Trace não encontrado.' })
        response.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' })
        return response.end(rows[0].content)
      }
      if (request.method === 'POST' && pathname === '/api/experiment-sessions') {
        const payload = await body(request)
        validateAssignment(invitation, payload)
        const sessionId = await saveSession(database, payload)
        return sendJson(response, 201, { sessionId, saved: true })
      }
      return sendJson(response, 404, { error: 'not found' })
    } catch (error) {
      if (error?.status) return sendJson(response, error.status, { error: error.message })
      if (error instanceof SyntaxError || error?.code?.startsWith('SQLITE_CONSTRAINT') || !error?.code) return sendJson(response, 400, { error: error instanceof Error ? error.message : 'Payload inválido.' })
      console.error('Experiment API failure:', error.code)
      return sendJson(response, 503, { error: 'Não foi possível acessar o banco. Tente novamente.' })
    }
  }
}

const mimeTypes = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml' }
export function createExperimentServer({ database, staticDirectory, appOrigin, adminPassword }) {
  const api = createApiHandler({ database, appOrigin, adminPassword })
  return createServer(async (request, response) => {
    if (request.url?.startsWith('/api/')) return api(request, response)
    if (request.method !== 'GET') return sendJson(response, 404, { error: 'not found' })
    try {
      const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname)
      // Private source files and the former public catalog are never served.
      if (pathname.startsWith('/data/') || pathname === '/data') return sendJson(response, 404, { error: 'not found' })
      const file = resolve(staticDirectory, '.' + (['/', '/setup', '/setup/'].includes(pathname) ? '/index.html' : pathname))
      if (!file.startsWith(resolve(staticDirectory) + sep)) return sendJson(response, 403, { error: 'forbidden' })
      const content = await readFile(file)
      response.writeHead(200, { 'Content-Type': mimeTypes[extname(file)] ?? 'application/octet-stream' })
      response.end(content)
    } catch { sendJson(response, 404, { error: 'not found' }) }
  })
}

function option(name, fallback) {
  const index = process.argv.indexOf(name)
  return index < 0 ? fallback : process.argv[index + 1]
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const port = Number(option('--port', '8765'))
  const host = option('--host', '127.0.0.1')
  const database = await openDatabase(option('--database', undefined))
  await migrate(database)
  createExperimentServer({ database, staticDirectory: resolve(option('--static', resolve(root, 'dist'))) }).listen(port, host, () => console.log(`Experiment server: http://${host}:${port}`))
}
