/**
 * Navigation Component
 *
 * Top navigation bar with:
 * - Logo/title
 * - Refresh button (clears backend cache, refetches data)
 * - Dark mode toggle
 * - User avatar and logout
 *
 * Uses useRefreshData mutation to invalidate all analytics queries
 * after the backend cache is cleared.
 */
import { useAuth } from '@/contexts/AuthContext';
import { useRefreshData } from '@/hooks/useAnalytics';
import { useDarkMode } from '@/hooks/useDarkMode';

export function Navigation(): JSX.Element {
  const { user, logout } = useAuth();
  const [isDark, toggleDarkMode] = useDarkMode();
  const refreshMutation = useRefreshData();

  return (
    <nav className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo/Title */}
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">
              Developer Dashboard
            </h1>
          </div>

          {/* Right side */}
          <div className="flex items-center gap-4">
            {/* Refresh Button */}
            <button
              onClick={() => refreshMutation.mutate()}
              disabled={refreshMutation.isPending}
              className="
                p-2 rounded-lg
                text-gray-500 dark:text-gray-400
                hover:bg-gray-100 dark:hover:bg-gray-700
                hover:text-gray-700 dark:hover:text-gray-200
                disabled:opacity-50 disabled:cursor-not-allowed
                transition-colors
              "
              title="Refresh data"
            >
              <svg
                className={`h-5 w-5 ${refreshMutation.isPending ? 'animate-spin' : ''}`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
            </button>

            {/* Dark Mode Toggle */}
            <button
              onClick={toggleDarkMode}
              className="
                p-2 rounded-lg
                text-gray-500 dark:text-gray-400
                hover:bg-gray-100 dark:hover:bg-gray-700
                hover:text-gray-700 dark:hover:text-gray-200
                transition-colors
              "
              title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {isDark ? (
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
                  />
                </svg>
              ) : (
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
                  />
                </svg>
              )}
            </button>

            {/* User Menu */}
            {user && (
              <div className="flex items-center gap-3">
                {user.avatarUrl && (
                  <img
                    src={user.avatarUrl}
                    alt={user.username}
                    className="h-8 w-8 rounded-full"
                  />
                )}
                <span className="text-sm text-gray-700 dark:text-gray-300 hidden sm:inline">
                  {user.name || user.username}
                </span>
                <button
                  onClick={() => void logout()}
                  className="
                    text-sm text-gray-500 dark:text-gray-400
                    hover:text-gray-700 dark:hover:text-gray-200
                    transition-colors
                  "
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
