"""
API Routers Package.

All routers are imported here and can be included in the main app.

Routers:
- auth_router: Authentication endpoints (/api/auth)
- users_router: User profile endpoints (/api/users) - Phase 3
- analytics_router: Analytics endpoints (/api/analytics) - Phase 3
"""
from app.routers.auth import router as auth_router

# Placeholder for future routers (Phase 3)
# from app.routers.users import router as users_router
# from app.routers.analytics import router as analytics_router

__all__ = [
    "auth_router",
    # "users_router",
    # "analytics_router",
]
