/**
 * Contribution Chart Component
 *
 * Line chart showing commits, PRs, and issues over time.
 * Uses Recharts with ResponsiveContainer for automatic sizing.
 *
 * Colors adapt to dark mode via the useDarkMode hook.
 * The chart uses monotone interpolation for smooth curves
 * and hides individual dots for a cleaner look.
 */
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { useDarkMode } from '@/hooks/useDarkMode';
import type { ContributionPoint } from '@/types';

interface ContributionChartProps {
  data: ContributionPoint[];
}

export function ContributionChart({ data }: ContributionChartProps): JSX.Element {
  const [isDark] = useDarkMode();

  // Colors for light and dark mode
  const colors = {
    grid: isDark ? '#374151' : '#e5e7eb',
    text: isDark ? '#9ca3af' : '#6b7280',
    commits: '#3b82f6',
    pullRequests: '#10b981',
    issues: '#f59e0b',
    tooltip: {
      bg: isDark ? '#1f2937' : '#ffffff',
      border: isDark ? '#374151' : '#e5e7eb',
      text: isDark ? '#f3f4f6' : '#111827',
    },
  };

  // Format date for X axis labels
  const formatDate = (dateStr: string): string => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke={colors.grid} />
          <XAxis
            dataKey="date"
            stroke={colors.text}
            tick={{ fill: colors.text, fontSize: 12 }}
            tickFormatter={formatDate}
            interval="preserveStartEnd"
          />
          <YAxis
            stroke={colors.text}
            tick={{ fill: colors.text, fontSize: 12 }}
            allowDecimals={false}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: colors.tooltip.bg,
              border: `1px solid ${colors.tooltip.border}`,
              borderRadius: '0.5rem',
              color: colors.tooltip.text,
            }}
            labelFormatter={formatDate}
          />
          <Legend
            wrapperStyle={{ paddingTop: '1rem' }}
          />
          <Line
            type="monotone"
            dataKey="commits"
            stroke={colors.commits}
            strokeWidth={2}
            dot={false}
            name="Commits"
          />
          <Line
            type="monotone"
            dataKey="pullRequests"
            stroke={colors.pullRequests}
            strokeWidth={2}
            dot={false}
            name="Pull Requests"
          />
          <Line
            type="monotone"
            dataKey="issues"
            stroke={colors.issues}
            strokeWidth={2}
            dot={false}
            name="Issues"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

/**
 * Skeleton for ContributionChart.
 * Displays a gray placeholder matching the chart height.
 */
export function ContributionChartSkeleton(): JSX.Element {
  return (
    <div className="h-80 w-full bg-gray-100 dark:bg-gray-700 rounded-lg animate-pulse" />
  );
}
