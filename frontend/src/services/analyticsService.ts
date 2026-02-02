/**
 * Analytics Service
 *
 * API calls for all analytics endpoints.
 * Used by TanStack Query hooks for data fetching.
 *
 * Each method corresponds to a backend analytics endpoint.
 */
import api from './api';
import type {
  UserStats,
  ContributionPoint,
  LanguageBreakdown,
  Repository,
  HeatmapPoint,
} from '@/types';

export const analyticsService = {
  /**
   * Get aggregated user statistics.
   */
  async getStats(): Promise<UserStats> {
    const response = await api.get<UserStats>('/analytics/stats');
    return response.data;
  },

  /**
   * Get contribution timeline.
   * @param days Number of days to fetch (default 30)
   */
  async getContributions(days: number = 30): Promise<ContributionPoint[]> {
    const response = await api.get<ContributionPoint[]>(
      '/analytics/contributions',
      { params: { days } }
    );
    return response.data;
  },

  /**
   * Get language breakdown across all repositories.
   */
  async getLanguages(): Promise<LanguageBreakdown[]> {
    const response = await api.get<LanguageBreakdown[]>('/analytics/languages');
    return response.data;
  },

  /**
   * Get top repositories sorted by stars.
   * @param limit Maximum number of repos (default 10)
   */
  async getRepositories(limit: number = 10): Promise<Repository[]> {
    const response = await api.get<Repository[]>('/analytics/repositories', {
      params: { limit },
    });
    return response.data;
  },

  /**
   * Get activity heatmap data.
   */
  async getHeatmap(): Promise<HeatmapPoint[]> {
    const response = await api.get<HeatmapPoint[]>('/analytics/heatmap');
    return response.data;
  },

  /**
   * Clear cache and trigger data refresh.
   */
  async refreshData(): Promise<void> {
    await api.post('/users/me/refresh');
  },
};
