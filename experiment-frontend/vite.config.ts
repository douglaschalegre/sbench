import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // Catalog and logs are imported into Turso and served through authenticated routes.
  publicDir: false,
  server: {
    host: '127.0.0.1',
    port: 4173,
    proxy: { '/api': 'http://127.0.0.1:8765' },
  },
})
