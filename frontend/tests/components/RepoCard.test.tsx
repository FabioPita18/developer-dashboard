/**
 * RepoCard Component Tests
 *
 * Tests repository card rendering including:
 * - Name as link to GitHub
 * - Description display
 * - Language with color dot
 * - Star and fork counts
 * - Private badge visibility
 *
 * Note: Our Repository type uses 'isPrivate' (camelCase from
 * backend's 'is_private'), not 'private'.
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '../utils';
import { RepoCard } from '@/components/dashboard/RepoCard';
import type { Repository } from '@/types';

const mockRepo: Repository = {
  name: 'awesome-project',
  fullName: 'user/awesome-project',
  description: 'An awesome project description',
  htmlUrl: 'https://github.com/user/awesome-project',
  language: 'TypeScript',
  stars: 1234,
  forks: 567,
  isPrivate: false,
  updatedAt: '2024-01-15T10:00:00Z',
};

describe('RepoCard', () => {
  it('renders repository name as link', () => {
    render(<RepoCard repo={mockRepo} />);

    const link = screen.getByRole('link', { name: 'awesome-project' });
    expect(link).toHaveAttribute('href', mockRepo.htmlUrl);
  });

  it('renders description', () => {
    render(<RepoCard repo={mockRepo} />);

    expect(screen.getByText(mockRepo.description!)).toBeInTheDocument();
  });

  it('renders language', () => {
    render(<RepoCard repo={mockRepo} />);

    expect(screen.getByText('TypeScript')).toBeInTheDocument();
  });

  it('renders star count', () => {
    render(<RepoCard repo={mockRepo} />);

    expect(screen.getByText('1,234')).toBeInTheDocument();
  });

  it('renders fork count', () => {
    render(<RepoCard repo={mockRepo} />);

    expect(screen.getByText('567')).toBeInTheDocument();
  });

  it('shows private badge for private repos', () => {
    const privateRepo = { ...mockRepo, isPrivate: true };
    render(<RepoCard repo={privateRepo} />);

    expect(screen.getByText('Private')).toBeInTheDocument();
  });

  it('handles null description', () => {
    const repoNoDesc = { ...mockRepo, description: null };
    render(<RepoCard repo={repoNoDesc} />);

    expect(screen.getByText('awesome-project')).toBeInTheDocument();
  });
});
