import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';
import { Button } from './components/ui';
import { AdminApiError, adminRequest } from './adminApi';
import { defaultTasks, latinSquare, harnessLabel } from './data';
import type { GroupNumber } from './data';
import { labelTask } from './lib/utils';
import type { TraceEntry } from './types';

type Invitation = {
  invitationId: string; sessionId: string; participantCode: string; group: GroupNumber;
  runId: string; repetition: string; taskSet: string[]; createdAt: string; expiresAt: string;
  startedAt: string | null; completedAt: string | null; revokedAt: string | null;
};
type Config = Pick<Invitation, 'participantCode' | 'group' | 'runId' | 'repetition' | 'taskSet' | 'expiresAt'>;
type IssuedCode = { invitationId: string; code: string };

function localDate(value: string) {
  const date = new Date(value);
  return new Date(date.getTime() - date.getTimezoneOffset() * 60_000).toISOString().slice(0, 16);
}
function initialTasks(entries: TraceEntry[]) {
  const tasks = [...new Set(entries.map((entry) => entry.task))];
  return defaultTasks.every((task) => tasks.includes(task)) ? [...defaultTasks] : tasks.slice(0, 3);
}
function emptyConfig(entries: TraceEntry[]): Config {
  const runId = [...new Set(entries.map((entry) => entry.runId))].sort().at(-1) ?? '';
  const run = entries.filter((entry) => entry.runId === runId);
  return { participantCode: '', group: 1, runId, repetition: run[0]?.repetition ?? '', taskSet: initialTasks(run), expiresAt: localDate(new Date(Date.now() + 14 * 86400_000).toISOString()) };
}
function status(invitation: Invitation) {
  if (invitation.revokedAt) return 'Revogado';
  if (invitation.completedAt) return 'Concluído';
  if (Date.parse(invitation.expiresAt) <= Date.now()) return 'Expirado';
  return invitation.startedAt ? 'Iniciado' : 'Aguardando acesso';
}
const inputClass = 'mt-2 h-11 w-full rounded-xl border border-line bg-white px-3 text-sm focus:outline-forest disabled:bg-canvas';

export default function Setup({ onExpired, onLogout }: { onExpired: () => void; onLogout: () => void }) {
  const [entries, setEntries] = useState<TraceEntry[]>([]);
  const [invitations, setInvitations] = useState<Invitation[]>([]);
  const [config, setConfig] = useState<Config>(() => emptyConfig([]));
  const [editing, setEditing] = useState<string | null>(null);
  const [issued, setIssued] = useState<IssuedCode | null>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  useEffect(() => {
    Promise.all([
      adminRequest<{ entries: TraceEntry[] }>('catalog'),
      adminRequest<{ invitations: Invitation[] }>('invitations'),
    ]).then(([catalog, list]) => {
      setEntries(catalog.entries); setConfig(emptyConfig(catalog.entries)); setInvitations(list.invitations);
    }).catch((cause) => {
      if (cause instanceof AdminApiError && cause.status === 401) onExpired();
      else setError(cause instanceof Error ? cause.message : 'Não foi possível carregar os convites.');
    }).finally(() => setLoading(false));
  }, [onExpired]);
  const handleError = (cause: unknown) => {
    if (cause instanceof AdminApiError && cause.status === 401) onExpired();
    else setError(cause instanceof Error ? cause.message : 'Não foi possível concluir a operação.');
  };
  const refresh = async () => setInvitations((await adminRequest<{ invitations: Invitation[] }>('invitations')).invitations);
  const run = entries.filter((entry) => entry.runId === config.runId);
  const repetitions = [...new Set(run.map((entry) => entry.repetition))].sort();
  const tasks = [...new Set(run.filter((entry) => entry.repetition === config.repetition).map((entry) => entry.task))].sort();
  const sequence = latinSquare[config.group].map((harness, index) => run.filter((entry) => entry.repetition === config.repetition && entry.task === config.taskSet[index] && entry.harness === harness));
  const valid = /^[A-Za-z0-9_-]{3,64}$/.test(config.participantCode) && config.taskSet.length === 3 && new Set(config.taskSet).size === 3 && sequence.every((matches) => matches.length === 1) && Date.parse(config.expiresAt) > Date.now();
  const save = async (event: FormEvent) => {
    event.preventDefault(); setBusy(true); setError(''); setNotice('');
    try {
      const payload = { ...config, expiresAt: new Date(config.expiresAt).toISOString() };
      const result = await adminRequest<IssuedCode>(editing ? `invitations/${editing}` : 'invitations', editing ? 'PATCH' : 'POST', payload);
      if (!editing) setIssued(result);
      setNotice(editing ? 'Convite atualizado. O código de acesso continua o mesmo.' : 'Convite criado. Guarde o código abaixo para enviar ao participante.');
      setEditing(null); setConfig(emptyConfig(entries));
      await refresh();
    } catch (cause) { handleError(cause); }
    finally { setBusy(false); }
  };
  const action = async (invitation: Invitation, operation: 'revoke' | 'delete' | 'rotate-code') => {
    const messages = { revoke: 'Revogar este convite e bloquear o acesso do participante?', delete: 'Excluir este convite que ainda não foi utilizado?', 'rotate-code': 'Gerar outro código? O código anterior deixará de funcionar.' };
    if (!window.confirm(messages[operation])) return;
    setBusy(true); setError(''); setNotice('');
    try {
      const result = await adminRequest<IssuedCode>(`invitations/${invitation.invitationId}${operation === 'delete' ? '' : `/${operation}`}`, operation === 'delete' ? 'DELETE' : 'POST');
      if (operation === 'rotate-code') setIssued(result);
      else if (issued?.invitationId === invitation.invitationId) setIssued(null);
      if (editing === invitation.invitationId) { setEditing(null); setConfig(emptyConfig(entries)); }
      setNotice(operation === 'revoke' ? 'Convite revogado.' : operation === 'delete' ? 'Convite excluído.' : 'Novo código gerado. Guarde o código abaixo.');
      await refresh();
    } catch (cause) { handleError(cause); }
    finally { setBusy(false); }
  };
  const logout = async () => {
    setBusy(true); setError('');
    try { await adminRequest('logout', 'POST'); onLogout(); }
    catch (cause) { handleError(cause); }
    finally { setBusy(false); }
  };
  const edit = (invitation: Invitation) => {
    setEditing(invitation.invitationId); setError(''); setNotice('');
    setConfig({ participantCode: invitation.participantCode, group: invitation.group, runId: invitation.runId, repetition: invitation.repetition, taskSet: [...invitation.taskSet], expiresAt: localDate(invitation.expiresAt) });
    document.getElementById('invite-form')?.scrollIntoView({ behavior: 'smooth' });
  };
  return <div className="min-h-screen bg-canvas text-ink">
    <header className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-6 lg:px-10">
      <a href="/" className="font-display text-2xl text-forest">SBench</a>
      <Button variant="ghost" disabled={busy} onClick={logout}>Sair do administrador</Button>
    </header>
    <main className="mx-auto max-w-7xl px-6 pb-12 lg:px-10">
      <h1 className="font-display text-4xl">Participantes e convites</h1>
      <p className="mt-3 max-w-2xl text-sm text-black/60">Prepare cada participação antes da sessão. O código de acesso leva o participante ao tutorial com a configuração definida aqui.</p>
      {error && <p role="alert" className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800">{error}</p>}
      {notice && <p role="status" className="mt-6 text-sm font-semibold text-forest">{notice}</p>}
      {issued && <section aria-label="Código do convite" className="mt-6 rounded-2xl border border-forest bg-paper p-5">
        <h2 className="font-display text-2xl">Código para o participante</h2>
        <p className="mt-2 text-sm text-black/60">Este código só aparece ao ser gerado. Guarde-o antes de sair da página.</p>
        <label htmlFor="issued-code" className="mt-4 block text-sm font-semibold">Código de acesso</label>
        <input id="issued-code" readOnly value={issued.code} onFocus={(event) => event.target.select()} className={inputClass} />
        <p className="mt-3 break-all text-sm">Endereço: {window.location.origin}/</p>
        <Button className="mt-4" variant="outline" onClick={async () => {
          try { await navigator.clipboard.writeText(`Acesse ${window.location.origin}/\nCódigo de acesso: ${issued.code}`); setNotice('Endereço e código copiados.'); }
          catch { setError('Não foi possível copiar. Selecione e copie o código acima.'); }
        }}>Copiar endereço e código</Button>
      </section>}
      {loading ? <p className="mt-8" role="status">Carregando convites…</p> : <div className="mt-8 grid items-start gap-8 xl:grid-cols-[370px_1fr]">
        <form id="invite-form" onSubmit={save} className="rounded-2xl border border-line bg-paper p-6">
          <h2 className="font-display text-2xl">{editing ? 'Editar convite' : 'Novo convite'}</h2>
          {!entries.length && <p className="mt-3 text-sm text-red-800">O catálogo está vazio. Importe os traces no banco antes de criar convites.</p>}
          <fieldset disabled={busy || !entries.length} className="mt-5 space-y-4">
            <label className="block text-sm font-semibold" htmlFor="participant-code">Código do participante
              <input id="participant-code" required minLength={3} maxLength={64} pattern={"[A-Za-z0-9_\\-]+"} placeholder="P-001" value={config.participantCode} onChange={(event) => setConfig({ ...config, participantCode: event.target.value })} className={inputClass} />
            </label>
            <label className="block text-sm font-semibold" htmlFor="participant-group">Posição no quadrado latino
              <select id="participant-group" value={config.group} onChange={(event) => setConfig({ ...config, group: Number(event.target.value) as GroupNumber })} className={inputClass}>{[1, 2, 3].map((group) => <option key={group} value={group}>Posição {group}</option>)}</select>
            </label>
            <label className="block text-sm font-semibold" htmlFor="participant-run">Execução e modelo
              <select id="participant-run" value={config.runId} onChange={(event) => {
                const next = entries.filter((entry) => entry.runId === event.target.value);
                setConfig({ ...config, runId: event.target.value, repetition: next[0]?.repetition ?? '', taskSet: initialTasks(next) });
              }} className={inputClass}>{[...new Set(entries.map((entry) => entry.runId))].sort().reverse().map((runId) => <option key={runId} value={runId}>{runId} · {[...new Set(entries.filter((entry) => entry.runId === runId).map((entry) => entry.model))].join(', ')}</option>)}</select>
            </label>
            <label className="block text-sm font-semibold" htmlFor="participant-repetition">Réplica
              <select id="participant-repetition" value={config.repetition} onChange={(event) => setConfig({ ...config, repetition: event.target.value })} className={inputClass}>{repetitions.map((repetition) => <option key={repetition}>{repetition}</option>)}</select>
            </label>
            {[0, 1, 2].map((index) => <label key={index} className="block text-sm font-semibold" htmlFor={`participant-task-${index}`}>Tarefa {index + 1} · {harnessLabel[latinSquare[config.group][index]]}
              <select id={`participant-task-${index}`} required value={config.taskSet[index] ?? ''} onChange={(event) => { const taskSet = [...config.taskSet]; taskSet[index] = event.target.value; setConfig({ ...config, taskSet }); }} className={inputClass}>
                <option value="" disabled>Selecione uma tarefa</option>
                {tasks.map((task) => <option key={task} value={task}>{labelTask(task)}</option>)}
              </select>
            </label>)}
            <label className="block text-sm font-semibold" htmlFor="participant-expiry">Válido até
              <input id="participant-expiry" type="datetime-local" required value={config.expiresAt} onChange={(event) => setConfig({ ...config, expiresAt: event.target.value })} className={inputClass} />
            </label>
            <p className="text-xs text-black/55">Horário local do seu dispositivo. Use três tarefas diferentes com traces disponíveis na execução e réplica selecionadas.</p>
            {!sequence.every((matches) => matches.length === 1) && <p className="text-sm text-red-800">A seleção não contém os três traces necessários.</p>}
            <Button type="submit" disabled={!valid} className="w-full">{busy ? 'Salvando…' : editing ? 'Salvar alterações' : 'Criar convite'}</Button>
          </fieldset>
          {editing && <Button type="button" variant="ghost" className="mt-3 w-full" disabled={busy} onClick={() => { setEditing(null); setConfig(emptyConfig(entries)); }}>Cancelar edição</Button>}
        </form>
        <section aria-label="Convites cadastrados" className="min-w-0">
          <h2 className="font-display text-2xl">Convites cadastrados ({invitations.length})</h2>
          <p className="mt-2 text-sm text-black/55">Após o primeiro acesso, a configuração fica fixa para preservar as respostas. Você ainda pode revogar o acesso.</p>
          {!invitations.length && <p className="mt-6 rounded-xl border border-dashed border-line p-6 text-sm text-black/60">Nenhum convite criado. Configure a primeira participação no formulário.</p>}
          <ul className="mt-5 divide-y divide-line rounded-2xl border border-line bg-paper">
            {invitations.map((invitation) => <li key={invitation.invitationId} className="p-5">
              <div className="flex flex-wrap items-baseline justify-between gap-2"><h3 className="text-lg font-semibold">{invitation.participantCode}</h3><span className="rounded-full bg-canvas px-3 py-1 text-xs font-semibold">{status(invitation)}</span></div>
              <p className="mt-2 break-all text-sm text-black/65">Posição {invitation.group} · {invitation.runId} · {invitation.repetition}</p>
              <ol className="mt-3 list-inside list-decimal text-sm text-black/65">{invitation.taskSet.map((task, index) => <li key={index}>{labelTask(task)} · {harnessLabel[latinSquare[invitation.group][index]]}</li>)}</ol>
              <p className="mt-3 text-xs text-black/55">Validade: {new Date(invitation.expiresAt).toLocaleString()}{invitation.startedAt ? ` · Primeiro acesso: ${new Date(invitation.startedAt).toLocaleString()}` : ''}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                <Button variant="outline" disabled={busy || !!invitation.startedAt || !!invitation.completedAt || !!invitation.revokedAt} onClick={() => edit(invitation)}>Editar</Button>
                <Button variant="ghost" disabled={busy || !!invitation.startedAt || !!invitation.completedAt || !!invitation.revokedAt} onClick={() => action(invitation, 'rotate-code')}>Gerar novo código</Button>
                <Button variant="ghost" disabled={busy || !!invitation.revokedAt} onClick={() => action(invitation, 'revoke')}>Revogar</Button>
                <Button variant="danger" disabled={busy || !!invitation.startedAt || !!invitation.completedAt} onClick={() => action(invitation, 'delete')}>Excluir</Button>
              </div>
            </li>)}
          </ul>
        </section>
      </div>}
    </main>
  </div>;
}
