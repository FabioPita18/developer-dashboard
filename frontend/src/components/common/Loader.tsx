/**
 * Loading Spinner Component
 *
 * Displays an animated spinner for loading states.
 * Uses Tailwind's animate-spin utility.
 */
import type { WithClassName } from '@/types';

interface LoaderProps extends WithClassName {
  /** Size variant */
  size?: 'sm' | 'md' | 'lg';
}

const sizeClasses = {
  sm: 'h-4 w-4',
  md: 'h-8 w-8',
  lg: 'h-12 w-12',
} as const;

export function Loader({ size = 'md', className = '' }: LoaderProps): JSX.Element {
  return (
    <div
      className={`
        inline-block animate-spin rounded-full
        border-2 border-solid border-current border-r-transparent
        text-primary-600 dark:text-primary-400
        ${sizeClasses[size]}
        ${className}
      `}
      role="status"
      aria-label="Loading"
    >
      <span className="sr-only">Loading...</span>
    </div>
  );
}
