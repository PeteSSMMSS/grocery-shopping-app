import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    // Disable PWA/Service Worker in local builds to avoid caching old API bases
    VitePWA({
      registerType: 'autoUpdate',
      injectRegister: false,
      disable: true,
      manifest: false,
      workbox: undefined
    })
  ],
  server: {
    port: 5173,
    host: true
  },
  preview: {
    port: 80,
    host: true
  }
})
