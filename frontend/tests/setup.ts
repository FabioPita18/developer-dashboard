/**
 * Vitest Setup File
 *
 * This file runs before each test file.
 * It sets up:
 * - Jest DOM matchers (toBeInTheDocument, etc.)
 * - Browser API mocks (localStorage, matchMedia, location)
 *
 * Mocking these browser APIs is required because jsdom
 * doesn't implement them natively.
 */
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock window.matchMedia for dark mode tests
// jsdom doesn't implement matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
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

// Mock window.location
const locationMock = {
  href: '',
  pathname: '/',
  assign: vi.fn(),
  replace: vi.fn(),
  reload: vi.fn(),
};
Object.defineProperty(window, 'location', {
  value: locationMock,
  writable: true,
});

// Mock scrollTo
window.scrollTo = vi.fn();

// Reset all mocks before each test
beforeEach(() => {
  vi.clearAllMocks();
  localStorageMock.getItem.mockReturnValue(null);
  locationMock.href = '';
  locationMock.pathname = '/';
});
