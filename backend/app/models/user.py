"""
User Model - Stores GitHub OAuth user data.

This model stores information about authenticated users,
including their GitHub profile data and OAuth access token.

SQLAlchemy 2.0 Syntax:
- Mapped[type]: Type annotation for ORM columns
- mapped_column(): Define column properties
- Optional[type] or type | None: Nullable fields

Security Note:
    The access_token field stores the GitHub OAuth token.
    This token allows making API calls on the user's behalf.
    NEVER expose this field in API responses!
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# TYPE_CHECKING prevents circular imports at runtime
# The import only happens during type checking (mypy, IDE)
if TYPE_CHECKING:
    from app.models.cache import CachedData


class User(Base):
    """
    User model for authenticated GitHub users.

    Stores both GitHub profile information and our session data.
    The github_id is the unique identifier from GitHub.
    """

    __tablename__ = "users"

    # =========================================================================
    # Primary Key
    # =========================================================================

    # Our internal user ID (auto-incremented)
    id: Mapped[int] = mapped_column(primary_key=True)

    # =========================================================================
    # GitHub Identity
    # =========================================================================

    # GitHub's unique user ID (never changes, even if username changes)
    # Using BigInteger because GitHub IDs can be large numbers
    github_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        comment="Unique GitHub user ID",
    )

    # GitHub username (can be changed by user, but unique at any time)
    username: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        comment="GitHub username (login)",
    )

    # =========================================================================
    # Profile Information (from GitHub API)
    # =========================================================================

    # Email may be null if user has private email
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="User email (may be private)",
    )

    # Display name (can be different from username)
    name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Display name",
    )

    # Profile picture URL
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="GitHub avatar URL",
    )

    # User bio (can be long, use Text type)
    bio: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="User biography",
    )

    # Company name
    company: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Company name",
    )

    # Location string
    location: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="User location",
    )

    # Blog/website URL
    blog: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Blog or website URL",
    )

    # =========================================================================
    # GitHub Statistics
    # =========================================================================

    # Number of public repositories
    public_repos: Mapped[int] = mapped_column(
        default=0,
        comment="Number of public repositories",
    )

    # Follower/following counts
    followers: Mapped[int] = mapped_column(
        default=0,
        comment="Number of followers",
    )

    following: Mapped[int] = mapped_column(
        default=0,
        comment="Number of users following",
    )

    # =========================================================================
    # Authentication
    # =========================================================================

    # GitHub OAuth access token
    # SECURITY: Never expose this in API responses!
    access_token: Mapped[str] = mapped_column(
        String(255),
        comment="GitHub OAuth access token (SENSITIVE)",
    )

    # =========================================================================
    # Timestamps
    # =========================================================================

    # When user first authenticated
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        comment="Account creation timestamp",
    )

    # When user data was last updated
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="Last update timestamp",
    )

    # When user last logged in
    last_login_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        comment="Last login timestamp",
    )

    # =========================================================================
    # Relationships
    # =========================================================================

    # One-to-many relationship with CachedData
    # cascade="all, delete-orphan": Delete cache when user is deleted
    cached_data: Mapped[list["CachedData"]] = relationship(
        "CachedData",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",  # Efficient loading strategy
    )

    # =========================================================================
    # Table Configuration
    # =========================================================================

    __table_args__ = (
        # Composite indexes for common queries
        Index("ix_users_github_username", "github_id", "username"),
        # Table comment for documentation
        {"comment": "GitHub OAuth authenticated users"},
    )

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<User id={self.id} username={self.username}>"
