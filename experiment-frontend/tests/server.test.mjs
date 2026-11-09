import assert from 'node:assert/strict'
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, test } from 'node:test'
import { execFileSync } from 'node:child_process'
import { mkdirSync, writeFileSync } from 'node:fs'
import { createExperimentServer, openDatabase, migrate, saveSession } from '../server.mjs'
import { randomBytes } from 'node:crypto'
import { createServer } from 'node:http'
import { authenticateAdmin } from '../admin.mjs'
import { createInvitation, hash } from '../access.mjs'

const databases = []
afterEach(() => { while (databases.length) databases.pop().close() })

function payload(sessionId = 'session-1') {
  const traceIds = Array.from({ length: 3 }, (_, index) => `trace-${index + 1}`)
  const traceResponses = Object.fromEntries(traceIds.map((traceId, index) => [traceId, { traceId, startedAt: '2026-01-01T00:00:00Z', completedAt: '2026-01-01T00:01:00Z', evidenceInteractions: 1, positionChanges: 2, evidenceReferences: [{ id: `ref-${index}`, startLine: 1, endLine: 3, addedAt: '2026-01-01T00:00:10Z', deltaMs: 10000 }], telemetry: [{ type: 'line_selection', at: '2026-01-01T00:00:05Z', deltaMs: 5000, detail: { line: 1 } }], confidence: 4, difficulty: 2, ease: 5, directness: 'direct', notes: '' }]))
  return { schemaVersion: 4, exportedAt: '2026-01-01T00:03:00Z', experiment: 'sbench-latin-square-q1-q4', session: { sessionId, participantCode: 'P-001', group: 1, repetition: 'r1', taskSet: Array.from({ length: 3 }, (_, index) => `task-${index}`), startedAt: '2026-01-01T00:00:00Z', completedAt: '2026-01-01T00:03:00Z', currentIndex: 3, traceResponses }, traces: traceIds.map((id, index) => ({ id, runId: 'run', task: `task-${index}`, harness: 'bdi', repetition: 'r1', model: 'model', status: 'ok' })), derivedMetrics: Object.fromEntries(traceIds.map((id) => [id, { m1_1_firstEvidenceDeltaMs: 10000 }])) }
}

test('saves a normalized session idempotently', async () => {
  const database = await openDatabase(':memory:'); databases.push(database); await migrate(database)
  const data = payload()
  await saveSession(database, data)
  data.session.traceResponses['trace-1'].notes = 'updated'
  await saveSession(database, data)
  assert.equal((await database.execute('SELECT COUNT(*) count FROM experiment_sessions')).rows[0].count, 1)
  assert.equal((await database.execute('SELECT COUNT(*) count FROM trace_responses')).rows[0].count, 3)
  assert.equal((await database.execute('SELECT COUNT(*) count FROM evidence_references')).rows[0].count, 3)
  assert.equal((await database.execute('SELECT COUNT(*) count FROM telemetry_events')).rows[0].count, 3)
  assert.equal((await database.execute("SELECT notes FROM trace_responses WHERE trace_id='trace-1'")).rows[0].notes, 'updated')
})

test('accepts an existing three-trace session', async () => {
  const database = await openDatabase(':memory:'); databases.push(database); await migrate(database)
  const data = payload('legacy-session')
  data.session.group = 1
  data.session.taskSet = data.session.taskSet.slice(0, 3)
  data.session.currentIndex = 3
  data.traces = data.traces.slice(0, 3)
  data.session.traceResponses = Object.fromEntries(Object.entries(data.session.traceResponses).slice(0, 3))
  await saveSession(database, data)
  assert.equal((await database.execute('SELECT COUNT(*) count FROM trace_responses')).rows[0].count, 3)
})

test('accepts a completed trace without references when marked as not found', async () => {
  const database = await openDatabase(':memory:'); databases.push(database); await migrate(database)
  const data = payload()
  data.session.traceResponses['trace-1'].evidenceReferences = []
  data.session.traceResponses['trace-1'].noReferencesFound = true
  data.derivedMetrics['trace-1'].m1_1_noReferencesFound = true
  await saveSession(database, data)
  assert.equal((await database.execute('SELECT COUNT(*) count FROM trace_responses')).rows[0].count, 3)
  assert.equal((await database.execute('SELECT COUNT(*) count FROM evidence_references')).rows[0].count, 2)
  const saved = JSON.parse((await database.execute('SELECT payload_json FROM experiment_sessions')).rows[0].payload_json)
  assert.equal(saved.session.traceResponses['trace-1'].noReferencesFound, true)
})

test('rejects a trace without a reference or a not-found answer', async () => {
  const database = await openDatabase(':memory:'); databases.push(database); await migrate(database)
  const data = payload()
  data.session.traceResponses['trace-1'].evidenceReferences = []
  await assert.rejects(() => saveSession(database, data), /referência ou resposta/)
})

test('rejects incomplete sessions', async () => {
  const database = await openDatabase(':memory:'); databases.push(database); await migrate(database)
  const data = payload(); delete data.session.traceResponses['trace-3']
  await assert.rejects(() => saveSession(database, data), /três tarefas/)
})

async function setup(options = {}) {
  const database = await openDatabase(':memory:'); databases.push(database); await migrate(database)
  const data = payload()
  const traces = data.traces.map((entry, index) => ({ ...entry, harness: ['bdi', 'codex', 'opencode'][index] }))
  await database.batch(traces.map((entry) => ({ sql: 'INSERT INTO trace_catalog VALUES (?, ?, ?)', args: [entry.id, JSON.stringify(entry), 'private log'] })), 'write')
  const config = { participantCode: 'P-001', group: 1, runId: 'run', repetition: 'r1', taskSet: data.session.taskSet, expiresAt: new Date(Date.now() + 86400_000).toISOString() }
  const invite = await createInvitation(database, config)
  const server = createExperimentServer({ database, staticDirectory: new URL('..', import.meta.url).pathname, appOrigin: 'https://experiment.example', ...options })
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve))
  const base = `http://127.0.0.1:${server.address().port}`
  return { database, data, invite, config, base, server }
}

async function authorized(base, code) {
  const response = await fetch(`${base}/api/access`, { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: 'https://experiment.example' }, body: JSON.stringify({ code }) })
  return { response, cookie: response.headers.get('set-cookie')?.split(';')[0], result: await response.json() }
}

test('authentication binds completed sessions and private traces to the invitation', async () => {
  const { database, data, invite, base, server } = await setup()
  try {
    for (const path of ['/api/access', '/api/manifest', '/api/traces/trace-1']) assert.equal((await fetch(base + path)).status, 401)
    assert.equal((await fetch(base + '/data/manifest.json')).status, 404)
    assert.equal((await authorized(base, 'wrong')).response.status, 401)
    const { response, cookie, result } = await authorized(base, invite.code)
    assert.equal(response.status, 200)
    assert.match(response.headers.get('set-cookie'), /HttpOnly; SameSite=Strict/)
    assert.match(response.headers.get('set-cookie'), /Secure/)
    assert.equal(result.session.sessionId, invite.sessionId)
    assert.equal(result.session.group, 1)
    const stored = (await database.execute('SELECT * FROM experiment_invitations')).rows[0]
    assert.notEqual(stored.code_hash, invite.code)
    assert.equal(stored.code_hash, hash(invite.code))
    const manifest = await fetch(base + '/api/manifest', { headers: { cookie } })
    assert.equal(manifest.headers.get('cache-control'), 'private, no-store')
    assert.equal((await manifest.json()).entries.length, 3)
    assert.equal((await fetch(base + '/api/traces/unassigned', { headers: { cookie } })).status, 403)
    assert.equal(await (await fetch(base + '/api/traces/trace-1', { headers: { cookie } })).text(), 'private log')
    data.session = { ...result.session, currentIndex: 3, traceResponses: data.session.traceResponses, completedAt: data.session.completedAt }
    const save = () => fetch(base + '/api/experiment-sessions', { method: 'POST', headers: { cookie, 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
    for (const [key, value] of Object.entries({ participantCode: 'P-OTHER', sessionId: 'other', group: 2, runId: 'other', repetition: 'r2', taskSet: ['x', 'y', 'z'], startedAt: 'other' })) {
      const original = data.session[key]; data.session[key] = value
      assert.equal((await save()).status, 400, key)
      data.session[key] = original
    }
    const originalId = data.traces[0].id; data.traces[0].id = 'unassigned'
    assert.equal((await save()).status, 400)
    data.traces[0].id = originalId
    assert.equal((await save()).status, 201)
    assert.equal((await save()).status, 201)
    assert.equal((await database.execute('SELECT COUNT(*) count FROM experiment_sessions')).rows[0].count, 1)
    const restored = await (await fetch(base + '/api/access', { headers: { cookie } })).json()
    assert.equal(restored.completedSession.sessionId, invite.sessionId)
    const again = await authorized(base, invite.code)
    assert.equal(again.result.session.startedAt, result.session.startedAt)
    const csrf = await fetch(base + '/api/access', { method: 'POST', headers: { Origin: 'https://evil.example', 'Content-Type': 'application/json' }, body: JSON.stringify({ code: invite.code }) })
    assert.equal(csrf.status, 403)
    assert.equal((await fetch(base + '/api/logout', { method: 'POST', headers: { cookie } })).status, 200)
    assert.equal((await fetch(base + '/api/access', { headers: { cookie } })).status, 401)
    const another = await authorized(base, invite.code)
    await database.execute({ sql: 'UPDATE experiment_invitations SET revoked_at = ? WHERE invitation_id = ?', args: [new Date().toISOString(), invite.invitationId] })
    assert.equal((await fetch(base + '/api/manifest', { headers: { cookie: another.cookie } })).status, 401)
    assert.equal((await authorized(base, invite.code)).response.status, 401)
  } finally { await new Promise((resolve) => server.close(resolve)) }
})

test('expired codes and access sessions cannot authenticate', async () => {
  const { database, invite, base, server } = await setup()
  try {
    const { cookie } = await authorized(base, invite.code)
    await database.execute("UPDATE access_sessions SET expires_at = '2000-01-01T00:00:00Z'")
    assert.equal((await fetch(base + '/api/access', { headers: { cookie } })).status, 401)
    await database.execute("UPDATE experiment_invitations SET expires_at = '2000-01-01T00:00:00Z'")
    assert.equal((await authorized(base, invite.code)).response.status, 401)
  } finally { await new Promise((resolve) => server.close(resolve)) }
})

test('invitations validate the Latin square against the imported catalog', async () => {
  const { database, config, server } = await setup()
  try {
    await assert.rejects(() => createInvitation(database, { ...config, group: 2 }), /exatamente um trace/)
    await assert.rejects(() => createInvitation(database, { ...config, group: 7 }), /Configuração inválida/)
    await assert.rejects(() => createInvitation(database, { ...config, taskSet: ['same', 'same', 'same'] }), /Configuração inválida/)
  } finally { await new Promise((resolve) => server.close(resolve)) }
})

test('migration preserves existing SQLite sessions and can run twice', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'sbench-experiment-'))
  const path = join(directory, 'experiment.sqlite')
  try {
    const database = await openDatabase(path); databases.push(database)
    await migrate(database)
    await saveSession(database, payload('existing'))
    await migrate(database); await migrate(database)
    assert.equal((await database.execute('SELECT session_id FROM experiment_sessions')).rows[0].session_id, 'existing')
    assert.deepEqual((await database.execute('PRAGMA foreign_key_check')).rows, [])
    const invalid = payload('invalid'); invalid.session.group = 7
    await assert.rejects(() => saveSession(database, invalid), /participante inválido/)
  } finally { while (databases.length) databases.pop().close(); rmSync(directory, { recursive: true, force: true }) }
})

test('researcher CLI migrates, imports, creates and revokes an invitation', () => {
  const directory = mkdtempSync(join(tmpdir(), 'sbench-cli-'))
  const databasePath = join(directory, 'test.sqlite')
  const cli = new URL('../scripts/experiment.mjs', import.meta.url)
  const run = (...args) => execFileSync(process.execPath, [cli.pathname, ...args, '--database', databasePath], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] })
  try {
    mkdirSync(join(directory, 'logs'))
    writeFileSync(join(directory, 'logs', 'trace.log'), 'private log')
    const data = payload()
    const entries = data.traces.map((entry, index) => ({ ...entry, harness: ['bdi', 'codex', 'opencode'][index], url: '/data/logs/trace.log' }))
    const manifestPath = join(directory, 'manifest.json')
    writeFileSync(manifestPath, JSON.stringify({ entries }))
    const configPath = join(directory, 'invitation.json')
    writeFileSync(configPath, JSON.stringify({ participantCode: 'P-CLI', group: 1, runId: 'run', repetition: 'r1', taskSet: data.session.taskSet, expiresAt: new Date(Date.now() + 86400_000).toISOString() }))
    run('migrate'); run('migrate')
    run('import', manifestPath); run('import', manifestPath)
    const invitation = JSON.parse(run('invite', configPath))
    assert.equal(invitation.code.length, 32)
    assert.ok(invitation.sessionId)
    assert.match(run('revoke', invitation.invitationId), /revogado/)
    writeFileSync(join(directory, 'logs', 'trace.log'), 'changed')
    assert.throws(() => run('import', manifestPath), /conteúdo diferente/)
  } finally { rmSync(directory, { recursive: true, force: true }) }
})


test('admin password protects all invitation operations and participant access stays separate', async () => {
  const password = randomBytes(32).toString('base64url')
  const { database, base, server, config, invite } = await setup({ adminPassword: password })
  const request = (path, method = 'GET', value, cookie, origin = 'https://experiment.example') => fetch(base + '/api/admin/' + path, {
    method, headers: { 'Content-Type': 'application/json', Origin: origin, ...(cookie ? { cookie } : {}) },
    body: value === undefined ? undefined : JSON.stringify(value),
  })
  try {
    for (const path of ['/setup', '/setup/']) assert.equal((await fetch(base + path)).status, 200)
    const participant = await authorized(base, invite.code)
    for (const cookie of [undefined, participant.cookie]) {
      for (const [path, method, value] of [
        ['session', 'GET'], ['catalog', 'GET'], ['invitations', 'GET'], ['invitations', 'POST', config],
        [`invitations/${invite.invitationId}`, 'PATCH', config], [`invitations/${invite.invitationId}`, 'DELETE'],
        [`invitations/${invite.invitationId}/revoke`, 'POST'], [`invitations/${invite.invitationId}/rotate-code`, 'POST'],
      ]) assert.equal((await request(path, method, value, cookie)).status, 401, `${method} ${path}`)
    }
    assert.equal((await request('login', 'POST', { password: 'wrong' })).status, 401)
    assert.equal((await request('login', 'POST', {})).status, 401)
    const login = await request('login', 'POST', { password })
    assert.equal(login.status, 200)
    assert.match(login.headers.get('set-cookie'), /HttpOnly; SameSite=Strict; Path=\/api\/admin; Max-Age=28800; Secure/)
    const cookie = login.headers.get('set-cookie').split(';')[0]
    const stored = (await database.execute('SELECT * FROM admin_sessions')).rows[0]
    assert.notEqual(stored.token_hash, cookie.split('=')[1])
    assert.notEqual(stored.password_hash, password)
    assert.equal((await request('session', 'GET', undefined, cookie)).status, 200)
    assert.equal((await fetch(base + '/api/access', { headers: { cookie } })).status, 401)
    assert.equal((await (await request('catalog', 'GET', undefined, cookie)).json()).entries.length, 3)
    const createdResponse = await request('invitations', 'POST', { ...config, participantCode: 'P-ADMIN' }, cookie)
    assert.equal(createdResponse.status, 201)
    const created = await createdResponse.json()
    const path = `invitations/${created.invitationId}`
    let list = await (await request('invitations', 'GET', undefined, cookie)).json()
    const listed = list.invitations.find((entry) => entry.invitationId === created.invitationId)
    assert.equal(listed.participantCode, 'P-ADMIN')
    for (const field of ['code', 'code_hash', 'password_hash', 'token_hash']) assert.equal(Object.hasOwn(listed, field), false)
    assert.equal((await request(path, 'PATCH', { ...config, participantCode: 'P-EDITED' }, cookie)).status, 200)
    assert.equal((await request(path, 'PATCH', { ...config, group: 7 }, cookie)).status, 400)
    assert.equal((await request(path, 'PATCH', { ...config, group: 2 }, cookie)).status, 400)
    for (const [route, method, value] of [['invitations', 'POST', config], [path, 'PATCH', config], [path, 'DELETE'], [path + '/revoke', 'POST']]) {
      assert.equal((await request(route, method, value, cookie, 'https://evil.example')).status, 403)
    }
    const rotated = await (await request(path + '/rotate-code', 'POST', undefined, cookie)).json()
    assert.notEqual(rotated.code, created.code)
    assert.equal((await authorized(base, created.code)).response.status, 401)
    const access = await authorized(base, rotated.code)
    assert.equal(access.response.status, 200)
    assert.equal(access.result.session.participantCode, 'P-EDITED')
    assert.equal((await request(path, 'PATCH', config, cookie)).status, 409)
    assert.equal((await request(path, 'DELETE', undefined, cookie)).status, 409)
    assert.equal((await request(path + '/rotate-code', 'POST', undefined, cookie)).status, 409)
    assert.equal((await request(path + '/revoke', 'POST', undefined, cookie)).status, 200)
    assert.equal((await fetch(base + '/api/access', { headers: { cookie: access.cookie } })).status, 401)
    const unused = await (await request('invitations', 'POST', config, cookie)).json()
    assert.equal((await request(`invitations/${unused.invitationId}`, 'DELETE', undefined, cookie)).status, 200)
    assert.equal((await authorized(base, unused.code)).response.status, 401)
    assert.equal((await request(`invitations/${unused.invitationId}`, 'DELETE', undefined, cookie)).status, 404)
    list = await (await request('invitations', 'GET', undefined, cookie)).json()
    assert.equal(list.invitations.length, 2)
    assert.equal(list.invitations.find((entry) => entry.invitationId === created.invitationId).revokedAt !== null, true)
    assert.equal(await authenticateAdmin(database, cookie, 'changed-password'), false)
    assert.equal((await request('logout', 'POST', undefined, cookie)).status, 200)
    assert.equal((await request('session', 'GET', undefined, cookie)).status, 401)
    const anotherLogin = await request('login', 'POST', { password })
    const anotherCookie = anotherLogin.headers.get('set-cookie').split(';')[0]
    await database.execute("UPDATE admin_sessions SET expires_at = '2000-01-01T00:00:00Z'")
    assert.equal((await request('invitations', 'GET', undefined, anotherCookie)).status, 401)
  } finally { await new Promise((resolve) => server.close(resolve)) }
})

test('admin access fails closed when no password is configured', async () => {
  const { base, server } = await setup({ adminPassword: '' })
  try {
    assert.equal((await fetch(base + '/api/admin/invitations')).status, 503)
    assert.equal((await fetch(base + '/api/admin/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ password: 'anything' }) })).status, 503)
  } finally { await new Promise((resolve) => server.close(resolve)) }
})


test('Vercel entrypoint initializes an empty database before serving concurrent requests', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'sbench-vercel-'))
  const path = join(directory, 'test.sqlite')
  const previousUrl = process.env.TURSO_DATABASE_URL
  const previousPassword = process.env.ADMIN_PASSWORD
  const previousOrigin = process.env.APP_ORIGIN
  const password = randomBytes(32).toString('base64url')
  process.env.TURSO_DATABASE_URL = `file:${path}`
  process.env.ADMIN_PASSWORD = password
  process.env.APP_ORIGIN = 'https://experiment.example'
  const { default: api } = await import('../api/index.js')
  const server = createServer(api)
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve))
  try {
    const base = `http://127.0.0.1:${server.address().port}`
    const responses = await Promise.all([fetch(base + '/api/health'), fetch(base + '/api?route=admin/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ password }) })])
    assert.equal(responses[0].status, 200)
    assert.equal(responses[1].status, 200)
    const cookie = responses[1].headers.get('set-cookie').split(';')[0]
    assert.equal((await fetch(base + '/api?route=admin/session', { headers: { cookie } })).status, 200)
    assert.equal((await fetch(base + '/api?route=admin/invitations', { headers: { cookie } })).status, 200)
    const database = await openDatabase(path)
    assert.equal((await database.execute('SELECT COUNT(*) count FROM admin_sessions')).rows[0].count, 1)
    database.close()
  } finally {
    await new Promise((resolve) => server.close(resolve))
    for (const [name, value] of [['TURSO_DATABASE_URL', previousUrl], ['ADMIN_PASSWORD', previousPassword], ['APP_ORIGIN', previousOrigin]]) {
      if (value === undefined) delete process.env[name]; else process.env[name] = value
    }
    rmSync(directory, { recursive: true, force: true })
  }
})
