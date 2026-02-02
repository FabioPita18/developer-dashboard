"""
API Routers Package.

All routers are exported here for inclusion in the main app.

Routers:
- auth_router: Authentication endpoints (/api/auth)
- users_router: User profile endpoints (/api/users)
- analytics_router: Analytics endpoints (/api/analytics)
"""
from app.routers.analytics import router as analytics_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router

__all__ = [
    "auth_router",
    "users_router",
    "analytics_router",
]
