/**
 * Card Component
 *
 * Reusable card wrapper with consistent styling
 * and dark mode support.
 */
import type { WithChildren, WithClassName } from '@/types';

interface CardProps extends WithChildren, WithClassName {
  /** Optional padding size */
  padding?: 'sm' | 'md' | 'lg';
}

const paddingClasses = {
  sm: 'p-4',
  md: 'p-6',
  lg: 'p-8',
} as const;

export function Card({
  children,
  className = '',
  padding = 'md',
}: CardProps): JSX.Element {
  return (
    <div
      className={`
        bg-white dark:bg-gray-800
        border border-gray-200 dark:border-gray-700
        rounded-lg shadow-sm
        ${paddingClasses[padding]}
        ${className}
      `}
    >
      {children}
    </div>
  );
}
