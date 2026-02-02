/**
 * Loader Component Tests
 *
 * Tests the loading spinner with:
 * - Default size rendering
 * - Small size variant
 * - Large size variant
 * - Accessible loading text (sr-only)
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '../utils';
import { Loader } from '@/components/common/Loader';

describe('Loader', () => {
  it('renders with default size', () => {
    render(<Loader />);

    const loader = screen.getByRole('status');
    expect(loader).toBeInTheDocument();
  });

  it('renders with small size', () => {
    render(<Loader size="sm" />);

    const loader = screen.getByRole('status');
    expect(loader).toHaveClass('h-4', 'w-4');
  });

  it('renders with large size', () => {
    render(<Loader size="lg" />);

    const loader = screen.getByRole('status');
    expect(loader).toHaveClass('h-12', 'w-12');
  });

  it('has accessible loading text', () => {
    render(<Loader />);

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
});
