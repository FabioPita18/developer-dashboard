"""
Analytics Endpoint Tests.

Tests the analytics data processing endpoints.
Uses mocked GitHub API responses to avoid real API calls.

Important: The analytics service uses two data sources:
- GitHub Search Commits API (via search_user_commits / get_all_user_commits)
  for accurate commit counts
- GitHub Events API (via get_all_events) for PR and issue counts

Both must be mocked in tests that hit contribution/stats endpoints.

Endpoints tested:
- GET /api/analytics/stats: Aggregated statistics
- GET /api/analytics/contributions: Contribution timeline
- GET /api/analytics/languages: Language breakdown
- GET /api/analytics/repositories: Top repositories
- GET /api/analytics/heatmap: Activity heatmap
"""
import pytest
from unittest.mock import patch


class TestGetStats:
    """Tests for GET /api/analytics/stats endpoint."""

    @pytest.mark.asyncio
    async def test_returns_stats(
        self, authenticated_client, test_user, mock_repos
    ):
        """Should return aggregated statistics."""
        with patch("app.services.github.get_all_repos") as mock_get_repos:
            with patch("app.services.github.search_user_commits") as mock_search:
                mock_get_repos.return_value = mock_repos
                # search_user_commits returns (items, total_count, links)
                mock_search.return_value = ([], 42, {})

                response = await authenticated_client.get(
                    "/api/analytics/stats"
                )

                assert response.status_code == 200
                data = response.json()
                assert "total_stars" in data
                assert "total_forks" in data
                assert "public_repos" in data
                assert "private_repos" in data
                assert "total_commits" in data
                assert data["total_stars"] == 100  # 100 + 0 from mock repos
                assert data["total_forks"] == 25  # 25 + 0
                assert data["public_repos"] == 1
                assert data["private_repos"] == 1
                assert data["total_commits"] == 42

    @pytest.mark.asyncio
    async def test_requires_authentication(self, client):
        """Should return 401 when not authenticated."""
        response = await client.get("/api/analytics/stats")

        assert response.status_code == 401


class TestGetContributions:
    """Tests for GET /api/analytics/contributions endpoint."""

    @pytest.mark.asyncio
    async def test_returns_contributions(
        self, authenticated_client, test_user, mock_events, mock_search_commits
    ):
        """Should return contribution timeline."""
        with patch("app.services.github.get_all_user_commits") as mock_commits:
            with patch("app.services.github.get_all_events") as mock_get_events:
                mock_commits.return_value = mock_search_commits
                mock_get_events.return_value = mock_events

                response = await authenticated_client.get(
                    "/api/analytics/contributions?days=30"
                )

                assert response.status_code == 200
                data = response.json()
                assert isinstance(data, list)
                assert len(data) == 30
                assert all("date" in point for point in data)
                assert all("commits" in point for point in data)
                assert all("pull_requests" in point for point in data)
                assert all("issues" in point for point in data)

    @pytest.mark.asyncio
    async def test_custom_days_parameter(
        self, authenticated_client, test_user, mock_events, mock_search_commits
    ):
        """Should respect days parameter."""
        with patch("app.services.github.get_all_user_commits") as mock_commits:
            with patch("app.services.github.get_all_events") as mock_get_events:
                mock_commits.return_value = mock_search_commits
                mock_get_events.return_value = mock_events

                response = await authenticated_client.get(
                    "/api/analytics/contributions?days=7"
                )

                assert response.status_code == 200
                assert len(response.json()) == 7

    @pytest.mark.asyncio
    async def test_days_validation(self, authenticated_client, test_user):
        """Should validate days parameter range (1-90)."""
        # Test too high
        response = await authenticated_client.get(
            "/api/analytics/contributions?days=100"
        )
        assert response.status_code == 422

        # Test too low
        response = await authenticated_client.get(
            "/api/analytics/contributions?days=0"
        )
        assert response.status_code == 422


class TestGetLanguages:
    """Tests for GET /api/analytics/languages endpoint."""

    @pytest.mark.asyncio
    async def test_returns_languages(
        self, authenticated_client, test_user, mock_repos, mock_languages
    ):
        """Should return language breakdown."""
        with patch("app.services.github.get_all_repos") as mock_get_repos:
            with patch("app.services.github.get_repo_languages") as mock_get_langs:
                mock_get_repos.return_value = mock_repos
                mock_get_langs.return_value = mock_languages

                response = await authenticated_client.get(
                    "/api/analytics/languages"
                )

                assert response.status_code == 200
                data = response.json()
                assert isinstance(data, list)
                if data:
                    assert all("language" in lang for lang in data)
                    assert all("percentage" in lang for lang in data)
                    assert all("color" in lang for lang in data)


class TestGetRepositories:
    """Tests for GET /api/analytics/repositories endpoint."""

    @pytest.mark.asyncio
    async def test_returns_repos_sorted_by_stars(
        self, authenticated_client, test_user, mock_repos
    ):
        """Should return repositories sorted by stars descending."""
        with patch("app.services.github.get_all_repos") as mock_get:
            mock_get.return_value = mock_repos

            response = await authenticated_client.get(
                "/api/analytics/repositories"
            )

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 2
            # First repo should have more stars
            if len(data) > 1:
                assert data[0]["stars"] >= data[1]["stars"]

    @pytest.mark.asyncio
    async def test_limit_parameter(
        self, authenticated_client, test_user, mock_repos
    ):
        """Should respect limit parameter."""
        with patch("app.services.github.get_all_repos") as mock_get:
            mock_get.return_value = mock_repos * 5  # 10 repos

            response = await authenticated_client.get(
                "/api/analytics/repositories?limit=3"
            )

            assert response.status_code == 200
            assert len(response.json()) <= 3


class TestGetHeatmap:
    """Tests for GET /api/analytics/heatmap endpoint."""

    @pytest.mark.asyncio
    async def test_returns_heatmap(
        self, authenticated_client, test_user, mock_events
    ):
        """Should return activity heatmap data."""
        with patch("app.services.github.get_all_events") as mock_get:
            mock_get.return_value = mock_events

            response = await authenticated_client.get("/api/analytics/heatmap")

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            # Should have 7 days * 24 hours = 168 points
            assert len(data) == 168
            assert all("day" in point for point in data)
            assert all("hour" in point for point in data)
            assert all("count" in point for point in data)
