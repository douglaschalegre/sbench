import assert from 'node:assert/strict'
import { afterEach, test } from 'node:test'
import { createExperimentServer, openDatabase, saveSession } from '../server.mjs'

const databases = []
afterEach(() => { while (databases.length) databases.pop().close() })

function payload(sessionId = 'session-1') {
  const traceIds = ['trace-1', 'trace-2', 'trace-3']
  const traceResponses = Object.fromEntries(traceIds.map((traceId, index) => [traceId, { traceId, startedAt: '2026-01-01T00:00:00Z', completedAt: '2026-01-01T00:01:00Z', evidenceInteractions: 1, positionChanges: 2, evidenceReferences: [{ id: `ref-${index}`, startLine: 1, endLine: 3, addedAt: '2026-01-01T00:00:10Z', deltaMs: 10000 }], telemetry: [{ type: 'line_selection', at: '2026-01-01T00:00:05Z', deltaMs: 5000, detail: { line: 1 } }], confidence: 4, difficulty: 2, ease: 5, directness: 'direct', notes: '' }]))
  return { schemaVersion: 2, exportedAt: '2026-01-01T00:03:00Z', experiment: 'sbench-latin-square-q1-q4', session: { sessionId, participantCode: 'P-001', group: 1, repetition: 'r1', taskSet: ['task-0', 'task-1', 'task-2'], startedAt: '2026-01-01T00:00:00Z', completedAt: '2026-01-01T00:03:00Z', currentIndex: 3, traceResponses }, traces: traceIds.map((id, index) => ({ id, runId: 'run', task: `task-${index}`, harness: 'bdi', repetition: 'r1', model: 'model', status: 'ok' })), derivedMetrics: Object.fromEntries(traceIds.map((id) => [id, { m1_1_firstEvidenceDeltaMs: 10000 }])) }
}

test('saves a normalized session idempotently', () => {
  const database = openDatabase(':memory:'); databases.push(database)
  const data = payload()
  saveSession(database, data)
  data.session.traceResponses['trace-1'].notes = 'updated'
  saveSession(database, data)
  assert.equal(database.prepare('SELECT COUNT(*) count FROM experiment_sessions').get().count, 1)
  assert.equal(database.prepare('SELECT COUNT(*) count FROM trace_responses').get().count, 3)
  assert.equal(database.prepare('SELECT COUNT(*) count FROM evidence_references').get().count, 3)
  assert.equal(database.prepare('SELECT COUNT(*) count FROM telemetry_events').get().count, 3)
  assert.equal(database.prepare("SELECT notes FROM trace_responses WHERE trace_id='trace-1'").get().notes, 'updated')
})

test('rejects incomplete sessions', () => {
  const database = openDatabase(':memory:'); databases.push(database)
  const data = payload(); delete data.session.traceResponses['trace-3']
  assert.throws(() => saveSession(database, data), /exatamente três/)
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
