/// <reference types="vite/client" />

/**
 * Vite Environment Types
 *
 * This file provides TypeScript definitions for Vite-specific features.
 * The triple-slash reference imports Vite's client types.
 *
 * Learning Notes:
 * - Triple-slash directives are special comments that affect compilation
 * - These types enable features like import.meta.env
 * - Vite's client types handle HMR (Hot Module Replacement) API
 */

/**
 * Environment variables available in the application.
 * Add custom env variables here as needed.
 *
 * Note: Only variables prefixed with VITE_ are exposed to the client.
 * This prevents accidentally exposing server-side secrets.
 */
interface ImportMetaEnv {
  /** The current mode (development, production, etc.) */
  readonly MODE: string;
  /** Base URL of the application */
  readonly BASE_URL: string;
  /** Whether we're in production mode */
  readonly PROD: boolean;
  /** Whether we're in development mode */
  readonly DEV: boolean;
  /** Whether SSR (server-side rendering) is enabled */
  readonly SSR: boolean;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
