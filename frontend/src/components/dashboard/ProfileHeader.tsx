/**
 * Profile Header Component
 *
 * Displays user profile information at the top of the dashboard.
 * Shows avatar, name, bio, metadata (company, location, blog),
 * and follower/following/repo counts.
 *
 * Responsive: stacks vertically on mobile, horizontal on sm+.
 */
import type { User } from '@/types';

interface ProfileHeaderProps {
  user: User;
}

export function ProfileHeader({ user }: ProfileHeaderProps): JSX.Element {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6">
        {/* Avatar */}
        {user.avatarUrl && (
          <img
            src={user.avatarUrl}
            alt={user.username}
            className="h-24 w-24 rounded-full ring-4 ring-gray-100 dark:ring-gray-700"
          />
        )}

        {/* Info */}
        <div className="text-center sm:text-left flex-1">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            {user.name || user.username}
          </h2>
          <p className="text-gray-500 dark:text-gray-400">@{user.username}</p>

          {user.bio && (
            <p className="mt-3 text-gray-700 dark:text-gray-300 max-w-2xl">
              {user.bio}
            </p>
          )}

          {/* Meta info */}
          <div className="mt-4 flex flex-wrap justify-center sm:justify-start gap-4 text-sm">
            {user.company && (
              <div className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <span>{user.company}</span>
              </div>
            )}
            {user.location && (
              <div className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>{user.location}</span>
              </div>
            )}
            {user.blog && (
              <a
                href={user.blog.startsWith('http') ? user.blog : `https://${user.blog}`}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1 text-primary-600 dark:text-primary-400 hover:underline"
              >
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                </svg>
                <span>{user.blog.replace(/^https?:\/\//, '')}</span>
              </a>
            )}
          </div>

          {/* Stats */}
          <div className="mt-4 flex justify-center sm:justify-start gap-6 text-sm">
            <div>
              <span className="font-semibold text-gray-900 dark:text-white">
                {user.followers.toLocaleString()}
              </span>
              <span className="text-gray-500 dark:text-gray-400 ml-1">followers</span>
            </div>
            <div>
              <span className="font-semibold text-gray-900 dark:text-white">
                {user.following.toLocaleString()}
              </span>
              <span className="text-gray-500 dark:text-gray-400 ml-1">following</span>
            </div>
            <div>
              <span className="font-semibold text-gray-900 dark:text-white">
                {user.publicRepos}
              </span>
              <span className="text-gray-500 dark:text-gray-400 ml-1">repositories</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
