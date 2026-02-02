/**
 * Dark Mode Hook
 *
 * Manages dark mode state with:
 * - localStorage persistence
 * - System preference detection
 * - DOM class manipulation on <html> element
 *
 * Tailwind's 'class' dark mode strategy requires the 'dark'
 * class on the root element to activate dark styles.
 */
import { useCallback, useEffect, useState } from 'react';

/**
 * Hook for managing dark mode.
 *
 * @returns Tuple of [isDark, toggle]
 */
export function useDarkMode(): [boolean, () => void] {
  // Initialize from localStorage or system preference
  const [isDark, setIsDark] = useState<boolean>(() => {
    // Check if we're in the browser
    if (typeof window === 'undefined') {
      return false;
    }

    // Check localStorage first (user preference)
    const stored = localStorage.getItem('theme');
    if (stored !== null) {
      return stored === 'dark';
    }

    // Fall back to system preference
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  // Update DOM and localStorage when state changes
  useEffect(() => {
    const root = document.documentElement;

    if (isDark) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }

    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }, [isDark]);

  // Toggle function
  const toggle = useCallback(() => {
    setIsDark((prev) => !prev);
  }, []);

  return [isDark, toggle];
}
