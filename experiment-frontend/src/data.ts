import type { Harness } from './types'

export const groupNumbers = [1, 2, 3, 4, 5, 6, 7] as const
export type GroupNumber = typeof groupNumbers[number]

const harnessOrder: Harness[] = ['bdi', 'codex', 'opencode']
export const latinSquare: Record<GroupNumber, Harness[]> = Object.fromEntries(
  groupNumbers.map((group) => [group, groupNumbers.map((_, activity) => harnessOrder[(group - 1 + activity) % harnessOrder.length])]),
) as Record<GroupNumber, Harness[]>

export const harnessLabel: Record<Harness, string> = { bdi: 'BDI', codex: 'Codex', opencode: 'OpenCode' }
export const defaultTasks = ['incident_staffing_plan', 'travel_reimbursement_audit', 'vendor_selection', 'clinic_rollout_plan', 'community_workshop_replan', 'grant_closeout_recovery', 'shelter_restock_scope']
