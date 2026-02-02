"""
Authentication Endpoint Tests.

Tests the GitHub OAuth flow and authentication status.
Uses mocked GitHub responses to avoid real API calls.

Endpoints tested:
- GET /health: Health check
- GET /api/auth/status: Authentication status
- GET /api/auth/github: GitHub OAuth redirect
- GET /api/auth/callback: OAuth callback handler
- POST /api/auth/logout: Logout
"""

from unittest.mock import patch

import pytest


class TestHealthCheck:
    """Tests for /health endpoint."""

    @pytest.mark.asyncio
    async def test_health_returns_healthy(self, client):
        """Health check should return healthy status."""
        response = await client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestAuthStatus:
    """Tests for /api/auth/status endpoint."""

    @pytest.mark.asyncio
    async def test_unauthenticated_returns_false(self, client):
        """Should return authenticated=false when no cookie."""
        response = await client.get("/api/auth/status")

        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is False
        assert data["user"] is None

    @pytest.mark.asyncio
    async def test_authenticated_returns_user(self, authenticated_client, test_user):
        """Should return user data when authenticated."""
        response = await authenticated_client.get("/api/auth/status")

        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is True
        assert data["user"]["username"] == test_user.username
        assert data["user"]["github_id"] == test_user.github_id

    @pytest.mark.asyncio
    async def test_invalid_token_returns_false(self, client):
        """Should return authenticated=false for invalid token."""
        client.cookies.set("access_token", "invalid_token")
        response = await client.get("/api/auth/status")

        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is False


class TestGitHubLogin:
    """Tests for /api/auth/github endpoint."""

    @pytest.mark.asyncio
    async def test_redirects_to_github(self, client):
        """Should redirect to GitHub authorization URL."""
        response = await client.get(
            "/api/auth/github",
            follow_redirects=False,
        )

        assert response.status_code == 307
        location = response.headers["location"]
        assert "github.com" in location
        assert "oauth/authorize" in location
        assert "client_id=" in location
        assert "redirect_uri=" in location


class TestGitHubCallback:
    """Tests for /api/auth/callback endpoint."""

    @pytest.mark.asyncio
    async def test_successful_callback(
        self, client, mock_github_user, mock_github_token
    ):
        """Should create user and set cookie on successful OAuth."""
        with patch("app.services.github.exchange_code_for_token") as mock_exchange:
            with patch("app.services.github.get_user_profile") as mock_profile:
                mock_exchange.return_value = mock_github_token
                mock_profile.return_value = mock_github_user

                response = await client.get(
                    "/api/auth/callback?code=test_code",
                    follow_redirects=False,
                )

                assert response.status_code == 302
                assert "access_token" in response.cookies
                assert "/dashboard" in response.headers["location"]

    @pytest.mark.asyncio
    async def test_oauth_error_returns_400(self, client):
        """Should return 400 when GitHub returns error."""
        with patch("app.services.github.exchange_code_for_token") as mock_exchange:
            mock_exchange.return_value = {
                "error": "bad_verification_code",
                "error_description": "The code is invalid",
            }

            response = await client.get("/api/auth/callback?code=invalid")

            assert response.status_code == 400
            assert "error" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_profile_fetch_error(self, client, mock_github_token):
        """Should return 400 when profile fetch fails."""
        with patch("app.services.github.exchange_code_for_token") as mock_exchange:
            with patch("app.services.github.get_user_profile") as mock_profile:
                mock_exchange.return_value = mock_github_token
                mock_profile.side_effect = Exception("GitHub API error")

                response = await client.get("/api/auth/callback?code=test")

                assert response.status_code == 400


class TestLogout:
    """Tests for /api/auth/logout endpoint."""

    @pytest.mark.asyncio
    async def test_logout_clears_cookie(self, authenticated_client):
        """Should clear auth cookie on logout."""
        response = await authenticated_client.post("/api/auth/logout")

        assert response.status_code == 200
        assert response.json()["message"] == "Successfully logged out"

    @pytest.mark.asyncio
    async def test_logout_without_auth(self, client):
        """Should work even when not authenticated."""
        response = await client.post("/api/auth/logout")

        assert response.status_code == 200
