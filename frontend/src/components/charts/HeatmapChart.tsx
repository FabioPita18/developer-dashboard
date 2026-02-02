/**
 * Heatmap Chart Component
 *
 * Custom grid visualization showing activity by day of week and hour.
 * Each cell represents activity count at a specific day/hour combination.
 *
 * Color intensity scales from light (low activity) to blue (high activity).
 * The grid is scrollable horizontally on small screens.
 *
 * Data format: { day: 0-6 (Sun-Sat), hour: 0-23, count: number }
 */
import { useMemo } from 'react';
import { useDarkMode } from '@/hooks/useDarkMode';
import type { HeatmapPoint } from '@/types';

interface HeatmapChartProps {
  data: HeatmapPoint[];
}

/** Day labels matching the backend's day numbering (0 = Sunday) */
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

/** All 24 hours for the grid columns */
const HOURS = Array.from({ length: 24 }, (_, i) => i);

export function HeatmapChart({ data }: HeatmapChartProps): JSX.Element {
  const [isDark] = useDarkMode();

  // Create a map for O(1) lookup by day-hour key
  const dataMap = useMemo(() => {
    const map = new Map<string, number>();
    data.forEach((point) => {
      map.set(`${point.day}-${point.hour}`, point.count);
    });
    return map;
  }, [data]);

  // Find max count for color intensity scaling
  const maxCount = useMemo(() => {
    return Math.max(...data.map((d) => d.count), 1);
  }, [data]);

  // Get background color based on activity count
  const getColor = (count: number): string => {
    if (count === 0) {
      return isDark ? '#1f2937' : '#f3f4f6';
    }
    const intensity = count / maxCount;
    if (intensity < 0.25) {
      return isDark ? '#1e3a5f' : '#dbeafe';
    }
    if (intensity < 0.5) {
      return isDark ? '#1e40af' : '#93c5fd';
    }
    if (intensity < 0.75) {
      return isDark ? '#2563eb' : '#60a5fa';
    }
    return isDark ? '#3b82f6' : '#3b82f6';
  };

  return (
    <div className="overflow-x-auto">
      <div className="min-w-[600px]">
        {/* Hour labels - show every 3 hours */}
        <div className="flex mb-1 ml-12">
          {HOURS.filter((h) => h % 3 === 0).map((hour) => (
            <div
              key={hour}
              className="text-xs text-gray-500 dark:text-gray-400"
              style={{ width: '3rem', textAlign: 'center' }}
            >
              {hour}:00
            </div>
          ))}
        </div>

        {/* Grid rows - one per day */}
        {DAYS.map((day, dayIndex) => (
          <div key={day} className="flex items-center mb-1">
            {/* Day label */}
            <div className="w-12 text-xs text-gray-500 dark:text-gray-400 text-right pr-2">
              {day}
            </div>

            {/* Hour cells */}
            <div className="flex gap-1">
              {HOURS.map((hour) => {
                const count = dataMap.get(`${dayIndex}-${hour}`) ?? 0;
                return (
                  <div
                    key={hour}
                    className="w-4 h-4 rounded-sm cursor-pointer transition-transform hover:scale-125"
                    style={{ backgroundColor: getColor(count) }}
                    title={`${day} ${hour}:00 - ${count} activities`}
                  />
                );
              })}
            </div>
          </div>
        ))}

        {/* Legend */}
        <div className="flex items-center justify-end mt-4 gap-2 text-xs text-gray-500 dark:text-gray-400">
          <span>Less</span>
          <div className="flex gap-1">
            {[0, 0.25, 0.5, 0.75, 1].map((intensity, i) => (
              <div
                key={i}
                className="w-4 h-4 rounded-sm"
                style={{ backgroundColor: getColor(intensity * maxCount) }}
              />
            ))}
          </div>
          <span>More</span>
        </div>
      </div>
    </div>
  );
}

/**
 * Skeleton for HeatmapChart.
 * Displays a gray placeholder matching approximate chart dimensions.
 */
export function HeatmapChartSkeleton(): JSX.Element {
  return (
    <div className="h-48 w-full bg-gray-100 dark:bg-gray-700 rounded-lg animate-pulse" />
  );
}
