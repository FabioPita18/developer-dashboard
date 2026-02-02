/**
 * Stats Card Component
 *
 * Displays a single statistic with title, value, and optional icon.
 * Includes an optional trend indicator showing percentage change.
 *
 * Also exports StatsCardSkeleton for loading states.
 */
import type { ReactNode } from 'react';
import type { WithClassName } from '@/types';

interface StatsCardProps extends WithClassName {
  /** Label displayed above the value */
  title: string;
  /** The statistic value - numbers are formatted with locale separators */
  value: number | string;
  /** Optional icon displayed in the top-right corner */
  icon?: ReactNode;
  /** Optional trend indicator */
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

export function StatsCard({
  title,
  value,
  icon,
  trend,
  className = '',
}: StatsCardProps): JSX.Element {
  const formattedValue = typeof value === 'number'
    ? value.toLocaleString()
    : value;

  return (
    <article
      className={`
        bg-white dark:bg-gray-800
        border border-gray-200 dark:border-gray-700
        rounded-lg shadow-sm p-6
        ${className}
      `}
    >
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">
          {title}
        </h3>
        {icon && (
          <span className="text-gray-400 dark:text-gray-500">
            {icon}
          </span>
        )}
      </div>

      <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">
        {formattedValue}
      </p>

      {trend && (
        <p
          className={`
            mt-2 text-sm flex items-center gap-1
            ${trend.isPositive
              ? 'text-green-600 dark:text-green-400'
              : 'text-red-600 dark:text-red-400'
            }
          `}
        >
          {trend.isPositive ? (
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
            </svg>
          ) : (
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
          )}
          {Math.abs(trend.value)}%
        </p>
      )}
    </article>
  );
}

/**
 * Skeleton loading state for StatsCard.
 * Uses Tailwind animate-pulse for a subtle loading animation.
 */
export function StatsCardSkeleton(): JSX.Element {
  return (
    <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm p-6 animate-pulse">
      <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4" />
      <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/2" />
    </div>
  );
}
