"""
Developer Dashboard Backend Application.

This package contains the FastAPI application for the Developer Dashboard,
which provides GitHub analytics and visualization APIs.

Architecture:
- main.py: FastAPI application factory and configuration
- config.py: Environment configuration using Pydantic Settings
- database.py: SQLAlchemy async engine and session management
- dependencies.py: FastAPI dependency injection
- models/: SQLAlchemy ORM models
- schemas/: Pydantic schemas for API validation
- routers/: API endpoint handlers
- services/: Business logic and external API clients
"""

__version__ = "0.1.0"
