import { createClient } from '@libsql/client'
import { resolve } from 'node:path'

export const schema = `

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

export async function openDatabase(path) {
  const url = path ? (path === ':memory:' ? path : `file:${resolve(path)}`) : process.env.TURSO_DATABASE_URL
  if (!url) throw new Error('Configure TURSO_DATABASE_URL ou informe --database para usar SQLite local.')
  if (process.env.VERCEL && !url.startsWith('libsql://') && !url.startsWith('https://')) throw new Error('O deploy exige um banco remoto.')
  const database = createClient({ url, authToken: path ? undefined : process.env.TURSO_AUTH_TOKEN })
  return database
}

export async function migrate(database) {
  await database.executeMultiple(schema + accessSchema)
}

const accessSchema = `
CREATE TABLE IF NOT EXISTS trace_catalog (
  trace_id TEXT PRIMARY KEY, metadata_json TEXT NOT NULL, content TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS experiment_invitations (
  invitation_id TEXT PRIMARY KEY, code_hash TEXT NOT NULL UNIQUE,
  session_id TEXT NOT NULL UNIQUE, participant_code TEXT NOT NULL,
  group_number INTEGER NOT NULL CHECK (group_number BETWEEN 1 AND 3),
  run_id TEXT NOT NULL, repetition TEXT NOT NULL, task_set_json TEXT NOT NULL,
  traces_json TEXT NOT NULL, created_at TEXT NOT NULL, expires_at TEXT NOT NULL,
  started_at TEXT, revoked_at TEXT
);
CREATE TABLE IF NOT EXISTS admin_sessions (
  token_hash TEXT PRIMARY KEY, password_hash TEXT NOT NULL, expires_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS access_sessions (
  token_hash TEXT PRIMARY KEY,
  invitation_id TEXT NOT NULL REFERENCES experiment_invitations(invitation_id),
  expires_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_access_invitation ON access_sessions(invitation_id);
`

function required(object, key, type) {
  const value = object?.[key]
  if (value == null || typeof value !== type || (type === 'string' && !value.trim())) throw new Error(`campo obrigatório inválido: ${key}`)
  return value
}

export async function saveSession(database, payload) {
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
  const upsertSession = statement(`INSERT INTO experiment_sessions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(session_id) DO UPDATE SET participant_code=excluded.participant_code,
    group_number=excluded.group_number, repetition=excluded.repetition, task_set_json=excluded.task_set_json,
    started_at=excluded.started_at, completed_at=excluded.completed_at, exported_at=excluded.exported_at,
    received_at=excluded.received_at, experiment=excluded.experiment, schema_version=excluded.schema_version,
    payload_json=excluded.payload_json`)
  const insertTrace = statement('INSERT INTO trace_responses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
  const insertReference = statement('INSERT INTO evidence_references VALUES (?, ?, ?, ?, ?, ?, ?)')
  const insertEvent = statement('INSERT INTO telemetry_events VALUES (?, ?, ?, ?, ?, ?, ?)')
  const statements = []
  function statement(sql) { return { run: (...args) => statements.push({ sql, args }) } }
  upsertSession.run(sessionId, session.participantCode, session.group, session.repetition, JSON.stringify(session.taskSet), session.startedAt, session.completedAt, payload.exportedAt, new Date().toISOString(), payload.experiment, payload.schemaVersion, JSON.stringify(payload))
  statement('DELETE FROM trace_responses WHERE session_id = ?').run(sessionId)
  payload.traces.forEach((entry, sequenceIndex) => {
    const traceId = entry.id
    const response = session.traceResponses[traceId]
    if (!response?.completedAt || !entries.has(traceId)) throw new Error(`resposta ausente ou incompleta para o trace ${traceId}`)
    if (!response.evidenceReferences?.length && !response.noReferencesFound) throw new Error(`referência ou resposta "Não encontrei referências" obrigatória para o trace ${traceId}`)
    insertTrace.run(sessionId, traceId, sequenceIndex, entry.runId ?? null, entry.task, entry.harness, entry.repetition, entry.model ?? null, entry.status ?? null, response.startedAt, response.readingCompletedAt ?? null, response.completedAt, response.firstEvidenceAt ?? null, response.confidence ?? null, response.difficulty ?? null, response.ease ?? null, response.directness ?? null, response.notes ?? '', response.evidenceInteractions ?? 0, response.positionChanges ?? 0, JSON.stringify(payload.derivedMetrics?.[traceId] ?? {}))
    response.evidenceReferences?.forEach((reference) => insertReference.run(reference.id, sessionId, traceId, reference.startLine, reference.endLine, reference.addedAt, reference.deltaMs))
    response.telemetry?.forEach((event, index) => insertEvent.run(sessionId, traceId, index, event.type, event.at, event.deltaMs, event.detail == null ? null : JSON.stringify(event.detail)))
  })
  await database.batch(statements, 'write')
  return sessionId
}
