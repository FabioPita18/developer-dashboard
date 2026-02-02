/**
 * Axios API Client Configuration
 *
 * Central HTTP client with:
 * - Base URL configuration
 * - Credentials for cookies
 * - Response interceptors
 * - Snake_case to camelCase conversion
 *
 * Why Axios over fetch?
 * - Better error handling with interceptors
 * - Automatic JSON parsing
 * - Request cancellation support
 * - Consistent API across browsers
 */
import axios, {
  type AxiosError,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from 'axios';

// Create Axios instance with defaults
const api = axios.create({
  // Base URL - Vite proxy handles /api in development
  baseURL: '/api',

  // CRITICAL: Include cookies in requests
  // Required for HTTP-only JWT cookie authentication
  withCredentials: true,

  // Default headers
  headers: {
    'Content-Type': 'application/json',
  },

  // Timeout after 30 seconds
  timeout: 30000,
});

// =============================================================================
// Case Conversion Utilities
// =============================================================================

/**
 * Convert snake_case string to camelCase.
 * Example: "user_name" -> "userName"
 */
function toCamelCase(str: string): string {
  return str.replace(/_([a-z])/g, (_: string, letter: string) =>
    letter.toUpperCase()
  );
}

/**
 * Convert camelCase string to snake_case.
 * Example: "userName" -> "user_name"
 */
function toSnakeCase(str: string): string {
  return str.replace(/[A-Z]/g, (letter: string) => `_${letter.toLowerCase()}`);
}

/**
 * Recursively convert object keys from snake_case to camelCase.
 * Handles nested objects and arrays.
 */
function convertKeysToCamelCase<T>(obj: T): T {
  if (Array.isArray(obj)) {
    return obj.map(convertKeysToCamelCase) as T;
  }

  if (obj !== null && typeof obj === 'object' && !(obj instanceof Date)) {
    const converted: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(obj as Record<string, unknown>)) {
      converted[toCamelCase(key)] = convertKeysToCamelCase(value);
    }
    return converted as T;
  }

  return obj;
}

/**
 * Recursively convert object keys from camelCase to snake_case.
 * Used for sending data to the Python backend.
 */
function convertKeysToSnakeCase<T>(obj: T): T {
  if (Array.isArray(obj)) {
    return obj.map(convertKeysToSnakeCase) as T;
  }

  if (obj !== null && typeof obj === 'object' && !(obj instanceof Date)) {
    const converted: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(obj as Record<string, unknown>)) {
      converted[toSnakeCase(key)] = convertKeysToSnakeCase(value);
    }
    return converted as T;
  }

  return obj;
}

// =============================================================================
// Request Interceptor
// =============================================================================

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Convert request body keys to snake_case for backend
    if (config.data && typeof config.data === 'object') {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
      config.data = convertKeysToSnakeCase(config.data);
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// =============================================================================
// Response Interceptor
// =============================================================================

api.interceptors.response.use(
  (response: AxiosResponse) => {
    // Convert response data keys from snake_case to camelCase
    if (response.data) {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
      response.data = convertKeysToCamelCase(response.data);
    }
    return response;
  },
  (error: AxiosError) => {
    // Handle 401 Unauthorized - redirect to login
    if (error.response?.status === 401) {
      // Only redirect if not already on login page
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
      }
    }

    // Convert error response data to camelCase
    if (error.response?.data) {
      error.response.data = convertKeysToCamelCase(error.response.data);
    }

    return Promise.reject(error);
  }
);

export default api;
