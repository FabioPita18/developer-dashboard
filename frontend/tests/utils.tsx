/**
 * Test Utilities
 *
 * Custom render function that wraps components with
 * all required providers (QueryClient, BrowserRouter).
 *
 * This ensures components have access to routing and
 * query context during tests.
 */
import { type ReactElement } from 'react';
import { render, type RenderOptions } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

/**
 * Create a fresh QueryClient for each test.
 * Disable retries and caching to make tests deterministic.
 */
const createTestQueryClient = (): QueryClient =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: 0,
        staleTime: 0,
      },
    },
  });

interface WrapperProps {
  children: React.ReactNode;
}

/**
 * Wraps children with all providers needed for testing.
 * Creates a new QueryClient per render to avoid state leaks.
 */
function AllProviders({ children }: WrapperProps): JSX.Element {
  const queryClient = createTestQueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{children}</BrowserRouter>
    </QueryClientProvider>
  );
}

/**
 * Custom render that includes all providers.
 * Use this instead of @testing-library/react's render.
 */
const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: AllProviders, ...options });

// Re-export everything from testing library
export * from '@testing-library/react';

// Override render with our custom version
export { customRender as render };
