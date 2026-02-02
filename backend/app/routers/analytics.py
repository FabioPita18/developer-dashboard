"""
Analytics Router - Dashboard Data Endpoints.

All endpoints require authentication and return cached data
when available.

Endpoints:
- GET /stats: Aggregated user statistics
- GET /contributions: Contribution timeline
- GET /languages: Language breakdown
- GET /repositories: Top repositories
- GET /heatmap: Activity heatmap
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.analytics import (
    ContributionPoint,
    HeatmapPoint,
    LanguageBreakdown,
    Repository,
    UserStats,
)
from app.services import analytics

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
)


@router.get(
    "/stats",
    response_model=UserStats,
    summary="Get user statistics",
    description="Returns aggregated statistics across all repositories.",
)
async def get_stats(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserStats:
    """
    Get aggregated user statistics.

    Includes:
    - Total stars across all repos
    - Total forks
    - Public repo count
    - Private repo count
    - Estimated commit count

    Data is cached for 24 hours by default.
    """
    return await analytics.get_user_stats(db, user)


@router.get(
    "/contributions",
    response_model=list[ContributionPoint],
    summary="Get contribution timeline",
    description="Returns daily contribution counts for the specified period.",
)
async def get_contributions(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    days: int = Query(
        default=30,
        ge=1,
        le=90,
        description="Number of days to include (1-90)",
    ),
) -> list[ContributionPoint]:
    """
    Get contribution timeline.

    Shows daily counts of:
    - Commits
    - Pull requests opened
    - Issues opened

    Note: GitHub only keeps 90 days of events,
    and max 300 events total.
    """
    return await analytics.get_contribution_timeline(db, user, days)


@router.get(
    "/languages",
    response_model=list[LanguageBreakdown],
    summary="Get language breakdown",
    description="Returns language statistics across all repositories.",
)
async def get_languages(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[LanguageBreakdown]:
    """
    Get language breakdown.

    Aggregates bytes of code per language across all repos.
    Returns top 10 languages with percentages.

    Forked repos are excluded (only original code counts).
    """
    return await analytics.get_language_breakdown(db, user)


@router.get(
    "/repositories",
    response_model=list[Repository],
    summary="Get top repositories",
    description="Returns user's repositories sorted by stars.",
)
async def get_repositories(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of repositories to return",
    ),
) -> list[Repository]:
    """
    Get top repositories by stars.

    Returns:
    - Repository name and description
    - Primary language
    - Star and fork counts
    - Privacy status
    - Last updated timestamp
    """
    return await analytics.get_top_repositories(db, user, limit)


@router.get(
    "/heatmap",
    response_model=list[HeatmapPoint],
    summary="Get activity heatmap",
    description="Returns activity counts by day of week and hour.",
)
async def get_heatmap(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[HeatmapPoint]:
    """
    Get activity heatmap data.

    Returns counts for each day/hour combination:
    - day: 0 (Sunday) to 6 (Saturday)
    - hour: 0 to 23
    - count: Number of events

    Useful for visualizing when the user is most active.
    """
    return await analytics.get_activity_heatmap(db, user)
