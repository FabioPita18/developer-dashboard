"""
Pytest Configuration and Fixtures.

This module provides shared fixtures for all tests.

Fixtures:
- test_db: In-memory SQLite database for fast tests
- client: Async HTTP client for API testing
- mock_github_user: Sample GitHub user data
- mock_github_token: Sample GitHub OAuth token response
"""
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.dependencies import get_db
from app.main import app

# Use SQLite for tests - fast and no external dependencies
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def test_db():
    """
    Create a fresh in-memory database for each test.

    Uses SQLite for speed - no need for PostgreSQL in tests.
    Each test gets a clean database.
    """
    # Create engine
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session factory
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Yield session for test
    async with async_session() as session:
        yield session

    # Drop all tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Dispose engine
    await engine.dispose()


@pytest_asyncio.fixture
async def client(test_db):
    """
    Create async HTTP client with database override.

    The client uses the test database instead of production.
    """
    # Override database dependency
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    # Create async client
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # Clear overrides
    app.dependency_overrides.clear()


@pytest.fixture
def mock_github_user():
    """
    Sample GitHub user data for tests.

    Matches the structure returned by GitHub's /user endpoint.
    """
    return {
        "id": 12345678,
        "login": "testuser",
        "email": "test@example.com",
        "name": "Test User",
        "avatar_url": "https://avatars.githubusercontent.com/u/12345678",
        "bio": "Test bio for testing",
        "company": "Test Company",
        "location": "Test City",
        "blog": "https://testblog.com",
        "public_repos": 42,
        "followers": 100,
        "following": 50,
    }


@pytest.fixture
def mock_github_token():
    """Sample GitHub OAuth token response."""
    return {
        "access_token": "gho_test_token_12345",
        "token_type": "bearer",
        "scope": "read:user,user:email,repo",
    }
