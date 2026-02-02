"""
Security Service - JWT Token Management.

This module handles:
- JWT token creation and validation
- User creation/update from OAuth data
- Token payload structure

JWT (JSON Web Token) Overview:
    JWT is a standard for securely transmitting information.
    Each token has three parts: header.payload.signature

    We use JWT for stateless authentication:
    - User logs in via GitHub OAuth
    - We create a JWT and store it in an HTTP-only cookie
    - Each request includes the cookie automatically
    - We validate the JWT to identify the user

Security Considerations:
    - Tokens have short expiration (30 minutes default)
    - HTTP-only cookies prevent JavaScript access (XSS protection)
    - Secure flag ensures HTTPS-only in production
    - SameSite flag provides CSRF protection
"""

from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.user import User

settings = get_settings()


def create_access_token(
    user_id: int,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a JWT access token for a user.

    Args:
        user_id: The database ID of the user
        expires_delta: Custom expiration time (optional)

    Returns:
        Encoded JWT string

    Token Payload Structure:
        - sub (subject): User ID as string
        - exp (expiration): When token expires
        - iat (issued at): When token was created
        - type: Token type identifier

    Example payload:
        {
            "sub": "123",
            "exp": 1705320000,
            "iat": 1705318200,
            "type": "access"
        }
    """
    # Calculate expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    # Build the token payload
    payload = {
        "sub": str(user_id),  # Subject (who the token is about)
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at
        "type": "access",  # Token type
    }

    # Encode and return the JWT
    encoded: str = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded


def verify_token(token: str) -> dict[str, Any] | None:
    """
    Verify and decode a JWT token.

    Args:
        token: The JWT string to verify

    Returns:
        Decoded payload dict if valid, None if invalid/expired

    The function handles:
    - Signature verification (is it tampered?)
    - Expiration check (is it still valid?)
    - Algorithm validation (is it the expected algorithm?)
    """
    try:
        # Decode and verify the token
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        # Token is invalid, expired, or tampered
        return None


def get_user_id_from_token(token: str) -> int | None:
    """
    Extract user ID from a valid JWT token.

    Args:
        token: The JWT string

    Returns:
        User ID as integer, or None if token is invalid

    This is a convenience function that:
    1. Verifies the token
    2. Extracts the 'sub' claim
    3. Converts to integer
    """
    payload = verify_token(token)

    if not payload:
        return None

    # Get the subject (user ID)
    user_id_str = payload.get("sub")

    if not user_id_str:
        return None

    try:
        return int(user_id_str)
    except ValueError:
        return None


async def get_user_by_github_id(
    db: AsyncSession,
    github_id: int,
) -> User | None:
    """
    Find a user by their GitHub ID.

    Args:
        db: Database session
        github_id: GitHub's unique user ID

    Returns:
        User if found, None otherwise
    """
    stmt = select(User).where(User.github_id == github_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_or_update_user(
    db: AsyncSession,
    github_data: dict[str, Any],
    access_token: str,
) -> User:
    """
    Create a new user or update existing from GitHub OAuth data.

    This function is called after successful GitHub OAuth:
    1. Check if user exists (by github_id)
    2. If exists, update their profile data
    3. If new, create a user record

    Args:
        db: Database session
        github_data: User profile from GitHub API
        access_token: GitHub OAuth access token

    Returns:
        The created or updated User object

    GitHub Data Fields Used:
        - id: Unique GitHub user ID
        - login: Username
        - email: Email (may be null)
        - name: Display name
        - avatar_url: Profile picture
        - bio: Biography
        - company: Company name
        - location: Location
        - blog: Website URL
        - public_repos: Repository count
        - followers: Follower count
        - following: Following count
    """
    # Check if user already exists
    user = await get_user_by_github_id(db, github_data["id"])

    if user:
        # Update existing user
        user.username = github_data["login"]
        user.email = github_data.get("email")
        user.name = github_data.get("name")
        user.avatar_url = github_data.get("avatar_url")
        user.bio = github_data.get("bio")
        user.company = github_data.get("company")
        user.location = github_data.get("location")
        user.blog = github_data.get("blog")
        user.public_repos = github_data.get("public_repos", 0)
        user.followers = github_data.get("followers", 0)
        user.following = github_data.get("following", 0)
        user.access_token = access_token
        user.last_login_at = datetime.utcnow()
        user.updated_at = datetime.utcnow()
    else:
        # Create new user
        user = User(
            github_id=github_data["id"],
            username=github_data["login"],
            email=github_data.get("email"),
            name=github_data.get("name"),
            avatar_url=github_data.get("avatar_url"),
            bio=github_data.get("bio"),
            company=github_data.get("company"),
            location=github_data.get("location"),
            blog=github_data.get("blog"),
            public_repos=github_data.get("public_repos", 0),
            followers=github_data.get("followers", 0),
            following=github_data.get("following", 0),
            access_token=access_token,
        )
        db.add(user)

    # Commit changes
    await db.commit()
    await db.refresh(user)

    return user
