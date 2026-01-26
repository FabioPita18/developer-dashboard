"""
Pydantic Schemas for API Validation.

This package contains Pydantic v2 schemas for request/response validation.
All schemas use the modern ConfigDict pattern (not class Config).

Schema Categories:
- user.py: User-related schemas (UserResponse, AuthStatus)
- analytics.py: Analytics response schemas (UserStats, ContributionPoint, etc.)

Note: Imports are commented out until the actual schema files are created in Phase 2.
"""

# These will be uncommented in Phase 2 when the schemas are created:
# from app.schemas.user import UserBase, UserResponse, AuthStatus
# from app.schemas.analytics import (
#     UserStats,
#     ContributionPoint,
#     LanguageBreakdown,
#     Repository,
#     HeatmapPoint,
# )

# __all__ = [
#     "UserBase",
#     "UserResponse",
#     "AuthStatus",
#     "UserStats",
#     "ContributionPoint",
#     "LanguageBreakdown",
#     "Repository",
#     "HeatmapPoint",
# ]
__all__: list[str] = []
