/**
 * Application Entry Point
 *
 * This file initializes React and mounts the app to the DOM.
 * We'll add providers (QueryClient, Router, etc.) in Phase 4.
 *
 * Learning Notes:
 * - React 18 uses createRoot instead of ReactDOM.render
 * - StrictMode helps catch common issues during development
 * - The root element is defined in index.html
 */
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// Get the root element from the HTML
const rootElement = document.getElementById('root');

// Throw error if root element is not found
// This should never happen if index.html is correct
if (!rootElement) {
  throw new Error(
    'Root element not found. Check that index.html contains <div id="root"></div>'
  );
}

// Create React root and render the app
// React 18's createRoot enables concurrent features
ReactDOM.createRoot(rootElement).render(
  // StrictMode enables additional development checks:
  // - Identifies components with unsafe lifecycles
  // - Warns about deprecated API usage
  // - Detects unexpected side effects by double-invoking functions
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
