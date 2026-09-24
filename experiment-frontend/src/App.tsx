import { useEffect, useMemo, useRef, useState } from 'react'
import { ArrowLeft, ArrowRight, Check, CheckCircle2, ClipboardCopy, Clock3, Download, FileText, FlaskConical, Highlighter, LoaderCircle, MousePointer2, RefreshCw, RotateCcw, ShieldCheck, X } from 'lucide-react'
import { Button, FieldLabel, Progress, Scale, Segmented } from './components/ui'
import { defaultTasks, groupNumbers, latinSquare } from './data'
import type { GroupNumber } from './data'
import { cn, formatDuration, labelTask } from './lib/utils'
import type { EvidenceReference, Manifest, SessionState, TelemetryEvent, TraceEntry, TraceResponse } from './types'

const STORAGE_KEY = 'sbench-latin-square-session-v2'

function newSessionId() {
  return crypto.randomUUID()
}

function emptyTrace(traceId: string): TraceResponse {
  return { traceId, startedAt: new Date().toISOString(), evidenceInteractions: 0, positionChanges: 0, evidenceReferences: [], telemetry: [], notes: '' }
}

function referencedLines(references: EvidenceReference[]) {
  return new Set(references.flatMap((reference) => Array.from({ length: reference.endLine - reference.startLine + 1 }, (_, index) => reference.startLine + index)))
}

function deriveMetrics(trace: TraceResponse) {
  const clickSelections = trace.telemetry.filter((event) => event.type === 'line_selection')
  const selectedLines = referencedLines(trace.evidenceReferences)
  const viewedLines = new Set(trace.telemetry.filter((event) => event.type === 'lines_viewed').flatMap((event) => Array.isArray(event.detail?.lines) ? event.detail.lines : []))
  const eventCounts = trace.telemetry.reduce<Record<string, number>>((counts, event) => ({ ...counts, [event.type]: (counts[event.type] ?? 0) + 1 }), {})
  const directnessEvent = [...trace.telemetry].reverse().find((event) => event.type === 'answer_changed' && event.detail?.metric === 'M4.1')
  return {
    m1_1_firstEvidenceDeltaMs: trace.evidenceReferences[0]?.deltaMs ?? null,
    m1_1_noReferencesFound: trace.noReferencesFound ?? false,
    m1_2_selectedLines: selectedLines.size,
    m1_2_viewedLines: viewedLines.size,
    m1_2_selectionInteractions: clickSelections.length,
    m2_1_confidence: trace.confidence ?? null,
    m2_2_cognitiveLoad: trace.difficulty ?? null,
    m3_1_evidenceDeltasMs: trace.evidenceReferences.map((reference) => reference.deltaMs),
    m3_2_positionChanges: trace.positionChanges,
    m3_2_eventCounts: eventCounts,
    m3_3_ease: trace.ease ?? null,
    m4_1_directness: trace.directness ?? null,
    m4_2_classificationDeltaMs: directnessEvent?.deltaMs ?? null,
  }
}

function Logo() {
  return <div className="flex items-center gap-3"><div className="grid size-9 place-items-center rounded-xl bg-forest text-white"><FlaskConical size={18} /></div><div><div className="text-sm font-bold tracking-tight">SBench</div><div className="text-[10px] uppercase tracking-[.18em] text-black/45">Auditability study</div></div></div>
}

function Tutorial({ onComplete }: { onComplete: () => void }) {
  const [selectedLines, setSelectedLines] = useState<number[]>([])
  const [referenceAdded, setReferenceAdded] = useState(false)
  const [confidence, setConfidence] = useState<number>()
  const [directness, setDirectness] = useState<'direct' | 'inferred'>()
  const complete = referenceAdded && confidence != null && directness != null
  const example = ['Agente iniciou a análise.', 'Encontrou o requisito no arquivo task.md.', 'Criou answer/relatorio.md conforme solicitado.', 'Execução finalizada com sucesso.']
  const toggleLine = (line: number) => setSelectedLines((current) => current.includes(line) ? current.filter((item) => item !== line) : [...current, line].sort((a, b) => a - b))
  const classify = (value: 'direct' | 'inferred') => { setDirectness(value); if (referenceAdded && confidence != null) onComplete() }

  return <section className="flex flex-col justify-center">
    <div className="mb-5 flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-[.18em] text-amber">Tutorial obrigatório</p><h1 className="mt-2 font-display text-4xl leading-tight">Aprenda fazendo</h1></div><div className={cn('rounded-full px-3 py-1.5 text-xs font-semibold', complete ? 'bg-[#dcece5] text-forest' : 'bg-white text-black/45')}>{complete ? 'Concluído' : `${referenceAdded ? confidence ? 2 : 1 : 0}/3 etapas`}</div></div>
    <p className="mb-5 max-w-xl text-sm leading-relaxed text-black/55">Este exemplo não entra nos resultados. Complete as três ações para liberar sua sessão.</p>

    <div className="overflow-hidden rounded-2xl border border-line bg-paper shadow-card">
      <div className="border-b border-line px-4 py-3"><div className="flex items-center gap-2"><span className="grid size-6 place-items-center rounded-full bg-forest text-[10px] font-bold text-white">1</span><strong className="text-sm">Selecione as linhas 2 e 3</strong></div><p className="ml-8 mt-1 text-xs text-black/45">Clique em cada linha. Na aplicação, Shift+clique também seleciona intervalos.</p></div>
      <div className="bg-[#101713] py-3 font-mono text-xs text-[#cbd5cc]">{example.map((line, index) => { const lineNumber = index + 1; const selected = selectedLines.includes(lineNumber); return <button type="button" key={line} onClick={() => !referenceAdded && toggleLine(lineNumber)} className={cn('flex w-full items-center border-l-2 border-transparent px-3 py-1.5 text-left hover:bg-white/5', selected && 'border-amber bg-amber/15', referenceAdded && (lineNumber === 2 || lineNumber === 3) && 'border-[#86b59e] bg-[#86b59e]/10')}><span className={cn('mr-4 w-5 text-right text-white/30', selected && 'font-bold text-amber')}>{lineNumber}</span><span>{line}</span></button> })}</div>
      <div className="flex items-center gap-3 border-t border-line p-3"><div className="min-w-0 flex-1 text-xs text-black/50">{referenceAdded ? <span className="font-semibold text-forest">✓ Linhas 2–3 adicionadas como evidência</span> : selectedLines.length ? `${selectedLines.length} linha${selectedLines.length > 1 ? 's' : ''} selecionada${selectedLines.length > 1 ? 's' : ''}` : 'Selecione as duas linhas indicadas'}</div><Button className="h-9 px-3" disabled={referenceAdded || !(selectedLines.includes(2) && selectedLines.includes(3) && selectedLines.length === 2)} onClick={() => { setReferenceAdded(true); setSelectedLines([]) }}><Highlighter size={14} /> Adicionar evidência</Button></div>
    </div>

    <div className={cn('mt-3 rounded-2xl border border-line bg-paper p-4 transition', !referenceAdded && 'pointer-events-none opacity-45')}><div className="flex items-center gap-2"><span className="grid size-6 place-items-center rounded-full bg-forest text-[10px] font-bold text-white">2</span><strong className="text-sm">Responda uma escala</strong></div><p className="ml-8 mt-1 text-xs text-black/45">Escolha qualquer valor para praticar. No estudo, 1 é o mínimo e 5 é o máximo.</p><div className="ml-8 mt-3 grid grid-cols-5 gap-2">{[1, 2, 3, 4, 5].map((value) => <button type="button" key={value} onClick={() => setConfidence(value)} className={cn('h-9 rounded-lg border border-line text-xs font-semibold', confidence === value && 'border-forest bg-[#e8f0e9] text-forest')}>{value}</button>)}</div></div>

    <div className={cn('mt-3 rounded-2xl border border-line bg-paper p-4 transition', (!referenceAdded || confidence == null) && 'pointer-events-none opacity-45')}><div className="flex items-center gap-2"><span className="grid size-6 place-items-center rounded-full bg-forest text-[10px] font-bold text-white">3</span><strong className="text-sm">Classifique a evidência</strong></div><p className="ml-8 mt-1 text-xs text-black/45">Indique se a resposta aparece diretamente ou exige combinar partes do trace.</p><div className="ml-8 mt-3 grid grid-cols-2 gap-2"><button type="button" onClick={() => classify('direct')} className={cn('rounded-lg border border-line p-2.5 text-xs font-semibold', directness === 'direct' && 'border-forest bg-[#e8f0e9] text-forest')}>Declarada diretamente</button><button type="button" onClick={() => classify('inferred')} className={cn('rounded-lg border border-line p-2.5 text-xs font-semibold', directness === 'inferred' && 'border-forest bg-[#e8f0e9] text-forest')}>Inferida combinando partes</button></div></div>
    {complete && <div className="mt-3 flex items-center gap-2 rounded-xl bg-[#dcece5] px-4 py-3 text-sm font-semibold text-forest"><CheckCircle2 size={17} /> Tutorial concluído. Configure e inicie sua sessão.</div>}
  </section>
}

function Welcome({ manifest, onStart, restored, onResume, onReset }: { manifest: Manifest; onStart: (state: SessionState) => void; restored: SessionState | null; onResume: () => void; onReset: () => void }) {
  const tasks = [...new Set(manifest.entries.map((entry) => entry.task))]
  const repetitions = [...new Set(manifest.entries.map((entry) => entry.repetition))].sort()
  const [participantCode, setParticipantCode] = useState('')
  const [group, setGroup] = useState<GroupNumber>(1)
  const [repetition, setRepetition] = useState(repetitions.at(-1) ?? 'r3')
  const [taskSet, setTaskSet] = useState<string[]>(defaultTasks)
  const [tutorialComplete, setTutorialComplete] = useState(false)
  const valid = tutorialComplete && participantCode.trim().length >= 3 && taskSet.length === groupNumbers.length && new Set(taskSet).size === groupNumbers.length

  const start = () => onStart({ sessionId: newSessionId(), participantCode: participantCode.trim(), group, repetition, taskSet, startedAt: new Date().toISOString(), currentIndex: 0, traceResponses: {} })

  return <div className="min-h-screen bg-canvas text-ink">
    <header className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-10"><Logo /><div className="flex items-center gap-2 rounded-full border border-line bg-paper px-3 py-1.5 text-xs text-black/55"><ShieldCheck size={14} className="text-forest" /> Progresso salvo neste dispositivo</div></header>
    <main className="mx-auto grid max-w-7xl gap-14 px-6 pb-16 pt-8 lg:grid-cols-[1.05fr_.95fr] lg:px-10 lg:pt-16">
      <Tutorial onComplete={() => setTutorialComplete(true)} />

      <section className="rounded-[28px] border border-line bg-paper p-6 shadow-card sm:p-8">
        <div className="mb-7"><p className="text-xs font-semibold uppercase tracking-[.18em] text-amber">Configuração da sessão</p><h2 className="mt-2 font-display text-3xl">Antes de começar</h2><p className="mt-2 text-sm text-black/50">Use o código fornecido pelo pesquisador.</p></div>
        {restored && <div className="mb-6 rounded-2xl border border-[#b9cfb5] bg-[#edf4ea] p-4"><div className="flex items-center gap-2 font-semibold text-forest"><CheckCircle2 size={17} /> Sessão em andamento</div><p className="mt-1 text-sm text-black/55">Participante {restored.participantCode} · trace {restored.currentIndex + 1} de {restored.taskSet.length}</p><div className="mt-3 flex gap-2"><Button className="h-9" onClick={onResume}>Continuar</Button><Button className="h-9" variant="ghost" onClick={onReset}><RotateCcw size={14} /> Descartar</Button></div></div>}
        <div className="space-y-6">
          <div><FieldLabel>Código do participante</FieldLabel><input value={participantCode} onChange={(e) => setParticipantCode(e.target.value.toUpperCase())} placeholder="Ex.: P-014" className="h-12 w-full rounded-xl border border-line bg-white px-4 text-sm uppercase tracking-wider outline-none transition placeholder:normal-case placeholder:tracking-normal focus:border-forest focus:ring-2 focus:ring-forest/10" /></div>
          <div><FieldLabel>Grupo do quadrado latino</FieldLabel><Segmented value={String(group)} onValueChange={(value) => setGroup(Number(value) as GroupNumber)} ariaLabel="Grupo experimental" options={groupNumbers.map((n) => ({ value: String(n), label: `Grupo ${n}` }))} /><div className="mt-2 flex items-center gap-2 text-xs text-black/45">A ordem das atividades é definida pelo grupo selecionado.</div></div>
          <div><FieldLabel>Réplica</FieldLabel><select value={repetition} onChange={(e) => setRepetition(e.target.value)} className="h-12 w-full rounded-xl border border-line bg-white px-4 text-sm outline-none focus:border-forest">{repetitions.map((r) => <option key={r}>{r}</option>)}</select></div>
          <div><FieldLabel>Conjunto de tarefas</FieldLabel><div className="space-y-2">{taskSet.map((_, position) => <div key={position} className="flex items-center gap-3"><span className="grid size-7 shrink-0 place-items-center rounded-lg bg-canvas text-xs font-bold text-forest">{position + 1}</span><select value={taskSet[position]} onChange={(e) => setTaskSet(taskSet.map((task, index) => index === position ? e.target.value : task))} className="h-11 min-w-0 flex-1 rounded-xl border border-line bg-white px-3 text-sm outline-none focus:border-forest">{tasks.map((task) => <option key={task} value={task}>{labelTask(task)}</option>)}</select></div>)}</div>{new Set(taskSet).size !== taskSet.length && <p className="mt-2 text-xs text-red-700">Selecione sete tarefas diferentes.</p>}</div>
          <Button disabled={!valid} onClick={start} className="w-full">{tutorialComplete ? 'Iniciar sessão' : 'Complete o tutorial para iniciar'} <ArrowRight size={16} /></Button>
        </div>
      </section>
    </main>
  </div>
}

function LogViewer({ content, references, selectedLines, onSelectionChange, onAddReferences, onTelemetry, initialViewedLines }: { content: string; references: EvidenceReference[]; selectedLines: number[]; onSelectionChange: (lines: number[]) => void; onAddReferences: (ranges: Array<{ startLine: number; endLine: number }>) => void; onTelemetry: (type: TelemetryEvent['type'], detail?: TelemetryEvent['detail']) => void; initialViewedLines: number[] }) {
  const containerRef = useRef<HTMLDivElement>(null)
  const lines = useMemo(() => content.split('\n'), [content])
  const displayLines = useMemo(() => lines.map((line) => {
    const trimmed = line.trim()
    if (!trimmed.startsWith('{') && !trimmed.startsWith('[')) return line
    try {
      return JSON.stringify(JSON.parse(trimmed), null, 2)
        .replaceAll('\\n', '\n')
        .replaceAll('\\r', '')
        .replaceAll('\\t', '  ')
    } catch {
      return line
    }
  }), [lines])
  const [query, setQuery] = useState('')
  const [wrap, setWrap] = useState(true)
  const [anchorLine, setAnchorLine] = useState<number>()
  const [matchIndex, setMatchIndex] = useState(0)
  const viewedLines = useRef(new Set(initialViewedLines))
  const telemetryRef = useRef(onTelemetry)
  telemetryRef.current = onTelemetry
  const matches = useMemo(() => query ? lines.flatMap((line, index) => line.toLowerCase().includes(query.toLowerCase()) ? [index] : []) : [], [lines, query])
  const selectLine = (line: number, extend: boolean) => {
    if (extend && anchorLine) {
      const start = Math.min(anchorLine, line)
      const end = Math.max(anchorLine, line)
      onSelectionChange([...new Set([...selectedLines, ...Array.from({ length: end - start + 1 }, (_, index) => start + index)])].sort((a, b) => a - b))
    } else {
      onSelectionChange(selectedLines.includes(line) ? selectedLines.filter((item) => item !== line) : [...selectedLines, line].sort((a, b) => a - b))
      setAnchorLine(line)
    }
    onTelemetry('line_selection', { line, extend })
  }
  const selectedRanges = useMemo(() => selectedLines.reduce<Array<{ startLine: number; endLine: number }>>((ranges, line) => {
    const last = ranges.at(-1)
    if (last && line === last.endLine + 1) last.endLine = line
    else ranges.push({ startLine: line, endLine: line })
    return ranges
  }, []), [selectedLines])
  const selectionLabel = selectedRanges.map((range) => range.startLine === range.endLine ? `${range.startLine}` : `${range.startLine}–${range.endLine}`).join(', ')
  useEffect(() => {
    const root = containerRef.current
    if (!root) return
    const observer = new IntersectionObserver((entries) => {
      const newlyViewed = entries.flatMap((item) => {
        if (!item.isIntersecting) return []
        const line = Number((item.target as HTMLElement).dataset.line)
        if (!line || viewedLines.current.has(line)) return []
        viewedLines.current.add(line)
        return [line]
      })
      if (newlyViewed.length) telemetryRef.current('lines_viewed', { lines: newlyViewed })
    }, { root, threshold: 0.15 })
    root.querySelectorAll('[data-line]').forEach((element) => observer.observe(element))
    return () => observer.disconnect()
  }, [content])
  const jump = (direction: number) => {
    if (!matches.length) return
    const next = (matchIndex + direction + matches.length) % matches.length
    setMatchIndex(next); onTelemetry('search_navigation', { matchIndex: next, query })
    containerRef.current?.querySelector(`[data-line="${matches[next] + 1}"]`)?.scrollIntoView({ block: 'center', behavior: 'smooth' })
  }

  return <div className="flex h-full min-h-0 flex-col bg-[#101713] text-[#d9e2da]">
    <div className="flex flex-wrap items-center gap-2 border-b border-white/10 px-4 py-3"><div className="flex flex-1 items-center gap-2 rounded-lg bg-white/7 px-3"><span className="text-white/35">⌕</span><input value={query} onChange={(e) => { setQuery(e.target.value); setMatchIndex(0); onTelemetry('search', { query: e.target.value }) }} placeholder="Buscar no trace" className="h-9 min-w-32 flex-1 bg-transparent text-xs text-white outline-none placeholder:text-white/35" />{query && <span className="text-[10px] text-white/40">{matches.length ? `${matchIndex + 1}/${matches.length}` : '0/0'}</span>}<button className="px-1 text-white/50" onClick={() => jump(-1)}>↑</button><button className="px-1 text-white/50" onClick={() => jump(1)}>↓</button></div><button onClick={() => { setWrap(!wrap); onTelemetry('wrap_toggle', { enabled: !wrap }) }} className={cn('rounded-lg px-3 py-2 text-[11px] font-semibold', wrap ? 'bg-white/12 text-white' : 'text-white/45 hover:bg-white/5')}>Quebra de linha</button></div>
    <div ref={containerRef} onScroll={() => onTelemetry('scroll')} className="relative flex-1 overflow-auto py-4 font-mono text-[12px] leading-[1.7] selection:bg-[#de8b4c]/45">
      {displayLines.map((line, index) => {
        const lineNumber = index + 1
        const selected = selectedLines.includes(lineNumber)
        const referenced = references.some((reference) => lineNumber >= reference.startLine && lineNumber <= reference.endLine)
        return <div data-line={lineNumber} key={index} onClick={(event) => selectLine(lineNumber, event.shiftKey)} className={cn('group flex min-w-full cursor-pointer border-l-2 border-transparent px-3 py-0.5 hover:border-amber/40 hover:bg-white/[.035]', matches.includes(index) && 'bg-amber/10', selected && 'border-amber bg-amber/15', referenced && !selected && 'border-[#86b59e] bg-[#86b59e]/10')}><button type="button" aria-label={`Selecionar linha ${lineNumber}`} className={cn('sticky left-0 mr-4 w-10 shrink-0 select-none self-start bg-[#101713] pr-2 text-right text-white/25', selected && 'font-bold text-amber', referenced && 'text-[#9bc8ae]')}>{lineNumber}</button><code className={cn('text-[#cbd5cc]', wrap ? 'whitespace-pre-wrap break-words' : 'whitespace-pre')}>{line || ' '}</code></div>
      })}
    </div>
    {selectedLines.length > 0 && <div className="flex items-center gap-3 border-t border-amber/30 bg-[#1a251f] p-3"><Highlighter size={16} className="shrink-0 text-amber" /><p className="min-w-0 flex-1 text-xs text-white/65">{selectedLines.length === 1 ? 'Linha' : 'Linhas'} {selectionLabel} {selectedLines.length === 1 ? 'selecionada' : 'selecionadas'} <span className="text-white/35">· clique alterna; Shift adiciona intervalo</span></p><Button className="h-9 shrink-0 bg-amber px-3 text-[#281408] hover:bg-[#ec8d45]" onClick={() => { onAddReferences(selectedRanges); setAnchorLine(undefined); onSelectionChange([]) }}>Adicionar referências</Button><button className="text-white/40" onClick={() => { setAnchorLine(undefined); onSelectionChange([]) }}><X size={16} /></button></div>}
  </div>
}

function Questionnaire({ trace, onUpdate, onNoReferences, onRemoveReference, onComplete, canComplete }: { trace: TraceResponse; onUpdate: (patch: Partial<TraceResponse>, metric?: string) => void; onNoReferences: () => void; onRemoveReference: (id: string) => void; onComplete: () => void; canComplete: boolean }) {
  const answered = [trace.evidenceReferences.length > 0 || trace.noReferencesFound, trace.confidence, trace.difficulty, trace.ease, trace.directness].filter(Boolean).length
  return <div className="flex h-full min-h-0 flex-col bg-paper">
    <div className="border-b border-line p-5"><div className="flex items-center justify-between"><div><p className="text-[10px] font-bold uppercase tracking-[.16em] text-amber">Questionário do trace</p><h2 className="mt-1 font-display text-2xl">Perguntas 1 a 4</h2></div><div className="text-right"><div className="text-sm font-bold text-forest">{answered}/5</div><div className="text-[10px] uppercase tracking-wider text-black/40">campos</div></div></div><Progress value={answered / 5 * 100} className="mt-4" /></div>
    <div className="flex-1 overflow-y-auto p-4 sm:p-5">
      <div className="mb-4 rounded-xl bg-[#edf1ea] p-3 text-xs leading-relaxed text-black/55"><strong className="text-forest">Como responder:</strong> clique em uma linha do trace; use Shift+clique para selecionar um intervalo e adicione a referência. A ferramenta registra tempos e interações automaticamente.</div>
      <div className="space-y-4">
        <section className="rounded-2xl border border-line bg-white p-4"><div className="flex items-start gap-3"><span className="grid size-8 shrink-0 place-items-center rounded-full bg-forest text-xs font-bold text-white">1</span><div><h3 className="text-sm font-bold">Esforço para auditar</h3><p className="mt-1 text-xs leading-relaxed text-black/50">Aponte para a primeira linha do log que deixa claro para você em qual atividade o agente está trabalhando e qual o objetivo dele.</p></div></div><div className="mt-4"><FieldLabel>Referências</FieldLabel>{trace.evidenceReferences.length ? <div className="flex flex-wrap gap-2">{trace.evidenceReferences.map((reference) => <div key={reference.id} className="flex items-center gap-2 rounded-lg border border-[#b9cfb5] bg-[#edf4ea] px-3 py-2 text-xs font-semibold text-forest"><span>{reference.startLine === reference.endLine ? `Linha ${reference.startLine}` : `Linhas ${reference.startLine}–${reference.endLine}`}</span><button onClick={() => onRemoveReference(reference.id)} aria-label="Remover referência"><X size={13} /></button></div>)}</div> : <div className="rounded-xl border border-dashed border-line bg-[#faf9f5] p-4 text-center text-xs text-black/45"><MousePointer2 className="mx-auto mb-2 text-amber" size={18} />{trace.noReferencesFound ? 'Você indicou que não encontrou referências.' : 'Selecione linhas no trace à esquerda.'}</div>}</div><button type="button" aria-pressed={Boolean(trace.noReferencesFound)} onClick={onNoReferences} className={cn('mt-3 w-full rounded-xl border px-3 py-2.5 text-left text-xs font-semibold transition', trace.noReferencesFound ? 'border-forest bg-[#e8f0e9] text-forest' : 'border-line text-black/60 hover:border-moss')}>Não encontrei referências</button></section>

        <section className="rounded-2xl border border-line bg-white p-4"><div className="mb-4 flex items-start gap-3"><span className="grid size-8 shrink-0 place-items-center rounded-full bg-forest text-xs font-bold text-white">2</span><div><h3 className="text-sm font-bold">Confiança subjetiva</h3><p className="mt-1 text-xs text-black/50">Avalie sua confiança e a carga cognitiva percebida.</p></div></div><div className="space-y-5"><div><FieldLabel>O quão confiante você ficou da sua resposta?</FieldLabel><Scale value={trace.confidence} onChange={(confidence) => onUpdate({ confidence }, 'M2.1')} low="Nada confiante" high="Muito confiante" /></div><div><FieldLabel>Qual a sua percepção de esforço cognitivo para encontrar o resultado?</FieldLabel><Scale value={trace.difficulty} onChange={(difficulty) => onUpdate({ difficulty }, 'M2.2')} low="Muito baixa" high="Muito alta" /></div></div></section>

        <section className="rounded-2xl border border-line bg-white p-4"><div className="mb-4 flex items-start gap-3"><span className="grid size-8 shrink-0 place-items-center rounded-full bg-forest text-xs font-bold text-white">3</span><div><h3 className="text-sm font-bold">Localização da evidência</h3><p className="mt-1 text-xs text-black/50">Avalie como foi encontrar essa informação no log.</p></div></div><div><FieldLabel>Qual a sua percepção do quão fácil foi encontrar essa informação?</FieldLabel><Scale value={trace.ease} onChange={(ease) => onUpdate({ ease }, 'M3.3')} low="Muito difícil" high="Muito fácil" /></div></section>

        <section className="rounded-2xl border border-line bg-white p-4"><div className="mb-4 flex items-start gap-3"><span className="grid size-8 shrink-0 place-items-center rounded-full bg-forest text-xs font-bold text-white">4</span><div><h3 className="text-sm font-bold">Inferência necessária</h3><p className="mt-1 text-xs text-black/50">Indique se a resposta aparece diretamente no log ou exige combinar partes dele.</p></div></div><FieldLabel>A resposta estava…</FieldLabel><div className="grid grid-cols-2 gap-2">{[['direct', 'Explícita'], ['inferred', 'Dispersa']].map(([value, label]) => <button type="button" key={value} onClick={() => onUpdate({ directness: value as TraceResponse['directness'] }, 'M4.1')} className={cn('rounded-xl border p-3 text-left text-xs font-semibold transition', trace.directness === value ? 'border-forest bg-[#e8f0e9] text-forest' : 'border-line hover:border-moss')}>{label}</button>)}</div></section>
      </div>
      <div className="mt-4"><FieldLabel optional>Observações sobre o trace</FieldLabel><textarea value={trace.notes} onChange={(e) => onUpdate({ notes: e.target.value })} rows={3} className="w-full rounded-xl border border-line bg-white p-3 text-sm outline-none focus:border-forest" placeholder="Registre algo que não foi coberto acima…" /></div>
    </div>
    <div className="border-t border-line bg-paper p-4"><Button className="w-full" disabled={!canComplete} onClick={onComplete}>{canComplete ? 'Concluir este trace' : `Complete os ${5 - answered} campos restantes`} <ArrowRight size={15} /></Button></div>
  </div>
}

function Experiment({ manifest, session, setSession, onExit }: { manifest: Manifest; session: SessionState; setSession: (state: SessionState) => void; onExit: () => void }) {
  const sequence = latinSquare[session.group].map((harness, index) => manifest.entries.find((entry) => entry.harness === harness && entry.task === session.taskSet[index] && entry.repetition === session.repetition)).filter(Boolean) as TraceEntry[]
  const entry = sequence[session.currentIndex]
  const [content, setContent] = useState('')
  const [elapsed, setElapsed] = useState(0)
  const [loading, setLoading] = useState(true)
  const [selectedLines, setSelectedLines] = useState<number[]>([])
  const lastNavigationAt = useRef(0)
  const storedTrace = session.traceResponses[entry.id]
  const trace: TraceResponse = {
    ...emptyTrace(entry.id),
    ...storedTrace,
    evidenceReferences: storedTrace?.evidenceReferences ?? [],
    telemetry: storedTrace?.telemetry ?? [],
  }
  const traceRef = useRef(trace)
  traceRef.current = trace

  useEffect(() => {
    window.scrollTo(0, 0)
    setSelectedLines([])
    if (!storedTrace?.evidenceReferences || !storedTrace?.telemetry) setSession({ ...session, traceResponses: { ...session.traceResponses, [entry.id]: trace } })
    setLoading(true); fetch(entry.url).then((response) => response.text()).then(setContent).finally(() => setLoading(false))
  }, [entry.id]) // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { const timer = window.setInterval(() => setElapsed(Math.floor((Date.now() - new Date(trace.startedAt).getTime()) / 1000)), 1000); return () => clearInterval(timer) }, [trace.startedAt])

  const updateTrace = (next: TraceResponse) => { traceRef.current = next; setSession({ ...session, traceResponses: { ...session.traceResponses, [entry.id]: next } }) }
  const eventAt = () => ({ at: new Date().toISOString(), deltaMs: Date.now() - new Date(trace.startedAt).getTime() })
  const recordTelemetry = (type: TelemetryEvent['type'], detail?: TelemetryEvent['detail']) => {
    const now = Date.now()
    if (type === 'scroll' && now - lastNavigationAt.current < 750) return
    if (type === 'scroll') lastNavigationAt.current = now
    const current = traceRef.current
    const event: TelemetryEvent = { type, ...eventAt(), detail }
    updateTrace({ ...current, telemetry: [...current.telemetry, event], positionChanges: current.positionChanges + (type === 'scroll' || type === 'search_navigation' ? 1 : 0) })
  }
  const addReferences = (ranges: Array<{ startLine: number; endLine: number }>) => {
    const current = traceRef.current
    const timing = eventAt()
    const additions: EvidenceReference[] = ranges.map(({ startLine, endLine }, index) => ({ id: `${startLine}-${endLine}-${Date.now()}-${index}`, startLine, endLine, addedAt: timing.at, deltaMs: timing.deltaMs }))
    const event: TelemetryEvent = { type: 'evidence_added', ...timing, detail: { ranges: ranges.length, selectedLines: ranges.reduce((total, range) => total + range.endLine - range.startLine + 1, 0) } }
    updateTrace({ ...current, firstEvidenceAt: current.firstEvidenceAt ?? timing.at, evidenceInteractions: current.evidenceInteractions + ranges.length, evidenceReferences: [...current.evidenceReferences, ...additions], noReferencesFound: false, telemetry: [...current.telemetry, event] })
  }
  const removeReference = (id: string) => {
    const current = traceRef.current
    const reference = current.evidenceReferences.find((item) => item.id === id)
    const event: TelemetryEvent = { type: 'evidence_removed', ...eventAt(), detail: reference ? { startLine: reference.startLine, endLine: reference.endLine } : undefined }
    updateTrace({ ...current, evidenceReferences: current.evidenceReferences.filter((item) => item.id !== id), telemetry: [...current.telemetry, event] })
  }
  const updateResponse = (patch: Partial<TraceResponse>, metric?: string) => {
    const current = traceRef.current
    const event: TelemetryEvent | null = metric ? { type: 'answer_changed', ...eventAt(), detail: { metric } } : null
    updateTrace({ ...current, ...patch, telemetry: event ? [...current.telemetry, event] : current.telemetry })
  }
  const answered = (trace.evidenceReferences.length > 0 || trace.noReferencesFound) && trace.confidence && trace.difficulty && trace.ease && trace.directness
  const initiallyViewedLines = trace.telemetry.filter((event) => event.type === 'lines_viewed').flatMap((event) => Array.isArray(event.detail?.lines) ? event.detail.lines : [])
  const completeTrace = () => {
    const now = new Date().toISOString(); const nextResponses = { ...session.traceResponses, [entry.id]: { ...trace, readingCompletedAt: trace.readingCompletedAt ?? now, completedAt: now } }
    setSession({ ...session, traceResponses: nextResponses, currentIndex: session.currentIndex + 1, completedAt: session.currentIndex === sequence.length - 1 ? now : undefined })
    window.scrollTo(0, 0)
  }

  return <div className="flex h-screen flex-col overflow-hidden bg-canvas text-ink">
    <header className="flex h-[72px] shrink-0 items-center gap-5 border-b border-line bg-paper px-4 sm:px-6"><button onClick={onExit} aria-label="Voltar ao início" className="rounded-lg p-2 hover:bg-black/5"><ArrowLeft size={18} /></button><Logo /><div className="hidden h-7 w-px bg-line sm:block" /><div className="min-w-0 flex-1"><div className="flex items-center gap-2 text-xs text-black/45"><span>Sessão {session.participantCode}</span><span>·</span><span>Trace {session.currentIndex + 1} de {sequence.length}</span></div><Progress value={(session.currentIndex / sequence.length) * 100} className="mt-2 max-w-sm" /></div><div className="hidden items-center gap-2 rounded-xl border border-line px-3 py-2 font-mono text-sm text-black/55 sm:flex"><Clock3 size={15} /> {formatDuration(elapsed)}</div></header>
    <div className="flex shrink-0 items-center gap-3 border-b border-line bg-[#f7f5ef] px-4 py-2.5 sm:px-6"><span aria-hidden="true" className={cn('h-6 w-8 shrink-0 rounded-md', entry.harness === 'bdi' ? 'bg-[#e9e2f5]' : entry.harness === 'codex' ? 'bg-[#dcece5]' : 'bg-[#f8e5d8]')} /><span className="truncate text-sm font-semibold">{labelTask(entry.task)}</span><span className="hidden text-xs text-black/35 sm:inline">· {entry.repetition} · {entry.model}</span><span className="ml-auto text-xs text-black/35">{content.split('\n').length.toLocaleString('pt-BR')} linhas</span></div>
    <main className="grid min-h-0 flex-1 lg:grid-cols-[minmax(0,1.35fr)_minmax(390px,.65fr)]">
      <section className="min-h-0 border-r border-line">{loading ? <div className="grid h-full place-items-center bg-[#101713] text-sm text-white/45">Carregando trace…</div> : <LogViewer key={entry.id} content={content} references={trace.evidenceReferences} selectedLines={selectedLines} onSelectionChange={setSelectedLines} onAddReferences={addReferences} onTelemetry={recordTelemetry} initialViewedLines={initiallyViewedLines} />}</section>
      <aside className="min-h-0"><Questionnaire key={entry.id} trace={trace} onUpdate={updateResponse} onNoReferences={() => { setSelectedLines([]); updateResponse({ noReferencesFound: !trace.noReferencesFound, evidenceReferences: [] }, 'M1.1') }} onRemoveReference={removeReference} onComplete={completeTrace} canComplete={Boolean(answered)} /></aside>
    </main>
  </div>
}

function Completion({ session, manifest, onReset }: { session: SessionState; manifest: Manifest; onReset: () => void }) {
  const sequence = latinSquare[session.group].map((harness, index) => manifest.entries.find((entry) => entry.harness === harness && entry.task === session.taskSet[index] && entry.repetition === session.repetition)).filter(Boolean) as TraceEntry[]
  const payload = { schemaVersion: 4, exportedAt: new Date().toISOString(), experiment: 'sbench-latin-square-q1-q4', session, traces: sequence, derivedMetrics: Object.fromEntries(Object.entries(session.traceResponses).map(([traceId, response]) => [traceId, deriveMetrics(response)])) }
  const [submission, setSubmission] = useState<'sending' | 'saved' | 'failed'>('sending')
  const [submissionMessage, setSubmissionMessage] = useState('Salvando no banco de dados…')
  const submit = async () => {
    setSubmission('sending'); setSubmissionMessage('Salvando no banco de dados…')
    try {
      const response = await fetch('/api/experiment-sessions', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
      if (!response.ok) { const body = await response.json().catch(() => ({})); throw new Error(body.error ?? `HTTP ${response.status}`) }
      setSubmission('saved'); setSubmissionMessage('Sessão salva no SQLite com sucesso.')
    } catch (error) {
      setSubmission('failed'); setSubmissionMessage(`Não foi possível salvar: ${error instanceof Error ? error.message : 'erro desconhecido'}. Seus dados continuam neste navegador.`)
    }
  }
  useEffect(() => { void submit() }, []) // eslint-disable-line react-hooks/exhaustive-deps
  const download = () => { const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }); const url = URL.createObjectURL(blob); const anchor = document.createElement('a'); anchor.href = url; anchor.download = `sbench-${session.participantCode}-${new Date().toISOString().slice(0, 10)}.json`; anchor.click(); URL.revokeObjectURL(url) }
  const totalSeconds = Object.values(session.traceResponses).reduce((sum, trace) => sum + (trace.completedAt ? (new Date(trace.completedAt).getTime() - new Date(trace.startedAt).getTime()) / 1000 : 0), 0)
  return <div className="min-h-screen bg-canvas px-6 py-8 text-ink"><header className="mx-auto flex max-w-5xl justify-between"><Logo /><div className="text-sm text-black/45">Participante {session.participantCode}</div></header><main className="mx-auto mt-16 max-w-3xl text-center"><div className="mx-auto grid size-20 place-items-center rounded-full bg-forest text-white shadow-card"><Check size={34} /></div><p className="mt-8 text-xs font-bold uppercase tracking-[.2em] text-amber">Sessão concluída</p><h1 className="mt-3 font-display text-5xl">Obrigado pela sua análise.</h1><p className="mx-auto mt-4 max-w-xl text-black/55">As sete avaliações foram concluídas. O envio ao banco acontece automaticamente e o JSON continua disponível como cópia de segurança.</p><div className={cn('mx-auto mt-5 flex max-w-xl items-center justify-center gap-2 rounded-xl border px-4 py-3 text-sm', submission === 'saved' ? 'border-[#b9cfb5] bg-[#edf4ea] text-forest' : submission === 'failed' ? 'border-red-200 bg-red-50 text-red-800' : 'border-line bg-paper text-black/55')}>{submission === 'sending' && <LoaderCircle className="animate-spin" size={16} />}{submission === 'saved' && <CheckCircle2 size={16} />}{submission === 'failed' && <X size={16} />}<span>{submissionMessage}</span>{submission === 'failed' && <button onClick={() => void submit()} className="ml-2 inline-flex items-center gap-1 font-semibold underline"><RefreshCw size={13} /> Tentar novamente</button>}</div><div className="mt-8 grid grid-cols-3 overflow-hidden rounded-2xl border border-line bg-paper text-left shadow-card">{[[String(sequence.length), 'traces avaliados'], ['1–4', 'por trace'], [formatDuration(totalSeconds), 'tempo total']].map(([value, label]) => <div className="border-r border-line p-5 last:border-r-0" key={label}><div className="font-display text-3xl text-forest">{value}</div><div className="mt-1 text-xs text-black/40">{label}</div></div>)}</div><div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row"><Button onClick={download}><Download size={17} /> Baixar respostas (.json)</Button><Button variant="outline" onClick={() => navigator.clipboard.writeText(JSON.stringify(payload))}><ClipboardCopy size={16} /> Copiar JSON</Button></div><button onClick={onReset} className="mt-10 text-xs text-black/40 underline underline-offset-4 hover:text-ink">Encerrar e limpar este dispositivo</button></main></div>
}

export default function App() {
  const [manifest, setManifest] = useState<Manifest | null>(null)
  const [session, setSessionState] = useState<SessionState | null>(() => { try { const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null'); return stored ? { ...stored, sessionId: stored.sessionId ?? newSessionId() } : null } catch { return null } })
  const [screen, setScreen] = useState<'welcome' | 'experiment' | 'complete'>('welcome')
  useEffect(() => { fetch('/data/manifest.json').then((response) => { if (!response.ok) throw new Error('manifest'); return response.json() }).then(setManifest).catch(() => setManifest({ generatedAt: '', entries: [] })) }, [])
  const setSession = (state: SessionState) => { setSessionState(state); localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); if (state.completedAt) setScreen('complete') }
  const reset = () => { localStorage.removeItem(STORAGE_KEY); setSessionState(null); setScreen('welcome') }
  if (!manifest) return <div className="grid min-h-screen place-items-center bg-canvas text-sm text-black/45">Preparando o estudo…</div>
  if (!manifest.entries.length) return <div className="grid min-h-screen place-items-center bg-canvas p-6 text-center"><div><FileText className="mx-auto text-amber" size={36} /><h1 className="mt-4 font-display text-3xl">Catálogo de traces não encontrado</h1><p className="mt-2 text-sm text-black/50">Execute <code className="rounded bg-white px-2 py-1">npm run prepare-data</code> nesta pasta e recarregue.</p></div></div>
  if (screen === 'complete' && session) return <Completion session={session} manifest={manifest} onReset={reset} />
  if (screen === 'experiment' && session) {
    if (session.currentIndex >= session.taskSet.length) return <Completion session={session} manifest={manifest} onReset={reset} />
    return <Experiment manifest={manifest} session={session} setSession={setSession} onExit={() => setScreen('welcome')} />
  }
  return <Welcome manifest={manifest} restored={session} onResume={() => setScreen(session?.completedAt ? 'complete' : 'experiment')} onReset={reset} onStart={(state) => { setSession(state); setScreen('experiment') }} />
}
