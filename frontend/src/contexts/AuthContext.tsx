/* eslint-disable react-refresh/only-export-components */
/**
 * Authentication Context
 *
 * Provides authentication state to the entire application.
 *
 * Features:
 * - Tracks current user
 * - Checks auth status on mount
 * - Provides login/logout functions
 * - Loading state during auth check
 *
 * Usage:
 *   const { user, isAuthenticated, login, logout } = useAuth();
 */
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from 'react';
import { authService } from '@/services/authService';
import type { User } from '@/types';

// =============================================================================
// Types
// =============================================================================

interface AuthContextType {
  /** Current user (null if not authenticated) */
  user: User | null;
  /** Whether user is authenticated */
  isAuthenticated: boolean;
  /** Whether auth check is in progress */
  isLoading: boolean;
  /** Initiate GitHub OAuth login */
  login: () => void;
  /** Log out the current user */
  logout: () => Promise<void>;
  /** Re-check authentication status */
  checkAuth: () => Promise<void>;
}

// =============================================================================
// Context
// =============================================================================

const AuthContext = createContext<AuthContextType | null>(null);

// =============================================================================
// Provider
// =============================================================================

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps): JSX.Element {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Check authentication status with the backend.
   */
  const checkAuth = useCallback(async (): Promise<void> => {
    try {
      setIsLoading(true);
      const status = await authService.getStatus();

      if (status.authenticated && status.user) {
        setUser(status.user);
      } else {
        setUser(null);
      }
    } catch {
      // If the check fails, assume not authenticated
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Initiate GitHub OAuth login.
   */
  const login = useCallback((): void => {
    authService.login();
  }, []);

  /**
   * Log out and clear user state.
   */
  const logout = useCallback(async (): Promise<void> => {
    try {
      await authService.logout();
    } catch {
      // Clear user state regardless of API result
    } finally {
      setUser(null);
    }
  }, []);

  // Check auth on mount
  useEffect(() => {
    void checkAuth();
  }, [checkAuth]);

  // Compute derived state
  const isAuthenticated = user !== null;

  // Context value
  const value: AuthContextType = {
    user,
    isAuthenticated,
    isLoading,
    login,
    logout,
    checkAuth,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// =============================================================================
// Hook
// =============================================================================

/**
 * Hook to access auth context.
 *
 * Must be used within AuthProvider.
 *
 * @throws Error if used outside AuthProvider
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
}
