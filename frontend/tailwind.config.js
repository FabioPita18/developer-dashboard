/** @type {import('tailwindcss').Config} */
export default {
  // Files to scan for Tailwind classes
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],

  // Dark mode configuration
  // 'class' strategy: dark mode is enabled by adding 'dark' class to <html>
  // This allows programmatic control via JavaScript
  // Alternative: 'media' uses system preference only
  darkMode: 'class',

  theme: {
    extend: {
      // Custom color palette
      colors: {
        // Primary colors (blue by default)
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
        // GitHub language colors for charts
        github: {
          javascript: '#f1e05a',
          typescript: '#3178c6',
          python: '#3572A5',
          java: '#b07219',
          go: '#00ADD8',
          rust: '#dea584',
          ruby: '#701516',
          php: '#4F5D95',
          csharp: '#178600',
          cpp: '#f34b7d',
          html: '#e34c26',
          css: '#563d7c',
          shell: '#89e051',
          swift: '#F05138',
          kotlin: '#A97BFF',
        },
      },
      // Custom animations
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 2s linear infinite',
      },
      // Custom font families (optional)
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },

  plugins: [],
};
