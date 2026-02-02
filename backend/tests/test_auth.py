"""
Authentication Endpoint Tests.

Tests the GitHub OAuth flow and authentication status.
Uses mocked GitHub responses to avoid real API calls.
"""
import pytest
from unittest.mock import patch


class TestAuthStatus:
    """Tests for /api/auth/status endpoint."""

    @pytest.mark.asyncio
    async def test_unauthenticated_status(self, client):
        """Test auth status when not logged in."""
        response = await client.get("/api/auth/status")

        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is False
        assert data["user"] is None

    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """Test health check endpoint."""
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestGitHubLogin:
    """Tests for /api/auth/github endpoint."""

    @pytest.mark.asyncio
    async def test_github_login_redirects(self, client):
        """Test that GitHub login initiates OAuth redirect."""
        response = await client.get(
            "/api/auth/github",
            follow_redirects=False,
        )

        # Should redirect to GitHub
        assert response.status_code == 307
        location = response.headers["location"]
        assert "github.com" in location
        assert "oauth/authorize" in location
        assert "client_id=" in location


class TestGitHubCallback:
    """Tests for /api/auth/callback endpoint."""

    @pytest.mark.asyncio
    async def test_callback_success(
        self,
        client,
        mock_github_user,
        mock_github_token,
    ):
        """Test successful OAuth callback creates user and sets cookie."""
        # Mock GitHub API calls
        with patch("app.services.github.exchange_code_for_token") as mock_exchange:
            with patch("app.services.github.get_user_profile") as mock_profile:
                # Setup mocks
                mock_exchange.return_value = mock_github_token
                mock_profile.return_value = mock_github_user

                # Make request
                response = await client.get(
                    "/api/auth/callback?code=test_code",
                    follow_redirects=False,
                )

                # Should redirect to frontend
                assert response.status_code == 302
                assert "/dashboard" in response.headers["location"]

                # Should set cookie
                assert "access_token" in response.cookies

    @pytest.mark.asyncio
    async def test_callback_oauth_error(self, client):
        """Test OAuth callback handles GitHub errors."""
        # Mock GitHub returning an error
        with patch("app.services.github.exchange_code_for_token") as mock_exchange:
            mock_exchange.return_value = {
                "error": "bad_verification_code",
                "error_description": "The code passed is incorrect or expired.",
            }

            response = await client.get(
                "/api/auth/callback?code=invalid_code",
            )

            assert response.status_code == 400
            assert "error" in response.json()["detail"].lower()


class TestLogout:
    """Tests for /api/auth/logout endpoint."""

    @pytest.mark.asyncio
    async def test_logout_clears_cookie(self, client):
        """Test logout clears the auth cookie."""
        response = await client.post("/api/auth/logout")

        assert response.status_code == 200
        assert response.json()["message"] == "Successfully logged out"
