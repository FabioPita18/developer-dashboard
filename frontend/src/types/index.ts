/**
 * TypeScript Type Definitions
 *
 * These types mirror the backend Pydantic schemas.
 * We'll expand these in Phase 4.
 *
 * Learning Notes:
 * - Interfaces define the shape of objects
 * - These types should match the backend API response formats
 * - Using strict TypeScript (no `any`) ensures type safety
 * - Types are defined separately from runtime code
 */

/**
 * User model - represents a GitHub user in the system.
 * This is a placeholder that will be expanded in Phase 4.
 */
export interface User {
  /** Unique database ID */
  id: number;
  /** GitHub username */
  username: string;
  /** User's email (may be null if private) */
  email: string | null;
  /** GitHub avatar URL */
  avatarUrl: string | null;
  /** Number of followers */
  followers: number;
  /** Number of users following */
  following: number;
  /** Account creation timestamp (ISO string) */
  createdAt: string;
}

/**
 * Authentication status response from the API.
 */
export interface AuthStatus {
  /** Whether the user is currently authenticated */
  isAuthenticated: boolean;
  /** The authenticated user, if any */
  user: User | null;
}

/**
 * Generic API response wrapper.
 * Used for consistent API response format.
 */
export interface ApiResponse<T> {
  /** The response data */
  data: T;
  /** Optional message */
  message?: string;
}

/**
 * API error response format.
 */
export interface ApiError {
  /** Error description */
  detail: string;
  /** HTTP status code */
  status: number;
}

/**
 * Type guard to check if an error is an API error.
 * Type guards help TypeScript narrow types at runtime.
 *
 * @param error - The error to check
 * @returns True if the error matches ApiError shape
 */
export function isApiError(error: unknown): error is ApiError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'detail' in error &&
    typeof (error as ApiError).detail === 'string'
  );
}
