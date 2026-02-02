"""
CachedData Model - Caches GitHub API responses.

Caching is essential because:
1. GitHub API has rate limits (5000 requests/hour)
2. API calls are slow compared to database queries
3. Data doesn't change frequently

We use PostgreSQL as our cache store instead of Redis because:
- Simpler infrastructure (one less service)
- Data persists across restarts
- Can query and debug cache contents with SQL
- PostgreSQL JSON support is excellent

Trade-offs:
- Slightly slower than Redis for simple key-value
- Uses database connections
- For our use case, these trade-offs are acceptable
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class CachedData(Base):
    """
    Cache entry for GitHub API responses.

    Each entry stores:
    - user_id: Which user this cache belongs to
    - cache_key: What type of data (e.g., "user_stats", "languages")
    - data: The actual cached data as JSON
    - expires_at: When this cache should be considered stale

    Example cache_keys:
    - "user_stats": Aggregated statistics
    - "contributions_30": 30-day contribution data
    - "languages": Language breakdown
    - "repositories_10": Top 10 repositories
    - "heatmap": Activity heatmap data
    """

    __tablename__ = "cached_data"

    # =========================================================================
    # Primary Key
    # =========================================================================

    id: Mapped[int] = mapped_column(primary_key=True)

    # =========================================================================
    # Foreign Key
    # =========================================================================

    # Link to the user who owns this cache
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        comment="User who owns this cache entry",
    )

    # =========================================================================
    # Cache Key
    # =========================================================================

    # Identifier for the type of cached data
    cache_key: Mapped[str] = mapped_column(
        String(100),
        index=True,
        comment="Cache key identifier (e.g., 'user_stats', 'languages')",
    )

    # =========================================================================
    # Cached Data
    # =========================================================================

    # The actual cached data stored as JSON
    # PostgreSQL has native JSON support with indexing capabilities
    data: Mapped[dict[str, Any] | list[Any]] = mapped_column(
        JSON,
        comment="Cached JSON data",
    )

    # =========================================================================
    # Expiration
    # =========================================================================

    # When this cache entry expires
    expires_at: Mapped[datetime] = mapped_column(
        index=True,
        comment="Cache expiration timestamp",
    )

    # =========================================================================
    # Timestamps
    # =========================================================================

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        comment="Cache creation timestamp",
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="Last update timestamp",
    )

    # =========================================================================
    # Relationships
    # =========================================================================

    # Many-to-one relationship with User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="cached_data",
    )

    # =========================================================================
    # Table Configuration
    # =========================================================================

    __table_args__ = (
        # Ensure only one cache entry per user per key
        UniqueConstraint(
            "user_id",
            "cache_key",
            name="uq_user_cache_key",
        ),
        # Index for expiration cleanup queries
        Index("ix_cached_data_expires", "expires_at"),
        # Composite index for common lookups
        Index("ix_cached_data_user_key", "user_id", "cache_key"),
        {"comment": "Cached GitHub API responses"},
    )

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<CachedData user_id={self.user_id} key={self.cache_key}>"

    @property
    def is_expired(self) -> bool:
        """
        Check if this cache entry has expired.

        Returns:
            True if current time is past expires_at
        """
        return datetime.utcnow() > self.expires_at

    @property
    def is_valid(self) -> bool:
        """
        Check if this cache entry is still valid (not expired).

        Returns:
            True if cache is still fresh
        """
        return not self.is_expired
