export type Harness = 'bdi' | 'codex' | 'opencode'

export type TraceEntry = {
  id: string
  runId: string
  task: string
  harness: Harness
  repetition: string
  url: string
  elapsedSeconds: number
  status: string
  model: string
}

export type Manifest = { generatedAt: string; entries: TraceEntry[] }

export type EvidenceReference = {
  id: string
  startLine: number
  endLine: number
  addedAt: string
  deltaMs: number
}

export type TelemetryEvent = {
  type: 'scroll' | 'search' | 'search_navigation' | 'wrap_toggle' | 'line_selection' | 'lines_viewed' | 'evidence_added' | 'evidence_removed' | 'answer_changed'
  at: string
  deltaMs: number
  detail?: Record<string, string | number | boolean | number[]>
}

export type TraceResponse = {
  traceId: string
  startedAt: string
  readingCompletedAt?: string
  completedAt?: string
  firstEvidenceAt?: string
  evidenceInteractions: number
  positionChanges: number
  evidenceReferences: EvidenceReference[]
  telemetry: TelemetryEvent[]
  confidence?: number
  difficulty?: number
  ease?: number
  directness?: 'direct' | 'inferred'
  notes: string
}

export type SessionState = {
  sessionId: string
  participantCode: string
  group: 1 | 2 | 3
  repetition: string
  taskSet: string[]
  startedAt: string
  currentIndex: number
  traceResponses: Record<string, TraceResponse>
  completedAt?: string
}
