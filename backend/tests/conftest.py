"""
Pytest Configuration and Fixtures.

Provides fixtures for:
- In-memory test database
- HTTP test client (unauthenticated and authenticated)
- Mock GitHub responses
- Authenticated test user

The authenticated_client fixture creates a client with a valid JWT
cookie, simulating a logged-in user for endpoint tests.
"""

from datetime import datetime
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.dependencies import get_db
from app.main import app
from app.models.user import User
from app.services.security import create_access_token

# Use SQLite for tests - fast and no external dependencies
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a fresh in-memory database for each test.

    Uses SQLite for speed - no need for PostgreSQL in tests.
    Each test gets a clean database.
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create unauthenticated test HTTP client with database override."""

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(test_db: AsyncSession) -> User:
    """Create a test user in the database."""
    user = User(
        github_id=12345678,
        username="testuser",
        email="test@example.com",
        name="Test User",
        avatar_url="https://example.com/avatar.jpg",
        bio="Test bio",
        company="Test Company",
        location="Test City",
        blog="https://testblog.com",
        public_repos=10,
        followers=100,
        following=50,
        access_token="test_github_token",
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest_asyncio.fixture
async def authenticated_client(
    test_db: AsyncSession,
    test_user: User,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Create authenticated test client with valid JWT cookie.

    This simulates a logged-in user by including the JWT token
    as an HTTP-only cookie in every request.
    """

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    # Create JWT token for test user
    token = create_access_token(test_user.id)

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        cookies={"access_token": token},
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def mock_github_user() -> dict:
    """Sample GitHub user profile response."""
    return {
        "id": 12345678,
        "login": "testuser",
        "email": "test@example.com",
        "name": "Test User",
        "avatar_url": "https://example.com/avatar.jpg",
        "bio": "Test bio",
        "company": "Test Company",
        "location": "Test City",
        "blog": "https://testblog.com",
        "public_repos": 10,
        "followers": 100,
        "following": 50,
    }


@pytest.fixture
def mock_github_token() -> dict:
    """Sample GitHub OAuth token response."""
    return {
        "access_token": "gho_test_token_12345",
        "token_type": "bearer",
        "scope": "read:user,user:email,repo",
    }


@pytest.fixture
def mock_repos() -> list[dict]:
    """Sample repository data matching GitHub API structure."""
    return [
        {
            "name": "awesome-project",
            "full_name": "testuser/awesome-project",
            "description": "An awesome project",
            "html_url": "https://github.com/testuser/awesome-project",
            "language": "Python",
            "stargazers_count": 100,
            "forks_count": 25,
            "private": False,
            "fork": False,
            "updated_at": "2024-01-15T10:00:00Z",
            "owner": {"login": "testuser"},
        },
        {
            "name": "secret-project",
            "full_name": "testuser/secret-project",
            "description": "A private project",
            "html_url": "https://github.com/testuser/secret-project",
            "language": "TypeScript",
            "stargazers_count": 0,
            "forks_count": 0,
            "private": True,
            "fork": False,
            "updated_at": "2024-01-10T10:00:00Z",
            "owner": {"login": "testuser"},
        },
    ]


@pytest.fixture
def mock_events() -> list[dict]:
    """Sample GitHub events data."""
    now = datetime.utcnow().isoformat() + "Z"
    return [
        {
            "type": "PushEvent",
            "created_at": now,
            "payload": {
                "commits": [
                    {"sha": "abc123", "message": "Fix bug"},
                    {"sha": "def456", "message": "Add feature"},
                ],
            },
        },
        {
            "type": "PullRequestEvent",
            "created_at": now,
            "payload": {"action": "opened"},
        },
        {
            "type": "IssuesEvent",
            "created_at": now,
            "payload": {"action": "opened"},
        },
        {
            "type": "WatchEvent",
            "created_at": now,
            "payload": {"action": "started"},
        },
    ]


@pytest.fixture
def mock_search_commits() -> list[dict]:
    """
    Sample commit search results matching GitHub Search Commits API.

    The Search API returns items with a 'commit' object containing
    'committer.date' for the commit timestamp.
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


@pytest.fixture
def mock_languages() -> dict[str, int]:
    """Sample repository languages data."""
    return {
        "Python": 50000,
        "JavaScript": 30000,
        "TypeScript": 15000,
        "HTML": 5000,
    }
