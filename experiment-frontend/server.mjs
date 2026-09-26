import { DatabaseSync } from 'node:sqlite'
import { createServer } from 'node:http'
import { readFileSync, statSync } from 'node:fs'
import { extname, join, normalize, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = fileURLToPath(new URL('.', import.meta.url))
const schema = `
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS experiment_sessions (
  session_id TEXT PRIMARY KEY, participant_code TEXT NOT NULL,
  group_number INTEGER NOT NULL CHECK (group_number BETWEEN 1 AND 3),
  repetition TEXT NOT NULL, task_set_json TEXT NOT NULL, started_at TEXT NOT NULL,
  completed_at TEXT NOT NULL, exported_at TEXT NOT NULL, received_at TEXT NOT NULL,
  experiment TEXT NOT NULL, schema_version INTEGER NOT NULL, payload_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS trace_responses (
  session_id TEXT NOT NULL REFERENCES experiment_sessions(session_id) ON DELETE CASCADE,
  trace_id TEXT NOT NULL, sequence_index INTEGER NOT NULL, run_id TEXT, task TEXT NOT NULL,
  harness TEXT NOT NULL, repetition TEXT NOT NULL, model TEXT, status TEXT,
  started_at TEXT NOT NULL, reading_completed_at TEXT, completed_at TEXT NOT NULL,
  first_evidence_at TEXT, confidence INTEGER, cognitive_load INTEGER, ease INTEGER,
  directness TEXT, notes TEXT NOT NULL DEFAULT '', evidence_interactions INTEGER NOT NULL DEFAULT 0,
  position_changes INTEGER NOT NULL DEFAULT 0, derived_metrics_json TEXT NOT NULL,
  PRIMARY KEY (session_id, trace_id)
);
CREATE TABLE IF NOT EXISTS evidence_references (
  reference_id TEXT NOT NULL, session_id TEXT NOT NULL, trace_id TEXT NOT NULL,
  start_line INTEGER NOT NULL, end_line INTEGER NOT NULL, added_at TEXT NOT NULL, delta_ms INTEGER NOT NULL,
  PRIMARY KEY (session_id, trace_id, reference_id),
  FOREIGN KEY (session_id, trace_id) REFERENCES trace_responses(session_id, trace_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS telemetry_events (
  session_id TEXT NOT NULL, trace_id TEXT NOT NULL, event_index INTEGER NOT NULL,
  event_type TEXT NOT NULL, occurred_at TEXT NOT NULL, delta_ms INTEGER NOT NULL, detail_json TEXT,
  PRIMARY KEY (session_id, trace_id, event_index),
  FOREIGN KEY (session_id, trace_id) REFERENCES trace_responses(session_id, trace_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_sessions_participant ON experiment_sessions(participant_code);
CREATE INDEX IF NOT EXISTS idx_telemetry_type ON telemetry_events(event_type);`

function required(object, key, type) {
  const value = object?.[key]
  if (typeof value !== type || (type === 'string' && !value.trim())) throw new Error(`campo obrigatório inválido: ${key}`)
  return value
}

export function openDatabase(path) {
  const database = new DatabaseSync(path)
  const existing = database.prepare("SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'experiment_sessions'").get()
  if (existing?.sql?.includes('group_number BETWEEN 1 AND 7')) {
    database.exec('PRAGMA foreign_keys = OFF; BEGIN IMMEDIATE;')
    try {
      database.exec(existing.sql.replace('experiment_sessions', 'experiment_sessions_new').replace('group_number BETWEEN 1 AND 7', 'group_number BETWEEN 1 AND 3'))
      database.exec('INSERT INTO experiment_sessions_new SELECT * FROM experiment_sessions')
      database.exec('DROP TABLE experiment_sessions')
      database.exec('ALTER TABLE experiment_sessions_new RENAME TO experiment_sessions')
      database.exec('COMMIT')
    } catch (error) {
      database.exec('ROLLBACK')
      throw error
    } finally {
      database.exec('PRAGMA foreign_keys = ON')
    }
  }
  database.exec(schema)
  return database
}

export function saveSession(database, payload) {
  const session = required(payload, 'session', 'object')
  const sessionId = required(session, 'sessionId', 'string')
  required(session, 'participantCode', 'string')
  required(session, 'completedAt', 'string')
  if (!Number.isInteger(session.group) || session.group < 1 || session.group > 3) throw new Error('participante inválido')
  const taskCount = session.taskSet?.length
  if (!Array.isArray(session.taskSet) || taskCount !== 3 || new Set(session.taskSet).size !== taskCount || !Array.isArray(payload.traces) || Object.keys(session.traceResponses ?? {}).length !== taskCount || payload.traces.length !== taskCount || session.currentIndex !== taskCount) {
    throw new Error('a sessão concluída deve conter três tarefas e três traces')
  }
  const entries = new Map(payload.traces.map((entry) => [entry.id, entry]))
  const upsertSession = database.prepare(`INSERT INTO experiment_sessions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(session_id) DO UPDATE SET participant_code=excluded.participant_code,
    group_number=excluded.group_number, repetition=excluded.repetition, task_set_json=excluded.task_set_json,
    started_at=excluded.started_at, completed_at=excluded.completed_at, exported_at=excluded.exported_at,
    received_at=excluded.received_at, experiment=excluded.experiment, schema_version=excluded.schema_version,
    payload_json=excluded.payload_json`)
  const insertTrace = database.prepare('INSERT INTO trace_responses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
  const insertReference = database.prepare('INSERT INTO evidence_references VALUES (?, ?, ?, ?, ?, ?, ?)')
  const insertEvent = database.prepare('INSERT INTO telemetry_events VALUES (?, ?, ?, ?, ?, ?, ?)')
  database.exec('BEGIN IMMEDIATE')
  try {
    upsertSession.run(sessionId, session.participantCode, session.group, session.repetition, JSON.stringify(session.taskSet), session.startedAt, session.completedAt, payload.exportedAt, new Date().toISOString(), payload.experiment, payload.schemaVersion, JSON.stringify(payload))
    database.prepare('DELETE FROM trace_responses WHERE session_id = ?').run(sessionId)
    payload.traces.forEach((entry, sequenceIndex) => {
      const traceId = entry.id
      const response = session.traceResponses[traceId]
      if (!response?.completedAt || !entries.has(traceId)) throw new Error(`resposta ausente ou incompleta para o trace ${traceId}`)
      if (!response.evidenceReferences?.length && !response.noReferencesFound) throw new Error(`referência ou resposta "Não encontrei referências" obrigatória para o trace ${traceId}`)
      insertTrace.run(sessionId, traceId, sequenceIndex, entry.runId ?? null, entry.task, entry.harness, entry.repetition, entry.model ?? null, entry.status ?? null, response.startedAt, response.readingCompletedAt ?? null, response.completedAt, response.firstEvidenceAt ?? null, response.confidence ?? null, response.difficulty ?? null, response.ease ?? null, response.directness ?? null, response.notes ?? '', response.evidenceInteractions ?? 0, response.positionChanges ?? 0, JSON.stringify(payload.derivedMetrics?.[traceId] ?? {}))
      response.evidenceReferences?.forEach((reference) => insertReference.run(reference.id, sessionId, traceId, reference.startLine, reference.endLine, reference.addedAt, reference.deltaMs))
      response.telemetry?.forEach((event, index) => insertEvent.run(sessionId, traceId, index, event.type, event.at, event.deltaMs, event.detail == null ? null : JSON.stringify(event.detail)))
    })
    database.exec('COMMIT')
    return sessionId
  } catch (error) {
    database.exec('ROLLBACK')
    throw error
  }
}

const mimeTypes = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.log': 'text/plain; charset=utf-8', '.svg': 'image/svg+xml' }

export function createExperimentServer({ database, staticDirectory }) {
  return createServer((request, response) => {
    if (request.method === 'OPTIONS' && request.url?.startsWith('/api/')) {
      response.writeHead(204, { 'Access-Control-Allow-Origin': 'http://127.0.0.1:4173', 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' })
      response.end()
      return
    }
    if (request.method === 'GET' && request.url === '/api/health') return sendJson(response, 200, { status: 'ok' })
    if (request.method === 'POST' && request.url === '/api/experiment-sessions') {
      let body = ''
      request.on('data', (chunk) => { body += chunk; if (body.length > 10_000_000) request.destroy() })
      request.on('end', () => {
        try {
          const sessionId = saveSession(database, JSON.parse(body))
          sendJson(response, 201, { sessionId, saved: true })
        } catch (error) {
          sendJson(response, 400, { error: error instanceof Error ? error.message : 'payload inválido' })
        }
      })
      return
    }
    if (request.method !== 'GET') return sendJson(response, 404, { error: 'not found' })
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname)
    const relative = normalize(pathname).replace(/^[/\\]+/, '') || 'index.html'
    let file = resolve(join(staticDirectory, relative))
    if (!file.startsWith(resolve(staticDirectory))) return sendJson(response, 403, { error: 'forbidden' })
    try { if (statSync(file).isDirectory()) file = join(file, 'index.html') } catch { file = join(staticDirectory, 'index.html') }
    try {
      const content = readFileSync(file)
      response.writeHead(200, { 'Content-Type': mimeTypes[extname(file)] ?? 'application/octet-stream', 'Content-Length': content.length })
      response.end(content)
    } catch { sendJson(response, 404, { error: 'not found' }) }
  })
}

function sendJson(response, status, value) {
  const body = Buffer.from(JSON.stringify(value))
  response.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': body.length, 'Access-Control-Allow-Origin': 'http://127.0.0.1:4173' })
  response.end(body)
}

function option(name, fallback) {
  const index = process.argv.indexOf(name)
  return index < 0 ? fallback : process.argv[index + 1]
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const port = Number(option('--port', '8765'))
  const host = option('--host', '127.0.0.1')
  const databasePath = resolve(option('--database', join(root, 'experiment.sqlite')))
  const staticDirectory = resolve(option('--static', join(root, 'dist')))
  const database = openDatabase(databasePath)
  createExperimentServer({ database, staticDirectory }).listen(port, host, () => console.log(`Experiment server: http://${host}:${port} (database: ${databasePath})`))
}
