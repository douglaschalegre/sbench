import { randomBytes, timingSafeEqual } from 'node:crypto'
import { hash, validateInvitationConfig } from './access.mjs'

export function adminToken(cookie = '') {
  return cookie.split(';').map((part) => part.trim()).find((part) => part.startsWith('sbench_admin='))?.slice('sbench_admin='.length)
}

export async function adminLogin(database, password, configuredPassword) {
  if (!configuredPassword) return null
  if (typeof password !== 'string' || password.length > 1024 || !timingSafeEqual(Buffer.from(hash(password), 'hex'), Buffer.from(hash(configuredPassword), 'hex'))) return null
  const token = randomBytes(32).toString('base64url')
  const expiresAt = new Date(Date.now() + 8 * 3600_000).toISOString()
  await database.batch([
    { sql: 'DELETE FROM admin_sessions WHERE expires_at <= ? OR password_hash <> ?', args: [new Date().toISOString(), hash(configuredPassword)] },
    { sql: 'INSERT INTO admin_sessions VALUES (?, ?, ?)', args: [hash(token), hash(configuredPassword), expiresAt] },
  ], 'write')
  return { token, expiresAt }
}

export async function authenticateAdmin(database, cookie, password) {
  const token = adminToken(cookie)
  if (!password || !token || !/^[A-Za-z0-9_-]{43}$/.test(token)) return false
  const { rows } = await database.execute({ sql: 'SELECT token_hash FROM admin_sessions WHERE token_hash = ? AND password_hash = ? AND expires_at > ?', args: [hash(token), hash(password), new Date().toISOString()] })
  return rows.length === 1
}

export async function listInvitations(database) {
  const { rows } = await database.execute(`SELECT i.invitation_id, i.session_id, i.participant_code,
    i.group_number, i.run_id, i.repetition, i.task_set_json, i.created_at, i.expires_at,
    i.started_at, i.revoked_at, s.completed_at FROM experiment_invitations i
    LEFT JOIN experiment_sessions s ON s.session_id = i.session_id ORDER BY i.created_at DESC, i.invitation_id`)
  return rows.map((row) => ({
    invitationId: row.invitation_id, sessionId: row.session_id, participantCode: row.participant_code,
    group: row.group_number, runId: row.run_id, repetition: row.repetition, taskSet: JSON.parse(row.task_set_json),
    createdAt: row.created_at, expiresAt: row.expires_at, startedAt: row.started_at, revokedAt: row.revoked_at,
    completedAt: row.completed_at,
  }))
}

function failure(status, message) {
  return Object.assign(new Error(message), { status })
}

async function unusedInvitation(database, invitationId, change) {
  // A write transaction prevents login from starting an experiment during an edit or deletion.
  const transaction = await database.transaction('write')
  try {
    const { rows } = await transaction.execute({ sql: `SELECT i.started_at, s.completed_at FROM experiment_invitations i
      LEFT JOIN experiment_sessions s ON s.session_id = i.session_id WHERE i.invitation_id = ?`, args: [invitationId] })
    if (!rows[0]) throw failure(404, 'Convite não encontrado.')
    if (rows[0].started_at || rows[0].completed_at) throw failure(409, 'A participação já foi iniciada. Você pode revogar o acesso e criar outro convite.')
    const result = await change(transaction)
    await transaction.commit()
    return result
  } finally { transaction.close() }
}

export async function updateInvitation(database, invitationId, config) {
  return unusedInvitation(database, invitationId, async (transaction) => {
    const { participantCode, group, runId, repetition, taskSet, expiresAt, traces } = await validateInvitationConfig(transaction, config)
    await transaction.execute({ sql: `UPDATE experiment_invitations SET participant_code = ?, group_number = ?, run_id = ?,
      repetition = ?, task_set_json = ?, expires_at = ?, traces_json = ? WHERE invitation_id = ?`, args: [participantCode, group, runId, repetition, JSON.stringify(taskSet), expiresAt, JSON.stringify(traces), invitationId] })
    return { saved: true }
  })
}

export async function deleteInvitation(database, invitationId) {
  return unusedInvitation(database, invitationId, async (transaction) => {
    await transaction.execute({ sql: 'DELETE FROM access_sessions WHERE invitation_id = ?', args: [invitationId] })
    await transaction.execute({ sql: 'DELETE FROM experiment_invitations WHERE invitation_id = ?', args: [invitationId] })
    return { deleted: true }
  })
}

export async function rotateInvitationCode(database, invitationId) {
  return unusedInvitation(database, invitationId, async (transaction) => {
    const code = randomBytes(24).toString('base64url')
    await transaction.execute({ sql: 'UPDATE experiment_invitations SET code_hash = ? WHERE invitation_id = ?', args: [hash(code), invitationId] })
    await transaction.execute({ sql: 'DELETE FROM access_sessions WHERE invitation_id = ?', args: [invitationId] })
    return { invitationId, code }
  })
}

export async function revokeInvitation(database, invitationId) {
  const result = await database.execute({ sql: 'UPDATE experiment_invitations SET revoked_at = COALESCE(revoked_at, ?) WHERE invitation_id = ?', args: [new Date().toISOString(), invitationId] })
  if (!result.rowsAffected) throw failure(404, 'Convite não encontrado.')
  return { revoked: true }
}
