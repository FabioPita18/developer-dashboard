"""
SQLAlchemy ORM Models.

This package contains all database models for the application.
Models use SQLAlchemy 2.0 declarative mapping with Mapped[] type hints.

Models:
- User: GitHub OAuth user data and authentication
- CachedData: Cached GitHub API responses for performance

Import all models here to ensure they're registered with SQLAlchemy
before creating tables or running migrations.
"""
from app.models.cache import CachedData
from app.models.user import User

# Export all models
__all__ = ["User", "CachedData"]
