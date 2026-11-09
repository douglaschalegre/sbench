import { createHash, randomBytes, randomUUID } from 'node:crypto'

export const hash = (value) => createHash('sha256').update(value).digest('hex')
const harnesses = ['bdi', 'codex', 'opencode']

export async function validateInvitationConfig(database, config) {
  const { participantCode, group, runId, repetition, taskSet, expiresAt } = config ?? {}
  if (typeof participantCode !== 'string' || !/^[A-Za-z0-9_-]{3,64}$/.test(participantCode) || !Number.isInteger(group) || group < 1 || group > 3 || typeof runId !== 'string' || typeof repetition !== 'string' || !Array.isArray(taskSet) || taskSet.length !== 3 || new Set(taskSet).size !== 3 || !taskSet.every((task) => typeof task === 'string') || !Number.isFinite(Date.parse(expiresAt)) || Date.parse(expiresAt) <= Date.now()) {
    throw new Error('Configuração inválida: informe participante, grupo 1–3, execução, réplica, três tarefas diferentes e validade futura.')
  }
  const { rows } = await database.execute('SELECT metadata_json FROM trace_catalog')
  const catalog = rows.map((row) => JSON.parse(row.metadata_json))
  const traces = taskSet.map((task, index) => {
    const matches = catalog.filter((entry) => entry.task === task && entry.runId === runId && entry.repetition === repetition && entry.harness === harnesses[(group - 1 + index) % 3])
    if (matches.length !== 1) throw new Error(`Esperado exatamente um trace para ${task} na posição ${index + 1}. Importe o catálogo correto.`)
    return matches[0]
  })
  return { participantCode, group, runId, repetition, taskSet, expiresAt: new Date(expiresAt).toISOString(), traces }
}

export async function createInvitation(database, config) {
  const { participantCode, group, runId, repetition, taskSet, expiresAt, traces } = await validateInvitationConfig(database, config)
  const code = randomBytes(24).toString('base64url')
  const invitationId = randomUUID()
  const sessionId = randomUUID()
  await database.execute({ sql: `INSERT INTO experiment_invitations
    (invitation_id, code_hash, session_id, participant_code, group_number, run_id, repetition, task_set_json, traces_json, created_at, expires_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`, args: [invitationId, hash(code), sessionId, participantCode, group, runId, repetition, JSON.stringify(taskSet), JSON.stringify(traces), new Date().toISOString(), new Date(expiresAt).toISOString()] })
  return { invitationId, sessionId, code }
}

export function assignedSession(invitation) {
  return {
    sessionId: invitation.session_id, participantCode: invitation.participant_code,
    group: invitation.group_number, runId: invitation.run_id, repetition: invitation.repetition,
    taskSet: JSON.parse(invitation.task_set_json), startedAt: invitation.started_at,
    currentIndex: 0, traceResponses: {},
  }
}

export async function authenticate(database, cookie = '') {
  const token = cookie.split(';').map((part) => part.trim()).find((part) => part.startsWith('sbench_access='))?.slice('sbench_access='.length)
  if (!token || !/^[A-Za-z0-9_-]{43}$/.test(token)) return null
  const { rows } = await database.execute({ sql: `SELECT i.* FROM access_sessions a
    JOIN experiment_invitations i ON i.invitation_id = a.invitation_id
    WHERE a.token_hash = ? AND a.expires_at > ? AND i.expires_at > ? AND i.revoked_at IS NULL`, args: [hash(token), new Date().toISOString(), new Date().toISOString()] })
  return rows[0] ?? null
}

export function validateAssignment(invitation, payload) {
  const expected = assignedSession(invitation)
  const session = payload?.session
  for (const key of ['sessionId', 'participantCode', 'group', 'runId', 'repetition', 'startedAt', 'taskSet']) {
    if (JSON.stringify(session?.[key]) !== JSON.stringify(expected[key])) throw new Error('A sessão não corresponde ao convite.')
  }
  const traces = JSON.parse(invitation.traces_json)
  if (!Array.isArray(payload.traces) || payload.traces.length !== traces.length || payload.traces.some((trace, index) => trace?.id !== traces[index].id)) throw new Error('Traces diferentes dos atribuídos ao participante.')
  // Persist canonical metadata; browser-supplied labels must not redefine the experiment.
  payload.traces = traces
}

export async function login(database, code) {
  if (typeof code !== 'string' || !/^[A-Za-z0-9_-]{32}$/.test(code.trim())) return null
  const now = new Date().toISOString()
  const { rows } = await database.execute({ sql: 'SELECT * FROM experiment_invitations WHERE code_hash = ? AND expires_at > ? AND revoked_at IS NULL', args: [hash(code.trim()), now] })
  const invitation = rows[0]
  if (!invitation) return null
  const token = randomBytes(32).toString('base64url')
  const expiresAt = new Date(Math.min(Date.now() + 12 * 3600_000, Date.parse(invitation.expires_at))).toISOString()
  await database.batch([
    { sql: 'UPDATE experiment_invitations SET started_at = COALESCE(started_at, ?) WHERE invitation_id = ?', args: [now, invitation.invitation_id] },
    { sql: 'DELETE FROM access_sessions WHERE expires_at <= ?', args: [now] },
    { sql: 'INSERT INTO access_sessions VALUES (?, ?, ?)', args: [hash(token), invitation.invitation_id, expiresAt] },
  ], 'write')
  invitation.started_at ??= now
  return { token, expiresAt, invitation }
}
