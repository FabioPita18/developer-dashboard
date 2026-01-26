/**
 * Vitest Setup File
 *
 * This file runs before each test file.
 * It sets up:
 * - Jest DOM matchers (toBeInTheDocument, etc.)
 * - Browser API mocks (localStorage, matchMedia)
 */
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock window.matchMedia for dark mode tests
// This is required because jsdom doesn't implement matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // Deprecated but still used
    removeListener: vi.fn(), // Deprecated but still used
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
  length: 0,
  key: vi.fn(),
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Mock scrollTo
window.scrollTo = vi.fn();

// Silence console errors in tests (optional)
// Uncomment if you want cleaner test output
// vi.spyOn(console, 'error').mockImplementation(() => {});
