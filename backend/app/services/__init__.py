"""
Business Logic Services.

This package contains service classes and functions that implement
the business logic, separate from the API layer.

Services:
- github.py: GitHub API client (OAuth, user data, repos, events)
- security.py: JWT token handling and authentication utilities
- cache.py: Database caching service for API responses (Phase 3)
- analytics.py: Analytics data processing and aggregation (Phase 3)

Design Pattern:
Services are stateless functions that receive dependencies (like db sessions)
as parameters. This makes them easy to test and reuse.
"""

from app.services import analytics, cache, github, security

__all__ = ["analytics", "cache", "github", "security"]
