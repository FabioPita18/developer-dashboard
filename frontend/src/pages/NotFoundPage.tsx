/**
 * 404 Not Found Page
 *
 * Shown when the user navigates to a non-existent route.
 */
import { Link } from 'react-router-dom';
import { Card } from '@/components/common';

export function NotFoundPage(): JSX.Element {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
      <Card className="max-w-md w-full text-center">
        <h1 className="text-6xl font-bold text-gray-300 dark:text-gray-600 mb-4">
          404
        </h1>
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
          Page Not Found
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          The page you're looking for doesn't exist.
        </p>
        <Link
          to="/"
          className="
            inline-block px-6 py-3
            bg-primary-600 hover:bg-primary-700
            text-white font-medium
            rounded-lg transition-colors
          "
        >
          Go Home
        </Link>
      </Card>
    </div>
  );
}
