/**
 * Dashboard Page
 *
 * Main dashboard assembling all analytics visualizations:
 * 1. Profile header with user info
 * 2. Statistics grid (stars, forks, public/private repos)
 * 3. Two-column chart row (contributions line chart + language pie chart)
 * 4. Activity heatmap
 * 5. Top repositories grid
 *
 * Each section handles its own loading/error states independently,
 * so partial data can display while other sections are still loading.
 */
import { useAuth } from '@/contexts/AuthContext';
import {
  useUserStats,
  useContributions,
  useLanguages,
  useRepositories,
  useHeatmap,
} from '@/hooks/useAnalytics';
import { DashboardLayout } from '@/components/layout';
import { ErrorMessage } from '@/components/common';
import { ProfileHeader, StatsCard, StatsCardSkeleton, RepoCard, RepoCardSkeleton } from '@/components/dashboard';
import { ContributionChart, ContributionChartSkeleton, LanguageChart, LanguageChartSkeleton, HeatmapChart, HeatmapChartSkeleton } from '@/components/charts';

export function DashboardPage(): JSX.Element {
  const { user } = useAuth();

  // Fetch all analytics data in parallel via TanStack Query
  const stats = useUserStats();
  const contributions = useContributions(30);
  const languages = useLanguages();
  const repositories = useRepositories(6);
  const heatmap = useHeatmap();

  return (
    <DashboardLayout>
      {/* Profile Header */}
      {user && <ProfileHeader user={user} />}

      {/* Stats Grid */}
      <section className="mt-8">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          Statistics
        </h2>

        {stats.error && (
          <ErrorMessage
            message={stats.error.message}
            onRetry={() => void stats.refetch()}
            className="mb-4"
          />
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.isLoading ? (
            <>
              <StatsCardSkeleton />
              <StatsCardSkeleton />
              <StatsCardSkeleton />
              <StatsCardSkeleton />
            </>
          ) : stats.data ? (
            <>
              <StatsCard
                title="Total Stars"
                value={stats.data.totalStars}
                icon={
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                  </svg>
                }
              />
              <StatsCard
                title="Total Forks"
                value={stats.data.totalForks}
                icon={
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                  </svg>
                }
              />
              <StatsCard
                title="Public Repos"
                value={stats.data.publicRepos}
                icon={
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                  </svg>
                }
              />
              <StatsCard
                title="Private Repos"
                value={stats.data.privateRepos}
                icon={
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                }
              />
            </>
          ) : null}
        </div>
      </section>

      {/* Charts Row */}
      <section className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Contribution Chart */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Contributions (30 days)
          </h3>
          {contributions.error && (
            <ErrorMessage
              message={contributions.error.message}
              onRetry={() => void contributions.refetch()}
            />
          )}
          {contributions.isLoading ? (
            <ContributionChartSkeleton />
          ) : contributions.data ? (
            <ContributionChart data={contributions.data} />
          ) : null}
        </div>

        {/* Language Chart */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Languages
          </h3>
          {languages.error && (
            <ErrorMessage
              message={languages.error.message}
              onRetry={() => void languages.refetch()}
            />
          )}
          {languages.isLoading ? (
            <LanguageChartSkeleton />
          ) : languages.data && languages.data.length > 0 ? (
            <LanguageChart data={languages.data} />
          ) : (
            <p className="text-gray-500 dark:text-gray-400 text-center py-8">
              No language data available
            </p>
          )}
        </div>
      </section>

      {/* Activity Heatmap */}
      <section className="mt-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Activity Heatmap
          </h3>
          {heatmap.error && (
            <ErrorMessage
              message={heatmap.error.message}
              onRetry={() => void heatmap.refetch()}
            />
          )}
          {heatmap.isLoading ? (
            <HeatmapChartSkeleton />
          ) : heatmap.data ? (
            <HeatmapChart data={heatmap.data} />
          ) : null}
        </div>
      </section>

      {/* Top Repositories */}
      <section className="mt-8">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          Top Repositories
        </h2>
        {repositories.error && (
          <ErrorMessage
            message={repositories.error.message}
            onRetry={() => void repositories.refetch()}
            className="mb-4"
          />
        )}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {repositories.isLoading ? (
            <>
              <RepoCardSkeleton />
              <RepoCardSkeleton />
              <RepoCardSkeleton />
              <RepoCardSkeleton />
              <RepoCardSkeleton />
              <RepoCardSkeleton />
            </>
          ) : repositories.data ? (
            repositories.data.map((repo) => (
              <RepoCard key={repo.fullName} repo={repo} />
            ))
          ) : null}
        </div>
      </section>
    </DashboardLayout>
  );
}
