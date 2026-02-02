/**
 * Analytics Hooks using TanStack Query
 *
 * Provides cached, automatically-refreshing data fetching.
 *
 * TanStack Query Benefits:
 * - Automatic caching
 * - Background refetching
 * - Loading/error states
 * - Query invalidation
 *
 * Query Keys:
 * - Used for caching and invalidation
 * - Hierarchical structure for related queries
 */
import {
  useQuery,
  useMutation,
  useQueryClient,
  type UseQueryResult,
  type UseMutationResult,
} from '@tanstack/react-query';
import { analyticsService } from '@/services/analyticsService';
import type {
  UserStats,
  ContributionPoint,
  LanguageBreakdown,
  Repository,
  HeatmapPoint,
} from '@/types';

// =============================================================================
// Query Keys
// =============================================================================

/**
 * Query key factory for type-safe, consistent keys.
 * All analytics queries share the same base key for bulk invalidation.
 */
export const analyticsKeys = {
  all: ['analytics'] as const,
  stats: () => [...analyticsKeys.all, 'stats'] as const,
  contributions: (days: number) =>
    [...analyticsKeys.all, 'contributions', days] as const,
  languages: () => [...analyticsKeys.all, 'languages'] as const,
  repositories: (limit: number) =>
    [...analyticsKeys.all, 'repositories', limit] as const,
  heatmap: () => [...analyticsKeys.all, 'heatmap'] as const,
};

// =============================================================================
// Query Hooks
// =============================================================================

/**
 * Hook for fetching user statistics.
 */
export function useUserStats(): UseQueryResult<UserStats, Error> {
  return useQuery({
    queryKey: analyticsKeys.stats(),
    queryFn: () => analyticsService.getStats(),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 30 * 60 * 1000,   // 30 minutes
  });
}

/**
 * Hook for fetching contribution timeline.
 */
export function useContributions(
  days: number = 30
): UseQueryResult<ContributionPoint[], Error> {
  return useQuery({
    queryKey: analyticsKeys.contributions(days),
    queryFn: () => analyticsService.getContributions(days),
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Hook for fetching language breakdown.
 */
export function useLanguages(): UseQueryResult<LanguageBreakdown[], Error> {
  return useQuery({
    queryKey: analyticsKeys.languages(),
    queryFn: () => analyticsService.getLanguages(),
    staleTime: 5 * 60 * 1000,
    // Filter out languages with less than 1% for cleaner charts
    select: (data: LanguageBreakdown[]) =>
      data.filter((lang) => lang.percentage >= 1),
  });
}

/**
 * Hook for fetching top repositories.
 */
export function useRepositories(
  limit: number = 10
): UseQueryResult<Repository[], Error> {
  return useQuery({
    queryKey: analyticsKeys.repositories(limit),
    queryFn: () => analyticsService.getRepositories(limit),
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Hook for fetching activity heatmap.
 */
export function useHeatmap(): UseQueryResult<HeatmapPoint[], Error> {
  return useQuery({
    queryKey: analyticsKeys.heatmap(),
    queryFn: () => analyticsService.getHeatmap(),
    staleTime: 5 * 60 * 1000,
  });
}

// =============================================================================
// Mutation Hooks
// =============================================================================

/**
 * Hook for refreshing data (clearing backend cache).
 * After success, all analytics queries are invalidated and refetched.
 */
export function useRefreshData(): UseMutationResult<void, Error, void> {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => analyticsService.refreshData(),
    onSuccess: () => {
      // Invalidate all analytics queries - they'll refetch
      void queryClient.invalidateQueries({
        queryKey: analyticsKeys.all,
      });
    },
  });
}
