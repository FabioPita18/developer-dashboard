/**
 * Root Application Component
 *
 * Sets up the core application infrastructure:
 * - QueryClientProvider: TanStack Query for server state management
 * - BrowserRouter: Client-side routing
 * - AuthProvider: Authentication context for the app
 * - Routes: Page routing with protected routes
 *
 * Component hierarchy:
 *   QueryClientProvider > BrowserRouter > AuthProvider > Routes
 *
 * Why this order?
 * - QueryClient must wrap everything that uses queries
 * - BrowserRouter must wrap anything using useNavigate/useLocation
 * - AuthProvider needs both Query and Router (for redirects)
 */
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from '@/contexts/AuthContext';
import { ProtectedRoute } from '@/components/common';
import {
  LoginPage,
  CallbackPage,
  DashboardPage,
  NotFoundPage,
} from '@/pages';

/**
 * Query Client with sensible defaults.
 *
 * - retry: 1 - retry failed requests once
 * - refetchOnWindowFocus: false - don't refetch when tab becomes active
 * - staleTime: 5 minutes - data is considered fresh for 5 minutes
 */
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000,
    },
  },
});

export default function App(): JSX.Element {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/callback" element={<CallbackPage />} />

            {/* Protected routes - require authentication */}
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />

            {/* Redirect root to dashboard */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />

            {/* 404 catch-all */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
