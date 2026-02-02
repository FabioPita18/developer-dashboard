"""
Async SQLAlchemy Database Configuration.

This module sets up the async database engine and session factory.
We use SQLAlchemy 2.0 with asyncpg driver for PostgreSQL.

Key components:
- engine: Connection pool to the database
- async_session_factory: Creates new sessions for each request
- Base: Base class for all ORM models

Why async?
    Async database operations don't block the event loop.
    This allows handling many concurrent requests efficiently.
    FastAPI is async-first, so we match that pattern.

Connection Pooling:
    - pool_size: Number of persistent connections
    - max_overflow: Additional connections under load
    - pool_pre_ping: Check if connection is alive before use
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

# Get settings
settings = get_settings()

# Create async engine with connection pool
# echo=True logs SQL statements (useful for debugging)
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL in debug mode
    pool_pre_ping=True,  # Verify connections are alive
    pool_size=5,  # Base number of connections
    max_overflow=10,  # Extra connections under load
)

# Session factory
# Creates new AsyncSession instances for each request
# expire_on_commit=False: Objects remain usable after commit
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    SQLAlchemy 2.0 uses DeclarativeBase instead of declarative_base().
    All models should inherit from this class.

    Example:
        class User(Base):
            __tablename__ = "users"
            id: Mapped[int] = mapped_column(primary_key=True)
    """

    pass


async def create_tables() -> None:
    """
    Create all tables in the database.

    This is for development/testing only.
    In production, use Alembic migrations.

    Usage:
        import asyncio
        from app.database import create_tables
        asyncio.run(create_tables())
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    """
    Drop all tables. DANGEROUS - for testing only!

    This permanently deletes all data.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_db_session() -> AsyncSession:
    """
    Get a database session.

    This is a simpler version without the generator pattern.
    Useful for scripts and background tasks.

    Usage:
        session = await get_db_session()
        try:
            # Use session
        finally:
            await session.close()
    """
    return async_session_factory()
