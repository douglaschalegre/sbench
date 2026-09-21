import type { Harness } from './types'

export const latinSquare: Record<1 | 2 | 3, Harness[]> = {
  1: ['bdi', 'codex', 'opencode'],
  2: ['codex', 'opencode', 'bdi'],
  3: ['opencode', 'bdi', 'codex'],
}

export const harnessLabel: Record<Harness, string> = { bdi: 'BDI', codex: 'Codex', opencode: 'OpenCode' }
export const defaultTasks = ['incident_staffing_plan', 'community_workshop_replan', 'vendor_selection']
