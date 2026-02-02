/**
 * Dashboard Layout
 *
 * Wrapper component that includes navigation
 * and provides consistent layout for dashboard pages.
 *
 * Uses max-w-7xl to constrain content width on large screens,
 * with responsive horizontal padding.
 */
import { Navigation } from './Navigation';
import type { WithChildren } from '@/types';

export function DashboardLayout({ children }: WithChildren): JSX.Element {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navigation />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}
