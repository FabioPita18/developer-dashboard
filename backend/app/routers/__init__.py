"""
API Route Handlers.

This package contains FastAPI routers organized by feature.
Each router handles a specific domain of the API.

Routers:
- auth.py: GitHub OAuth authentication endpoints
- users.py: User profile endpoints
- analytics.py: Analytics data endpoints

All routers use the /api prefix defined in main.py.

Note: Imports are commented out until the actual router files are created in Phase 2.
"""

# These will be uncommented in Phase 2 when the routers are created:
# from app.routers.auth import router as auth_router
# from app.routers.users import router as users_router
# from app.routers.analytics import router as analytics_router

# __all__ = ["auth_router", "users_router", "analytics_router"]
__all__: list[str] = []
