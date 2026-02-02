/**
 * Authentication Service
 *
 * Handles all authentication-related API calls:
 * - Checking auth status
 * - Initiating login (redirect to GitHub)
 * - Logging out (clears HTTP-only cookie)
 */
import api from './api';
import type { AuthStatus } from '@/types';

export const authService = {
  /**
   * Check current authentication status.
   *
   * Calls /api/auth/status which returns:
   * - authenticated: true/false
   * - user: User object or null
   */
  async getStatus(): Promise<AuthStatus> {
    const response = await api.get<AuthStatus>('/auth/status');
    return response.data;
  },

  /**
   * Initiate GitHub OAuth login.
   *
   * This is NOT an API call - it redirects the browser
   * to the backend OAuth endpoint, which then redirects
   * to GitHub for authorization.
   */
  login(): void {
    window.location.href = '/api/auth/github';
  },

  /**
   * Log out the current user.
   *
   * Clears the HTTP-only cookie on the backend.
   */
  async logout(): Promise<void> {
    await api.post('/auth/logout');
  },
};
