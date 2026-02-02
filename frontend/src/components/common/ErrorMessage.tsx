/**
 * Error Message Component
 *
 * Displays error messages with an optional retry button.
 * Styled with red accent colors for both light and dark mode.
 */
import type { WithClassName } from '@/types';

interface ErrorMessageProps extends WithClassName {
  /** Error message to display */
  message: string;
  /** Optional retry callback */
  onRetry?: () => void;
}

export function ErrorMessage({
  message,
  onRetry,
  className = '',
}: ErrorMessageProps): JSX.Element {
  return (
    <div
      className={`
        bg-red-50 dark:bg-red-900/20
        border border-red-200 dark:border-red-800
        rounded-lg p-4
        ${className}
      `}
      role="alert"
    >
      <div className="flex items-center">
        {/* Error icon */}
        <svg
          className="h-5 w-5 text-red-500 dark:text-red-400 mr-3 flex-shrink-0"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>

        <p className="text-red-700 dark:text-red-300 flex-1">{message}</p>

        {onRetry && (
          <button
            onClick={onRetry}
            className="
              ml-4 px-3 py-1 text-sm
              text-red-600 dark:text-red-400
              hover:bg-red-100 dark:hover:bg-red-900/30
              rounded-md transition-colors
            "
          >
            Retry
          </button>
        )}
      </div>
    </div>
  );
}
