"""
Pydantic Schemas for API Validation.

This package contains all Pydantic v2 schemas for request/response validation.

Schema Organization:
- user.py: User authentication and profile schemas
- analytics.py: Analytics data response schemas

All schemas use the modern ConfigDict pattern (Pydantic v2).
"""
from app.schemas.analytics import (
    ContributionPoint,
    HeatmapPoint,
    LanguageBreakdown,
    Repository,
    UserStats,
)
from app.schemas.user import AuthStatus, UserBase, UserResponse

__all__ = [
    # User schemas
    "UserBase",
    "UserResponse",
    "AuthStatus",
    # Analytics schemas
    "UserStats",
    "ContributionPoint",
    "LanguageBreakdown",
    "Repository",
    "HeatmapPoint",
]
