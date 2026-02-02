"""
Alembic Migration Environment Configuration.

This file configures Alembic for async SQLAlchemy.
It handles loading the database URL and model metadata.

Key configuration:
- Uses async database engine
- Loads URL from environment/settings
- Imports all models for autogenerate
"""
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Import our application components
# This also imports all models, registering them with Base.metadata
from app.config import get_settings
from app.database import Base
from app.models import User, CachedData  # noqa: F401 - Ensures models are loaded

# Alembic Config object
config = context.config

# Get settings
settings = get_settings()

# Set the database URL from our settings
# This overrides any value in alembic.ini
config.set_main_option("sqlalchemy.url", settings.database_url)

# Configure Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
# This is our Base.metadata which includes all models
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This generates SQL without connecting to the database.
    Useful for generating migration scripts for review.

    Usage: alembic upgrade head --sql
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Run migrations with the given connection.

    This is the actual migration execution.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # Compare types when detecting changes
        compare_type=True,
        # Compare server defaults
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Run migrations in async mode.

    Creates an async engine and runs migrations.
    This is the default mode for our async application.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    This connects to the database and runs migrations.
    Uses asyncio for our async setup.
    """
    asyncio.run(run_async_migrations())


# Determine which mode to run
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
