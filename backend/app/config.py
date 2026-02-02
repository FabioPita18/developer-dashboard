"""
Application Configuration using Pydantic Settings.

This module provides type-safe configuration management.
Settings are loaded from environment variables and .env file.

Pydantic Settings benefits:
- Type validation (strings, integers, booleans)
- Default values
- Environment variable override
- .env file support
- IDE autocompletion

Usage:
    from app.config import get_settings
    settings = get_settings()
    print(settings.database_url)

Why @lru_cache?
    Settings are loaded once and cached. This prevents
    re-reading environment variables on every request.
"""
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.

    All settings can be overridden by environment variables.
    Environment variables take precedence over .env file.
    """

    # =========================================================================
    # Application Settings
    # =========================================================================

    app_name: str = "Developer Dashboard"
    debug: bool = False
    environment: Literal["development", "staging", "production"] = "development"

    # =========================================================================
    # Database Settings
    # =========================================================================

    # Full database URL including the asyncpg driver
    # Format: postgresql+asyncpg://user:password@host:port/database
    database_url: str = "postgresql+asyncpg://devdash_user:devdash_password@localhost:5434/devdash_db"

    # =========================================================================
    # GitHub OAuth Settings
    # =========================================================================

    # Create OAuth App at: https://github.com/settings/developers
    github_client_id: str = ""
    github_client_secret: str = ""
    github_redirect_uri: str = "http://localhost:8000/api/auth/callback"

    # OAuth scopes determine what permissions we request
    # read:user - Basic profile info
    # user:email - Email addresses
    # repo - Full repository access (needed for private repos)
    github_scopes: str = "read:user user:email repo"

    # =========================================================================
    # JWT Authentication Settings
    # =========================================================================

    # Secret key for signing JWT tokens
    # IMPORTANT: Generate a secure key for production!
    # Use: openssl rand -hex 32
    jwt_secret_key: str = "your-super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"

    # Token expiration times
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # =========================================================================
    # CORS Settings
    # =========================================================================

    # Frontend URL for CORS - must match exactly
    frontend_url: str = "http://localhost:3000"

    # =========================================================================
    # Caching Settings
    # =========================================================================

    # How long to cache GitHub API responses (in seconds)
    # 86400 = 24 hours
    cache_ttl_seconds: int = 86400

    # =========================================================================
    # Pydantic Settings Configuration
    # =========================================================================

    model_config = SettingsConfigDict(
        # Load from .env file in the project root (one level up from backend/)
        env_file="../.env",
        env_file_encoding="utf-8",
        # Case-insensitive environment variable names
        # DATABASE_URL, database_url, Database_Url all work
        case_sensitive=False,
        # Don't raise error for extra env vars
        extra="ignore",
    )

    @property
    def github_scopes_list(self) -> list[str]:
        """
        Convert space-separated scopes string to list.

        Example:
            "read:user user:email repo" -> ["read:user", "user:email", "repo"]
        """
        return self.github_scopes.split()

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    The @lru_cache decorator ensures:
    1. Settings are only loaded once
    2. Same instance is returned on subsequent calls
    3. Better performance (no repeated env var reads)

    To reload settings (e.g., in tests), use:
        get_settings.cache_clear()
    """
    return Settings()
