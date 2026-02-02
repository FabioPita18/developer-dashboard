"""
Cache Service Tests.

Tests the PostgreSQL caching functionality.
Uses SQLite in-memory database via the test_db fixture.
"""
import pytest

from app.services import cache


class TestCacheService:
    """Tests for the cache service."""

    @pytest.mark.asyncio
    async def test_set_and_get_cache(self, test_db):
        """Test basic cache set and get."""
        user_id = 1
        cache_key = "test_key"
        data = {"foo": "bar", "count": 42}

        # Set cache
        await cache.set_cached(test_db, user_id, cache_key, data)

        # Get cache
        result = await cache.get_cached(test_db, user_id, cache_key)

        assert result is not None
        assert result["foo"] == "bar"
        assert result["count"] == 42

    @pytest.mark.asyncio
    async def test_cache_miss(self, test_db):
        """Test cache miss returns None."""
        result = await cache.get_cached(test_db, 999, "nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_cache_expiration(self, test_db):
        """Test that expired cache returns None."""
        user_id = 1
        cache_key = "expiring_key"
        data = {"test": "data"}

        # Set cache with 0 second TTL (immediately expired)
        await cache.set_cached(test_db, user_id, cache_key, data, ttl_seconds=0)

        # Should return None (expired)
        result = await cache.get_cached(test_db, user_id, cache_key)
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_cache(self, test_db):
        """Test cache deletion."""
        user_id = 1
        cache_key = "delete_test"
        data = {"test": "data"}

        # Set and verify
        await cache.set_cached(test_db, user_id, cache_key, data)
        assert await cache.get_cached(test_db, user_id, cache_key) is not None

        # Delete
        deleted = await cache.delete_cached(test_db, user_id, cache_key)
        assert deleted is True

        # Verify deleted
        assert await cache.get_cached(test_db, user_id, cache_key) is None

    @pytest.mark.asyncio
    async def test_delete_all_user_cache(self, test_db):
        """Test deleting all cache for a user."""
        user_id = 1

        # Set multiple cache entries
        await cache.set_cached(test_db, user_id, "key1", {"a": 1})
        await cache.set_cached(test_db, user_id, "key2", {"b": 2})
        await cache.set_cached(test_db, user_id, "key3", {"c": 3})

        # Delete all
        count = await cache.delete_all_user_cache(test_db, user_id)
        assert count == 3

        # Verify all deleted
        assert await cache.get_cached(test_db, user_id, "key1") is None
        assert await cache.get_cached(test_db, user_id, "key2") is None
        assert await cache.get_cached(test_db, user_id, "key3") is None

    @pytest.mark.asyncio
    async def test_cache_upsert(self, test_db):
        """Test that set_cached updates existing entries."""
        user_id = 1
        cache_key = "upsert_test"

        # Set initial value
        await cache.set_cached(test_db, user_id, cache_key, {"value": 1})
        result1 = await cache.get_cached(test_db, user_id, cache_key)
        assert result1["value"] == 1

        # Update value
        await cache.set_cached(test_db, user_id, cache_key, {"value": 2})
        result2 = await cache.get_cached(test_db, user_id, cache_key)
        assert result2["value"] == 2
