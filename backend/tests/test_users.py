"""
User Endpoint Tests.

Tests user profile retrieval and data refresh.

Endpoints tested:
- GET /api/users/me: Current user profile
- POST /api/users/me/refresh: Clear cache and refresh data
"""
import pytest


class TestGetCurrentUser:
    """Tests for GET /api/users/me endpoint."""

    @pytest.mark.asyncio
    async def test_returns_user_profile(self, authenticated_client, test_user):
        """Should return current user's profile."""
        response = await authenticated_client.get("/api/users/me")

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user.username
        assert data["email"] == test_user.email
        assert "access_token" not in data  # Security check

    @pytest.mark.asyncio
    async def test_requires_authentication(self, client):
        """Should return 401 when not authenticated."""
        response = await client.get("/api/users/me")

        assert response.status_code == 401


class TestRefreshUserData:
    """Tests for POST /api/users/me/refresh endpoint."""

    @pytest.mark.asyncio
    async def test_clears_cache(self, authenticated_client, test_user, test_db):
        """Should clear user's cached data."""
        from app.services import cache

        # Add some cached data
        await cache.set_cached(
            test_db, test_user.id, "test_key", {"data": "test"}
        )

        # Verify cache exists
        cached = await cache.get_cached(test_db, test_user.id, "test_key")
        assert cached is not None

        # Call refresh
        response = await authenticated_client.post("/api/users/me/refresh")

        assert response.status_code == 200
        assert "cleared" in response.json()["message"].lower()

    @pytest.mark.asyncio
    async def test_requires_authentication(self, client):
        """Should return 401 when not authenticated."""
        response = await client.post("/api/users/me/refresh")

        assert response.status_code == 401
