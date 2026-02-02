/**
 * TypeScript Type Definitions
 *
 * These types MUST match the backend Pydantic schemas exactly.
 * When the backend changes, update these immediately.
 *
 * Convention: Frontend uses camelCase, backend uses snake_case.
 * The API service layer handles conversion automatically.
 */

// =============================================================================
// User Types
// =============================================================================

/**
 * User profile data from API.
 * Matches backend UserResponse schema (after camelCase conversion).
 */
export interface User {
  id: number;
  githubId: number;
  username: string;
  email: string | null;
  name: string | null;
  avatarUrl: string | null;
  bio: string | null;
  company: string | null;
  location: string | null;
  blog: string | null;
  publicRepos: number;
  followers: number;
  following: number;
  createdAt: string;
  lastLoginAt: string;
}

/**
 * Authentication status from /api/auth/status.
 * Backend returns { authenticated: bool, user: User | null }.
 */
export interface AuthStatus {
  authenticated: boolean;
  user: User | null;
}

// =============================================================================
// Analytics Types
// =============================================================================

/**
 * Aggregated user statistics.
 * Matches backend UserStats schema.
 */
export interface UserStats {
  totalStars: number;
  totalForks: number;
  publicRepos: number;
  privateRepos: number;
  totalCommits: number;
}

/**
 * Single point on contribution timeline.
 * Matches backend ContributionPoint schema.
 */
export interface ContributionPoint {
  date: string;
  commits: number;
  pullRequests: number;
  issues: number;
}

/**
 * Language breakdown for pie chart.
 * Matches backend LanguageBreakdown schema.
 */
export interface LanguageBreakdown {
  language: string;
  bytes: number;
  percentage: number;
  color: string;
}

/**
 * Repository data for display.
 * Matches backend Repository schema.
 *
 * Note: Backend field 'is_private' becomes 'isPrivate' after
 * snake_case to camelCase conversion in the API layer.
 */
export interface Repository {
  name: string;
  fullName: string;
  description: string | null;
  htmlUrl: string;
  language: string | null;
  stars: number;
  forks: number;
  isPrivate: boolean;
  updatedAt: string;
}

/**
 * Activity heatmap data point.
 * Matches backend HeatmapPoint schema.
 */
export interface HeatmapPoint {
  day: number;
  hour: number;
  count: number;
}

// =============================================================================
// API Types
// =============================================================================

/**
 * API error response format (from FastAPI HTTPException).
 */
export interface ApiError {
  detail: string;
}

/**
 * Type guard for API errors.
 * Use this when catching errors from API calls.
 */
export function isApiError(error: unknown): error is ApiError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'detail' in error &&
    typeof (error as ApiError).detail === 'string'
  );
}

// =============================================================================
// Component Types
// =============================================================================

/**
 * Common props for components that accept className.
 */
export interface WithClassName {
  className?: string;
}

/**
 * Common props for components with children.
 */
export interface WithChildren {
  children: React.ReactNode;
}
