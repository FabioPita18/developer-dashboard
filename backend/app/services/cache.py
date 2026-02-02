"""
Caching Service - PostgreSQL-based API Response Cache.

This service caches GitHub API responses to:
1. Reduce API calls (stay under rate limits)
2. Improve response times
3. Provide offline-ish capability

Why PostgreSQL instead of Redis?
    - Simpler infrastructure (no extra service)
    - Persistent storage (survives restarts)
    - SQL queries for cache management
    - JSON support for flexible data

Trade-offs:
    - Slightly slower than Redis for simple operations
    - Uses database connections
    - Acceptable for our use case

Cache Strategy:
    - Each user has their own cache entries
    - Cache keys identify data type (e.g., "user_stats", "languages")
    - TTL (Time-To-Live) determines freshness
    - Expired entries are cleaned up periodically
"""
from datetime import datetime, timedelta
from typing import Any, Callable, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.cache import CachedData

settings = get_settings()

# Type variable for generic cache functions
T = TypeVar("T")


async def get_cached(
    db: AsyncSession,
    user_id: int,
    cache_key: str,
) -> dict[str, Any] | None:
    """
    Get cached data if it exists and is not expired.

    Args:
        db: Database session
        user_id: User's database ID
        cache_key: Cache identifier (e.g., "user_stats")

    Returns:
        Cached data dict, or None if not found/expired
    """
    stmt = select(CachedData).where(
        CachedData.user_id == user_id,
        CachedData.cache_key == cache_key,
    )
    result = await db.execute(stmt)
    cache_entry = result.scalar_one_or_none()

    if not cache_entry:
        return None

    # Check if expired
    if cache_entry.is_expired:
        # Optionally delete expired entry
        await delete_cached(db, user_id, cache_key)
        return None

    return cache_entry.data


async def set_cached(
    db: AsyncSession,
    user_id: int,
    cache_key: str,
    data: dict[str, Any],
    ttl_seconds: int | None = None,
) -> CachedData:
    """
    Store data in cache with TTL.

    Uses a manual upsert pattern (select then insert/update) for
    compatibility with both PostgreSQL and SQLite (used in tests).

    PostgreSQL has INSERT ... ON CONFLICT UPDATE, but SQLite support
    for this is limited. The manual approach works everywhere.

    Args:
        db: Database session
        user_id: User's database ID
        cache_key: Cache identifier
        data: Data to cache (must be JSON-serializable)
        ttl_seconds: Time-to-live in seconds (default from settings)

    Returns:
        The created/updated CachedData entry
    """
    if ttl_seconds is None:
        ttl_seconds = settings.cache_ttl_seconds

    expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)

    # Check if entry already exists
    stmt = select(CachedData).where(
        CachedData.user_id == user_id,
        CachedData.cache_key == cache_key,
    )
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        # Update existing entry
        existing.data = data
        existing.expires_at = expires_at
        existing.updated_at = datetime.utcnow()
        cache_entry = existing
    else:
        # Create new entry
        cache_entry = CachedData(
            user_id=user_id,
            cache_key=cache_key,
            data=data,
            expires_at=expires_at,
        )
        db.add(cache_entry)

    await db.commit()
    await db.refresh(cache_entry)
    return cache_entry


async def delete_cached(
    db: AsyncSession,
    user_id: int,
    cache_key: str,
) -> bool:
    """
    Delete a specific cache entry.

    Args:
        db: Database session
        user_id: User's database ID
        cache_key: Cache identifier

    Returns:
        True if entry was deleted, False if not found
    """
    stmt = delete(CachedData).where(
        CachedData.user_id == user_id,
        CachedData.cache_key == cache_key,
    )
    result = await db.execute(stmt)
    await db.commit()

    return result.rowcount > 0


async def delete_all_user_cache(
    db: AsyncSession,
    user_id: int,
) -> int:
    """
    Delete all cache entries for a user.

    Used when user requests a data refresh.

    Args:
        db: Database session
        user_id: User's database ID

    Returns:
        Number of entries deleted
    """
    stmt = delete(CachedData).where(CachedData.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()

    return result.rowcount


async def delete_expired_cache(db: AsyncSession) -> int:
    """
    Delete all expired cache entries.

    This should be run periodically (e.g., via a background task)
    to clean up stale cache entries.

    Args:
        db: Database session

    Returns:
        Number of entries deleted
    """
    stmt = delete(CachedData).where(
        CachedData.expires_at < datetime.utcnow()
    )
    result = await db.execute(stmt)
    await db.commit()

    return result.rowcount


async def get_or_fetch(
    db: AsyncSession,
    user_id: int,
    cache_key: str,
    fetch_func: Callable[[], Any],
    ttl_seconds: int | None = None,
) -> dict[str, Any]:
    """
    Get from cache or fetch and cache.

    This is the main cache utility. It:
    1. Checks if valid cache exists
    2. If yes, returns cached data
    3. If no, calls fetch_func to get fresh data
    4. Caches the fresh data
    5. Returns the data

    Args:
        db: Database session
        user_id: User's database ID
        cache_key: Cache identifier
        fetch_func: Async function to fetch fresh data
        ttl_seconds: Cache TTL (default from settings)

    Returns:
        The data (from cache or freshly fetched)

    Example:
        data = await get_or_fetch(
            db,
            user.id,
            "user_stats",
            lambda: calculate_user_stats(user),
        )
    """
    # Try to get from cache
    cached = await get_cached(db, user_id, cache_key)
    if cached is not None:
        return cached

    # Fetch fresh data
    data = await fetch_func()

    # Convert to dict if necessary
    if hasattr(data, "model_dump"):
        # Pydantic model
        data = data.model_dump()
    elif hasattr(data, "__dict__"):
        # Regular object
        data = dict(data.__dict__)

    # Cache it
    await set_cached(db, user_id, cache_key, data, ttl_seconds)

    return data
