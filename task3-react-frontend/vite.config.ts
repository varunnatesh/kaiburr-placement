import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8001/api/v1/namespaces/default/services/task-manager:8080/proxy',
        changeOrigin: true,
        rewrite: (path) => path,
      }
    }
  }
})
