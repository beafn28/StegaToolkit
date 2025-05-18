import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api/ocr': {
        target: 'https://stegatoolkit-backend.onrender.com',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, '')
      },
      '/api/ocultar': {
        target: 'https://stegatoolkit-backend.onrender.com',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, '')
      },
      '/api/extraer': {
        target: 'https://stegatoolkit-backend.onrender.com',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, '')
      },
      '/api/historial': {
        target: 'https://stegatoolkit-backend.onrender.com',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, '')
      },
      '/api/rgb_split': {
        target: 'https://stegatoolkit-backend.onrender.com',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, '')
      },
      '/api/ela': {
        target: 'https://stegatoolkit-backend.onrender.com',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, '')
      },
      '/api/analisis_forense': {
        target: 'https://stegatoolkit-backend.onrender.com',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, '')
      }
    }
  }
})