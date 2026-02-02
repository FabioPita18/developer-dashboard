/**
 * StatsCard Component Tests
 *
 * Tests rendering of statistics with various props:
 * - Title and value display
 * - Number formatting with locale separators
 * - String value passthrough
 * - Optional icon rendering
 * - Trend indicator display
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '../utils';
import { StatsCard } from '@/components/dashboard/StatsCard';

describe('StatsCard', () => {
  it('renders title and value', () => {
    render(<StatsCard title="Total Stars" value={1234} />);

    expect(screen.getByText('Total Stars')).toBeInTheDocument();
    expect(screen.getByText('1,234')).toBeInTheDocument();
  });

  it('formats large numbers with locale', () => {
    render(<StatsCard title="Followers" value={1000000} />);

    expect(screen.getByText('1,000,000')).toBeInTheDocument();
  });

  it('renders string values', () => {
    render(<StatsCard title="Status" value="Active" />);

    expect(screen.getByText('Active')).toBeInTheDocument();
  });

  it('renders icon when provided', () => {
    render(
      <StatsCard
        title="Stars"
        value={100}
        icon={<span data-testid="test-icon">★</span>}
      />
    );

    expect(screen.getByTestId('test-icon')).toBeInTheDocument();
  });

  it('renders trend when provided', () => {
    render(
      <StatsCard
        title="Stars"
        value={100}
        trend={{ value: 15, isPositive: true }}
      />
    );

    expect(screen.getByText('15%')).toBeInTheDocument();
  });
});
