/**
 * OAuth Callback Page
 *
 * Handles the redirect from GitHub OAuth.
 * The actual auth is handled by the backend - this page
 * just shows a loading state while the redirect happens.
 *
 * Flow:
 * 1. Backend completes OAuth and sets cookie
 * 2. Backend redirects to /dashboard
 * 3. If user lands here, re-check auth and navigate
 */
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Loader } from '@/components/common';

export function CallbackPage(): JSX.Element {
  const { checkAuth } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Re-check auth status after OAuth redirect
    const handleCallback = async (): Promise<void> => {
      await checkAuth();
      navigate('/dashboard', { replace: true });
    };

    void handleCallback();
  }, [checkAuth, navigate]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 dark:bg-gray-900">
      <Loader size="lg" />
      <p className="mt-4 text-gray-600 dark:text-gray-400">
        Completing sign in...
      </p>
    </div>
  );
}
