import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/ocr': 'http://localhost:8000',
      '/ocultar': 'http://localhost:8000',
      '/extraer': 'http://localhost:8000',
      '/historial': 'http://localhost:8000',
      '/rgb_split': 'http://localhost:8000',
      '/ela': 'http://localhost:8000',
      '/analisis_forense': 'http://localhost:8000',
    }
  }
})