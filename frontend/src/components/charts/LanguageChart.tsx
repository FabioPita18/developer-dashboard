/**
 * Language Chart Component
 *
 * Pie/donut chart showing programming language breakdown.
 * Uses Recharts PieChart with an inner radius to create
 * a donut effect. Each slice is colored using the language's
 * color from the backend data.
 *
 * Labels show language name and percentage for slices >= 5%.
 * A vertical legend is displayed on the right side.
 */
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { useDarkMode } from '@/hooks/useDarkMode';
import type { LanguageBreakdown } from '@/types';

interface LanguageChartProps {
  data: LanguageBreakdown[];
}

export function LanguageChart({ data }: LanguageChartProps): JSX.Element {
  const [isDark] = useDarkMode();

  const tooltipStyle = {
    backgroundColor: isDark ? '#1f2937' : '#ffffff',
    border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
    borderRadius: '0.5rem',
    color: isDark ? '#f3f4f6' : '#111827',
  };

  // Custom label renderer - only shows for slices >= 5%
  const renderLabel = ({
    name,
    percent,
  }: {
    name: string;
    percent: number;
  }): string => {
    if (percent < 0.05) return '';
    return `${name} (${(percent * 100).toFixed(0)}%)`;
  };

  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            dataKey="percentage"
            nameKey="language"
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            paddingAngle={2}
            label={renderLabel}
            labelLine={false}
          >
            {data.map((entry) => (
              <Cell key={entry.language} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={tooltipStyle}
            formatter={(value: number) => [`${value.toFixed(1)}%`, 'Percentage']}
          />
          <Legend
            layout="vertical"
            align="right"
            verticalAlign="middle"
            formatter={(value: string) => (
              <span className="text-sm text-gray-700 dark:text-gray-300">
                {value}
              </span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

/**
 * Skeleton for LanguageChart.
 * Displays a circular placeholder mimicking the donut shape.
 */
export function LanguageChartSkeleton(): JSX.Element {
  return (
    <div className="h-80 w-full flex items-center justify-center">
      <div className="w-48 h-48 rounded-full bg-gray-100 dark:bg-gray-700 animate-pulse" />
    </div>
  );
}
