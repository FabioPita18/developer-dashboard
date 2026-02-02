/**
 * Dashboard Page
 *
 * Main dashboard showing user analytics.
 * Will be expanded in Phase 5 with charts and components.
 *
 * Currently displays:
 * - User profile card
 * - Basic stats (stars, forks, repos)
 */
import { useAuth } from '@/contexts/AuthContext';
import { useUserStats } from '@/hooks/useAnalytics';
import { Card, Loader, ErrorMessage } from '@/components/common';

export function DashboardPage(): JSX.Element {
  const { user, logout } = useAuth();
  const { data: stats, isLoading, error, refetch } = useUserStats();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Developer Dashboard
            </h1>
            <div className="flex items-center gap-4">
              {user && (
                <div className="flex items-center gap-3">
                  {user.avatarUrl && (
                    <img
                      src={user.avatarUrl}
                      alt={user.username}
                      className="h-8 w-8 rounded-full"
                    />
                  )}
                  <span className="text-gray-700 dark:text-gray-300">
                    {user.name ?? user.username}
                  </span>
                </div>
              )}
              <button
                onClick={() => void logout()}
                className="
                  text-gray-600 dark:text-gray-400
                  hover:text-gray-900 dark:hover:text-white
                  text-sm transition-colors
                "
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* User Profile Card */}
        {user && (
          <Card className="mb-8">
            <div className="flex items-center gap-6">
              {user.avatarUrl && (
                <img
                  src={user.avatarUrl}
                  alt={user.username}
                  className="h-24 w-24 rounded-full"
                />
              )}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {user.name ?? user.username}
                </h2>
                <p className="text-gray-600 dark:text-gray-400">
                  @{user.username}
                </p>
                {user.bio && (
                  <p className="mt-2 text-gray-700 dark:text-gray-300">
                    {user.bio}
                  </p>
                )}
                <div className="mt-3 flex gap-4 text-sm text-gray-500 dark:text-gray-400">
                  <span>{user.followers} followers</span>
                  <span>{user.following} following</span>
                  <span>{user.publicRepos} repos</span>
                </div>
              </div>
            </div>
          </Card>
        )}

        {/* Stats Section */}
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          Statistics
        </h2>

        {isLoading && (
          <div className="flex justify-center py-12">
            <Loader size="lg" />
          </div>
        )}

        {error && (
          <ErrorMessage
            message={error.message}
            onRetry={() => void refetch()}
          />
        )}

        {stats && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Total Stars
              </p>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">
                {stats.totalStars.toLocaleString()}
              </p>
            </Card>
            <Card>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Total Forks
              </p>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">
                {stats.totalForks.toLocaleString()}
              </p>
            </Card>
            <Card>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Public Repos
              </p>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">
                {stats.publicRepos}
              </p>
            </Card>
            <Card>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Private Repos
              </p>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">
                {stats.privateRepos}
              </p>
            </Card>
          </div>
        )}

        {/* Placeholder for future components */}
        <div className="mt-8 text-center text-gray-500 dark:text-gray-400">
          <p>More visualizations coming in Phase 5!</p>
        </div>
      </main>
    </div>
  );
}
