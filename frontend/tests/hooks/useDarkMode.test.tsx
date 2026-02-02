/**
 * useDarkMode Hook Tests
 *
 * Tests dark mode state management:
 * - Default state when no preference stored
 * - Respecting localStorage preference
 * - Toggle functionality
 * - Persistence to localStorage
 * - DOM class manipulation
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useDarkMode } from '@/hooks/useDarkMode';

describe('useDarkMode', () => {
  beforeEach(() => {
    // Reset document classes between tests
    document.documentElement.classList.remove('dark');
    vi.mocked(localStorage.getItem).mockReturnValue(null);
  });

  it('returns false initially when no preference', () => {
    const { result } = renderHook(() => useDarkMode());

    expect(result.current[0]).toBe(false);
  });

  it('respects localStorage preference', () => {
    vi.mocked(localStorage.getItem).mockReturnValue('dark');

    const { result } = renderHook(() => useDarkMode());

    expect(result.current[0]).toBe(true);
  });

  it('toggles dark mode', () => {
    const { result } = renderHook(() => useDarkMode());

    expect(result.current[0]).toBe(false);

    act(() => {
      result.current[1](); // toggle
    });

    expect(result.current[0]).toBe(true);
    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });

  it('persists preference to localStorage', () => {
    const { result } = renderHook(() => useDarkMode());

    act(() => {
      result.current[1](); // toggle to dark
    });

    expect(localStorage.setItem).toHaveBeenCalledWith('theme', 'dark');
  });
});
