import { lazy, StrictMode, Suspense } from 'react'
import { createRoot } from 'react-dom/client'
const App = lazy(() => import('./App'))
const SetupAccess = lazy(() => import('./SetupAccess'))
import './index.css'

createRoot(document.getElementById('root')!).render(<StrictMode><Suspense fallback={<p className="p-8">Carregando…</p>}>{window.location.pathname.replace(/\/+$/, '') === '/setup' ? <SetupAccess /> : <App />}</Suspense></StrictMode>)
