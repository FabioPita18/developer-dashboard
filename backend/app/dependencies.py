"""
FastAPI Dependency Injection.

This module defines reusable dependencies for FastAPI routes.
Dependencies are functions that provide common resources/data.

Why Dependencies?
    - Reusable across many endpoints
    - Easy to test (can override in tests)
    - Automatic cleanup (using yield/async generators)
    - Clear separation of concerns

Common Patterns:
    - get_db: Provides database session (auto-cleanup)
    - get_current_user: Extracts authenticated user (raises 401)
    - get_optional_user: Extracts user if authenticated (allows None)

Usage:
    @router.get("/protected")
    async def protected(
        user: Annotated[User, Depends(get_current_user)],
        db: Annotated[AsyncSession, Depends(get_db)],
    ):
        # user and db are automatically injected
        pass
"""
from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory
from app.models.user import User
from app.services.security import get_user_id_from_token


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency.

    Creates a new database session for each request.
    Automatically closes the session when request completes.

    Usage:
        @router.get("/items")
        async def get_items(
            db: Annotated[AsyncSession, Depends(get_db)],
        ):
            # Use db here
            pass

    Why AsyncGenerator?
        The 'yield' pattern allows cleanup after the route completes.
        Everything after yield runs after the response is sent.

    Session Lifecycle:
        1. Create session
        2. Yield to route handler
        3. Route uses session
        4. Session closes (finally block)
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """
    Get the currently authenticated user.

    Extracts JWT from HTTP-only cookie, validates it,
    and returns the corresponding User object.

    Raises:
        HTTPException 401 if not authenticated

    Authentication Flow:
        1. Get 'access_token' cookie from request
        2. Verify JWT and extract user ID
        3. Fetch user from database
        4. Return user or raise 401

    Why HTTP-only Cookie?
        - Can't be accessed by JavaScript (XSS protection)
        - Automatically included in requests
        - More secure than localStorage
    """
    # Get token from HTTP-only cookie
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify token and get user ID
    user_id = get_user_id_from_token(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch user from database
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_optional_user(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User | None:
    """
    Get the current user if authenticated, None otherwise.

    Similar to get_current_user but doesn't raise 401.
    Useful for endpoints that work differently based on auth status.

    When to Use:
        - Public pages with optional personalization
        - Endpoints that have different behavior when authenticated
        - GET /api/auth/status (returns user or null)
    """
    try:
        return await get_current_user(request, db)
    except HTTPException:
        return None


# Type aliases for cleaner route signatures
# These combine the type annotation with the dependency

# Database session dependency type
DbSession = Annotated[AsyncSession, Depends(get_db)]

# Required authenticated user dependency type
CurrentUser = Annotated[User, Depends(get_current_user)]

# Optional authenticated user dependency type
OptionalUser = Annotated[User | None, Depends(get_optional_user)]
