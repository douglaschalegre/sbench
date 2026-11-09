import { lazy, Suspense, useCallback, useEffect, useState } from 'react';
import type { FormEvent } from 'react';
import { Button } from './components/ui';
import { AdminApiError, adminRequest } from './adminApi';

const Setup = lazy(() => import('./Setup'));

export default function SetupAccess() {
  const [authenticated, setAuthenticated] = useState(false);
  const [checking, setChecking] = useState(true);
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const expired = useCallback(() => { setAuthenticated(false); setError('Sua sessão expirou. Entre novamente.'); }, []);
  useEffect(() => {
    adminRequest('session').then(() => setAuthenticated(true)).catch((cause) => {
      if (!(cause instanceof AdminApiError) || cause.status !== 401) setError(cause instanceof Error ? cause.message : 'Não foi possível conectar.');
    }).finally(() => setChecking(false));
  }, []);
  const login = async (event: FormEvent) => {
    event.preventDefault();
    setChecking(true); setError('');
    try {
      await adminRequest('login', 'POST', { password });
      setPassword(''); setAuthenticated(true);
    } catch (cause) { setError(cause instanceof Error ? cause.message : 'Não foi possível entrar.'); }
    finally { setChecking(false); }
  };
  if (authenticated) return <Suspense fallback={<p className="p-8">Carregando configuração…</p>}><Setup onExpired={expired} onLogout={() => setAuthenticated(false)} /></Suspense>;
  return <main className="grid min-h-screen place-items-center bg-canvas p-6 text-ink">
    <form onSubmit={login} className="w-full max-w-md rounded-[28px] border border-line bg-paper p-8 shadow-card">
      <a href="/" className="text-sm font-semibold text-forest">SBench</a>
      <h1 className="mt-8 font-display text-3xl">Administrar o experimento</h1>
      <p className="mt-3 text-sm text-black/60">Entre para configurar participantes e gerenciar convites.</p>
      <label className="mt-6 block text-sm font-semibold" htmlFor="admin-password">Senha de administrador</label>
      <input id="admin-password" type="password" autoComplete="current-password" required value={password} onChange={(event) => setPassword(event.target.value)} className="mt-2 h-12 w-full rounded-xl border border-line bg-white px-4 focus:outline-forest" />
      {error && <p role="alert" className="mt-3 text-sm text-red-700">{error}</p>}
      <Button type="submit" disabled={checking || !password} className="mt-6 w-full">{checking ? 'Verificando acesso…' : 'Entrar'}</Button>
    </form>
  </main>;
}
