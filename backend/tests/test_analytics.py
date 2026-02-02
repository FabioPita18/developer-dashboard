"""
Analytics Endpoint Tests.

Tests the analytics data processing and caching.
Uses mocked GitHub responses to avoid real API calls.
"""
import pytest
import pytest_asyncio
from datetime import datetime
from unittest.mock import patch

from app.models.user import User
from app.services.security import create_access_token


@pytest_asyncio.fixture
async def test_user(test_db):
    """
    Create a test user in the database.

    Must be async because we need to commit and refresh
    to get the auto-generated ID.
    """
    user = User(
        github_id=12345,
        username="testuser",
        email="test@example.com",
        access_token="test_token",
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user):
    """Create auth headers with valid JWT cookie."""
    token = create_access_token(test_user.id)
    return {"Cookie": f"access_token={token}"}


@pytest.fixture
def mock_repos():
    """Sample repository data matching GitHub API structure."""
    return [
        {
            "name": "repo1",
            "full_name": "testuser/repo1",
            "description": "Test repo 1",
            "html_url": "https://github.com/testuser/repo1",
            "language": "Python",
            "stargazers_count": 100,
            "forks_count": 20,
            "private": False,
            "fork": False,
            "updated_at": "2024-01-15T10:00:00Z",
            "owner": {"login": "testuser"},
        },
        {
            "name": "repo2",
            "full_name": "testuser/repo2",
            "description": "Test repo 2",
            "html_url": "https://github.com/testuser/repo2",
            "language": "JavaScript",
            "stargazers_count": 50,
            "forks_count": 10,
            "private": True,
            "fork": False,
            "updated_at": "2024-01-10T10:00:00Z",
            "owner": {"login": "testuser"},
        },
    ]


@pytest.fixture
def mock_events():
    """Sample event data matching GitHub API structure."""
    return [
        {
            "type": "PushEvent",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "payload": {
                "commits": [{"sha": "abc123"}, {"sha": "def456"}],
            },
        },
        {
            "type": "PullRequestEvent",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "payload": {"action": "opened"},
        },
        {
            "type": "IssuesEvent",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "payload": {"action": "opened"},
        },
    ]


@pytest.fixture
def mock_search_commits():
    """
    Sample commit search results matching GitHub Search Commits API.

    The Search API returns a different structure than the Events API:
    each item has a 'commit' object with 'committer.date'.
    """
    now = datetime.utcnow().isoformat() + "Z"
    return [
        {
            "sha": "abc123",
            "commit": {
                "message": "feat: add feature",
                "committer": {"date": now},
            },
        },
        {
            "sha": "def456",
            "commit": {
                "message": "fix: bug fix",
                "committer": {"date": now},
            },
        },
    ]


class TestUserStats:
    """Tests for /api/analytics/stats endpoint."""

    @pytest.mark.asyncio
    async def test_stats_unauthenticated(self, client):
        """Test that stats require authentication."""
        response = await client.get("/api/analytics/stats")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_stats_success(
        self, client, test_user, auth_headers, mock_repos
    ):
        """Test successful stats retrieval."""
        with patch("app.services.github.get_all_repos") as mock_get_repos:
            with patch("app.services.github.search_user_commits") as mock_search:
                mock_get_repos.return_value = mock_repos
                # search_user_commits returns (items, total_count, links)
                mock_search.return_value = ([], 42, {})

                response = await client.get(
                    "/api/analytics/stats",
                    headers=auth_headers,
                )

                assert response.status_code == 200
                data = response.json()
                assert data["total_stars"] == 150  # 100 + 50
                assert data["total_forks"] == 30   # 20 + 10
                assert data["public_repos"] == 1
                assert data["private_repos"] == 1
                assert data["total_commits"] == 42


class TestLanguages:
    """Tests for /api/analytics/languages endpoint."""

    @pytest.mark.asyncio
    async def test_languages_success(
        self, client, test_user, auth_headers, mock_repos
    ):
        """Test successful language breakdown."""
        mock_languages = {
            "Python": 50000,
            "JavaScript": 30000,
        }

        with patch("app.services.github.get_all_repos") as mock_get_repos:
            with patch("app.services.github.get_repo_languages") as mock_get_langs:
                mock_get_repos.return_value = mock_repos
                mock_get_langs.return_value = mock_languages

                response = await client.get(
                    "/api/analytics/languages",
                    headers=auth_headers,
                )

                assert response.status_code == 200
                data = response.json()
                assert len(data) > 0
                assert all("language" in item for item in data)
                assert all("percentage" in item for item in data)


class TestContributions:
    """Tests for /api/analytics/contributions endpoint."""

    @pytest.mark.asyncio
    async def test_contributions_default_days(
        self, client, test_user, auth_headers, mock_events, mock_search_commits
    ):
        """Test contributions with default 30 days."""
        with patch("app.services.github.get_all_user_commits") as mock_commits:
            with patch("app.services.github.get_all_events") as mock_get_events:
                mock_commits.return_value = mock_search_commits
                mock_get_events.return_value = mock_events

                response = await client.get(
                    "/api/analytics/contributions",
                    headers=auth_headers,
                )

                assert response.status_code == 200
                data = response.json()
                assert len(data) == 30

    @pytest.mark.asyncio
    async def test_contributions_custom_days(
        self, client, test_user, auth_headers, mock_events, mock_search_commits
    ):
        """Test contributions with custom day count."""
        with patch("app.services.github.get_all_user_commits") as mock_commits:
            with patch("app.services.github.get_all_events") as mock_get_events:
                mock_commits.return_value = mock_search_commits
                mock_get_events.return_value = mock_events

                response = await client.get(
                    "/api/analytics/contributions?days=7",
                    headers=auth_headers,
                )

                assert response.status_code == 200
                data = response.json()
                assert len(data) == 7


class TestRepositories:
    """Tests for /api/analytics/repositories endpoint."""

    @pytest.mark.asyncio
    async def test_repositories_sorted_by_stars(
        self, client, test_user, auth_headers, mock_repos
    ):
        """Test repositories are sorted by stars descending."""
        with patch("app.services.github.get_all_repos") as mock_get_repos:
            mock_get_repos.return_value = mock_repos

            response = await client.get(
                "/api/analytics/repositories",
                headers=auth_headers,
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            # First repo should have more stars
            assert data[0]["stars"] >= data[1]["stars"]
