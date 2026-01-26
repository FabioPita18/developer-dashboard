/**
 * Root Application Component
 *
 * This is the entry point for the React application.
 * We'll add routing and providers in Phase 4.
 *
 * Learning Notes:
 * - React components are functions that return JSX
 * - JSX is a syntax extension that looks like HTML but compiles to JavaScript
 * - Tailwind classes are applied directly to elements
 * - dark: prefix applies styles when dark mode is active
 */

/**
 * Main App component that renders the application root.
 *
 * @returns {JSX.Element} The rendered application
 */
function App(): JSX.Element {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Container centers content and adds horizontal padding */}
      <div className="container mx-auto px-4 py-8">
        {/* Page header */}
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Developer Dashboard
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mb-8">
          GitHub analytics and visualization dashboard.
        </p>

        {/* Status card */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">
            Phase 1 Complete!
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            The development environment is set up and ready.
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-500">
            Next: Phase 2 - Backend Core (Database & OAuth)
          </p>
        </div>

        {/* Environment info card */}
        <div className="card mt-6">
          <h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">
            Tech Stack
          </h3>
          <ul className="space-y-2 text-gray-600 dark:text-gray-400">
            <li className="flex items-center">
              <span className="w-24 font-medium">Frontend:</span>
              <span>React + TypeScript + Tailwind CSS</span>
            </li>
            <li className="flex items-center">
              <span className="w-24 font-medium">Backend:</span>
              <span>FastAPI + SQLAlchemy 2.0 + PostgreSQL</span>
            </li>
            <li className="flex items-center">
              <span className="w-24 font-medium">Build:</span>
              <span>Vite + Docker Compose</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;
