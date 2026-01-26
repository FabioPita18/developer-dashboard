/**
 * Vitest Configuration
 *
 * Vitest is a Vite-native testing framework.
 * It's fast because it reuses Vite's config and transformers.
 *
 * @see https://vitest.dev/config/
 */
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],

  test: {
    // Use jsdom for DOM testing
    environment: 'jsdom',

    // Enable global APIs (describe, it, expect)
    globals: true,

    // Setup files run before each test file
    setupFiles: ['./tests/setup.ts'],

    // Test file patterns
    include: ['./tests/**/*.test.{ts,tsx}'],

    // Coverage configuration
    coverage: {
      reporter: ['text', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/types/*',
      ],
    },
  },

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
