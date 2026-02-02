"""
Cache Service Tests.

Tests the PostgreSQL-based caching functionality.
Uses SQLite in-memory database via the test_db fixture.

Functions tested:
- set_cached: Store data with TTL
- get_cached: Retrieve cached data
- delete_cached: Delete specific cache entry
- delete_all_user_cache: Delete all cache for a user
"""
import pytest

from app.services import cache


class TestCacheService:
    """Tests for the cache service."""

    @pytest.mark.asyncio
    async def test_set_and_get(self, test_db):
        """Should store and retrieve cached data."""
        await cache.set_cached(
            test_db, 1, "test_key", {"value": "test_data"}
        )

        result = await cache.get_cached(test_db, 1, "test_key")

        assert result is not None
        assert result["value"] == "test_data"

    @pytest.mark.asyncio
    async def test_cache_miss(self, test_db):
        """Should return None for non-existent cache."""
        result = await cache.get_cached(test_db, 999, "nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_expired_cache(self, test_db):
        """Should return None for expired cache."""
        await cache.set_cached(
            test_db, 1, "expiring", {"data": "test"}, ttl_seconds=0
        )

        # Should be expired immediately
        result = await cache.get_cached(test_db, 1, "expiring")

        assert result is None

    @pytest.mark.asyncio
    async def test_delete_cache(self, test_db):
        """Should delete specific cache entry."""
        await cache.set_cached(test_db, 1, "to_delete", {"data": "test"})

        # Verify it exists
        assert await cache.get_cached(test_db, 1, "to_delete") is not None

        # Delete it
        deleted = await cache.delete_cached(test_db, 1, "to_delete")

        assert deleted is True
        assert await cache.get_cached(test_db, 1, "to_delete") is None

    @pytest.mark.asyncio
    async def test_delete_all_user_cache(self, test_db):
        """Should delete all cache for a user."""
        await cache.set_cached(test_db, 1, "key1", {"a": 1})
        await cache.set_cached(test_db, 1, "key2", {"b": 2})
        await cache.set_cached(test_db, 1, "key3", {"c": 3})
        await cache.set_cached(test_db, 2, "other", {"d": 4})  # Different user

        count = await cache.delete_all_user_cache(test_db, 1)

        assert count == 3
        assert await cache.get_cached(test_db, 1, "key1") is None
        assert await cache.get_cached(test_db, 1, "key2") is None
        assert await cache.get_cached(test_db, 1, "key3") is None
        # Other user's cache should remain
        assert await cache.get_cached(test_db, 2, "other") is not None

    @pytest.mark.asyncio
    async def test_upsert_updates_existing(self, test_db):
        """Should update existing cache entry."""
        await cache.set_cached(test_db, 1, "key", {"version": 1})
        await cache.set_cached(test_db, 1, "key", {"version": 2})

        result = await cache.get_cached(test_db, 1, "key")

        assert result["version"] == 2
