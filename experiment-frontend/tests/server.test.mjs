import assert from 'node:assert/strict'
import { DatabaseSync } from 'node:sqlite'
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, test } from 'node:test'
import { createExperimentServer, openDatabase, saveSession } from '../server.mjs'

const databases = []
afterEach(() => { while (databases.length) databases.pop().close() })

function payload(sessionId = 'session-1') {
  const traceIds = Array.from({ length: 7 }, (_, index) => `trace-${index + 1}`)
  const traceResponses = Object.fromEntries(traceIds.map((traceId, index) => [traceId, { traceId, startedAt: '2026-01-01T00:00:00Z', completedAt: '2026-01-01T00:01:00Z', evidenceInteractions: 1, positionChanges: 2, evidenceReferences: [{ id: `ref-${index}`, startLine: 1, endLine: 3, addedAt: '2026-01-01T00:00:10Z', deltaMs: 10000 }], telemetry: [{ type: 'line_selection', at: '2026-01-01T00:00:05Z', deltaMs: 5000, detail: { line: 1 } }], confidence: 4, difficulty: 2, ease: 5, directness: 'direct', notes: '' }]))
  return { schemaVersion: 4, exportedAt: '2026-01-01T00:03:00Z', experiment: 'sbench-latin-square-q1-q4', session: { sessionId, participantCode: 'P-001', group: 7, repetition: 'r1', taskSet: Array.from({ length: 7 }, (_, index) => `task-${index}`), startedAt: '2026-01-01T00:00:00Z', completedAt: '2026-01-01T00:03:00Z', currentIndex: 7, traceResponses }, traces: traceIds.map((id, index) => ({ id, runId: 'run', task: `task-${index}`, harness: 'bdi', repetition: 'r1', model: 'model', status: 'ok' })), derivedMetrics: Object.fromEntries(traceIds.map((id) => [id, { m1_1_firstEvidenceDeltaMs: 10000 }])) }
}

test('saves a normalized session idempotently', () => {
  const database = openDatabase(':memory:'); databases.push(database)
  const data = payload()
  saveSession(database, data)
  data.session.traceResponses['trace-1'].notes = 'updated'
  saveSession(database, data)
  assert.equal(database.prepare('SELECT COUNT(*) count FROM experiment_sessions').get().count, 1)
  assert.equal(database.prepare('SELECT COUNT(*) count FROM trace_responses').get().count, 7)
  assert.equal(database.prepare('SELECT COUNT(*) count FROM evidence_references').get().count, 7)
  assert.equal(database.prepare('SELECT COUNT(*) count FROM telemetry_events').get().count, 7)
  assert.equal(database.prepare("SELECT notes FROM trace_responses WHERE trace_id='trace-1'").get().notes, 'updated')
})

test('accepts an existing three-trace session', () => {
  const database = openDatabase(':memory:'); databases.push(database)
  const data = payload('legacy-session')
  data.session.group = 1
  data.session.taskSet = data.session.taskSet.slice(0, 3)
  data.session.currentIndex = 3
  data.traces = data.traces.slice(0, 3)
  data.session.traceResponses = Object.fromEntries(Object.entries(data.session.traceResponses).slice(0, 3))
  saveSession(database, data)
  assert.equal(database.prepare('SELECT COUNT(*) count FROM trace_responses').get().count, 3)
})

test('accepts a completed trace without references when marked as not found', () => {
  const database = openDatabase(':memory:'); databases.push(database)
  const data = payload()
  data.session.traceResponses['trace-1'].evidenceReferences = []
  data.session.traceResponses['trace-1'].noReferencesFound = true
  data.derivedMetrics['trace-1'].m1_1_noReferencesFound = true
  saveSession(database, data)
  assert.equal(database.prepare('SELECT COUNT(*) count FROM trace_responses').get().count, 7)
  assert.equal(database.prepare('SELECT COUNT(*) count FROM evidence_references').get().count, 6)
  const saved = JSON.parse(database.prepare('SELECT payload_json FROM experiment_sessions').get().payload_json)
  assert.equal(saved.session.traceResponses['trace-1'].noReferencesFound, true)
})

test('rejects a trace without a reference or a not-found answer', () => {
  const database = openDatabase(':memory:'); databases.push(database)
  const data = payload()
  data.session.traceResponses['trace-1'].evidenceReferences = []
  assert.throws(() => saveSession(database, data), /referência ou resposta/)
})

test('rejects incomplete sessions', () => {
  const database = openDatabase(':memory:'); databases.push(database)
  const data = payload(); delete data.session.traceResponses['trace-7']
  assert.throws(() => saveSession(database, data), /três ou sete tarefas/)
})

test('accepts completed sessions through the HTTP API', async () => {
  const database = openDatabase(':memory:'); databases.push(database)
  const server = createExperimentServer({ database, staticDirectory: process.cwd() })
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve))
  try {
    const { port } = server.address()
    const response = await fetch(`http://127.0.0.1:${port}/api/experiment-sessions`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload('session-http')) })
    assert.equal(response.status, 201)
    assert.deepEqual(await response.json(), { sessionId: 'session-http', saved: true })
    assert.equal(database.prepare('SELECT COUNT(*) count FROM experiment_sessions').get().count, 1)
  } finally {
    await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()))
  }
})


test('migrates the existing database to accept group 7', () => {
  const directory = mkdtempSync(join(tmpdir(), 'sbench-experiment-'))
  const path = join(directory, 'experiment.sqlite')
  try {
    const legacy = new DatabaseSync(path)
    legacy.exec(`CREATE TABLE experiment_sessions (
      session_id TEXT PRIMARY KEY, participant_code TEXT NOT NULL,
      group_number INTEGER NOT NULL CHECK (group_number BETWEEN 1 AND 3),
      repetition TEXT NOT NULL, task_set_json TEXT NOT NULL, started_at TEXT NOT NULL,
      completed_at TEXT NOT NULL, exported_at TEXT NOT NULL, received_at TEXT NOT NULL,
      experiment TEXT NOT NULL, schema_version INTEGER NOT NULL, payload_json TEXT NOT NULL
    );`)
    legacy.prepare('INSERT INTO experiment_sessions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)').run('old', 'P-OLD', 1, 'r1', '[]', 'start', 'end', 'export', 'received', 'old-experiment', 3, '{}')
    legacy.close()
    const database = openDatabase(path); databases.push(database)
    assert.equal(database.prepare('SELECT participant_code FROM experiment_sessions WHERE session_id = ?').get('old').participant_code, 'P-OLD')
    saveSession(database, payload('new'))
    assert.equal(database.prepare('SELECT group_number FROM experiment_sessions WHERE session_id = ?').get('new').group_number, 7)
    assert.deepEqual(database.prepare('PRAGMA foreign_key_check').all(), [])
  } finally {
    while (databases.length) databases.pop().close()
    rmSync(directory, { recursive: true, force: true })
  }
})
