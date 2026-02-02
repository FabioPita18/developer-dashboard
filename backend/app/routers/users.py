"""
Users Router - User Profile Endpoints.

Provides:
- GET /me: Current user's profile
- POST /me/refresh: Clear cache and refresh data

These endpoints require authentication (JWT in HTTP-only cookie).
"""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.services import cache

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Returns the authenticated user's profile information.",
)
async def get_current_user_profile(
    user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """
    Get the current authenticated user's profile.

    Returns all public profile data (never includes access_token).
    """
    return UserResponse.model_validate(user)


@router.post(
    "/me/refresh",
    summary="Refresh user data",
    description="Clears cached data and triggers a refresh from GitHub.",
)
async def refresh_user_data(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    """
    Clear all cached data for the current user.

    This forces fresh data to be fetched from GitHub
    on the next analytics request.

    Use this when:
    - User wants to see latest data
    - User suspects cache is stale
    - After making changes on GitHub
    """
    count = await cache.delete_all_user_cache(db, user.id)

    return {
        "message": f"Cache cleared. {count} entries deleted.",
        "status": "success",
    }
