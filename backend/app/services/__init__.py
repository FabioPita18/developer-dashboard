"""
Business Logic Services.

This package contains service classes and functions that implement
the business logic, separate from the API layer.

Services:
- github.py: GitHub API client (OAuth, user data, repos, events)
- cache.py: Database caching service for API responses
- analytics.py: Analytics data processing and aggregation
- security.py: JWT token handling and authentication utilities

Design Pattern:
Services are stateless functions that receive dependencies (like db sessions)
as parameters. This makes them easy to test and reuse.

Note: Imports are commented out until the actual service files are created in Phase 2.
"""

# These will be uncommented in Phase 2 when the services are created:
# from app.services import github
# from app.services import cache
# from app.services import analytics
# from app.services import security

# __all__ = ["github", "cache", "analytics", "security"]
__all__: list[str] = []
