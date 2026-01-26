/**
 * Vite Configuration
 *
 * Vite is a modern build tool that provides:
 * - Instant server start (no bundling in dev)
 * - Lightning-fast HMR (Hot Module Replacement)
 * - Optimized production builds with Rollup
 *
 * @see https://vitejs.dev/config/
 */
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  // Plugins
  plugins: [
    // React plugin enables:
    // - Fast Refresh for instant feedback
    // - JSX runtime (no need to import React)
    react(),
  ],

  // Path resolution
  resolve: {
    alias: {
      // Enable imports like: import { Button } from '@/components/common/Button'
      // Instead of: import { Button } from '../../../components/common/Button'
      '@': path.resolve(__dirname, './src'),
    },
  },

  // Development server configuration
  server: {
    // Port to run dev server on
    port: 3000,

    // Open browser automatically
    open: false,

    // Proxy API requests to backend
    // This avoids CORS issues during development
    // Requests to /api/* will be forwarded to http://localhost:8000
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        // secure: false, // Uncomment if backend uses self-signed cert
      },
    },
  },

  // Build configuration
  build: {
    // Output directory
    outDir: 'dist',

    // Generate source maps for debugging
    sourcemap: true,

    // Rollup options
    rollupOptions: {
      output: {
        // Split vendor chunks for better caching
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          query: ['@tanstack/react-query'],
          charts: ['recharts'],
        },
      },
    },
  },

  // Preview server (for testing production build)
  preview: {
    port: 3000,
  },
});
