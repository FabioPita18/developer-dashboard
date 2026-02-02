/**
 * Protected Route Component
 *
 * Wraps routes that require authentication.
 * Shows a loader while checking auth status,
 * then redirects to login if not authenticated.
 */
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Loader } from './Loader';
import type { WithChildren } from '@/types';

export function ProtectedRoute({ children }: WithChildren): JSX.Element {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  // Show loader while checking auth
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <Loader size="lg" />
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return (
      <Navigate
        to="/login"
        state={{ from: location }}
        replace
      />
    );
  }

  return <>{children}</>;
}
