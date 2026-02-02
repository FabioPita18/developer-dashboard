"""
Authentication Router - GitHub OAuth Endpoints.

This module handles the GitHub OAuth authentication flow:
1. /github - Initiates OAuth by redirecting to GitHub
2. /callback - Handles GitHub redirect with auth code
3. /logout - Clears authentication
4. /status - Checks if user is authenticated

OAuth Flow:
    1. User visits /api/auth/github
    2. Redirected to GitHub login page
    3. User authorizes our app
    4. GitHub redirects to /api/auth/callback?code=xxx
    5. We exchange code for access token
    6. Fetch user profile from GitHub
    7. Create/update user in database
    8. Create JWT and set as HTTP-only cookie
    9. Redirect to frontend dashboard
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.dependencies import get_db, get_optional_user
from app.models.user import User
from app.schemas.user import AuthStatus, UserResponse
from app.services import github, security

settings = get_settings()

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.get(
    "/github",
    summary="Initiate GitHub OAuth login",
    description="Redirects user to GitHub for authentication. "
    "After authorization, GitHub redirects back to /callback.",
    response_class=RedirectResponse,
)
async def github_login() -> RedirectResponse:
    """
    Initiate GitHub OAuth flow.

    This endpoint redirects the user to GitHub's authorization page.
    After the user authorizes (or denies), GitHub redirects back
    to our callback URL.

    No authentication required - this is the login entry point.
    """
    authorization_url = github.get_authorization_url()
    return RedirectResponse(url=authorization_url)


@router.get(
    "/callback",
    summary="GitHub OAuth callback",
    description="Handles the OAuth callback from GitHub. "
    "Exchanges code for token, creates user, sets cookie.",
    response_class=RedirectResponse,
)
async def github_callback(
    code: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RedirectResponse:
    """
    Handle GitHub OAuth callback.

    This is where GitHub redirects after user authorizes.
    The 'code' parameter is a temporary authorization code.

    Flow:
        1. Exchange code for access token
        2. Fetch user profile from GitHub
        3. Create or update user in database
        4. Create JWT token
        5. Set JWT as HTTP-only cookie
        6. Redirect to frontend dashboard

    Args:
        code: Authorization code from GitHub
        db: Database session

    Returns:
        Redirect to frontend with auth cookie set

    Raises:
        HTTPException 400 if code exchange fails
    """
    # Step 1: Exchange code for access token
    token_data = await github.exchange_code_for_token(code)

    # Check for OAuth errors
    if "error" in token_data:
        error_description = token_data.get("error_description", "Unknown OAuth error")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"GitHub OAuth error: {error_description}",
        )

    access_token = token_data["access_token"]

    # Step 2: Fetch user profile
    try:
        user_data = await github.get_user_profile(access_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch GitHub profile: {str(e)}",
        )

    # Step 3: Create or update user
    user = await security.create_or_update_user(db, user_data, access_token)

    # Step 4: Create JWT token
    jwt_token = security.create_access_token(user.id)

    # Step 5: Create redirect response
    redirect_url = f"{settings.frontend_url}/dashboard"
    response = RedirectResponse(
        url=redirect_url,
        status_code=status.HTTP_302_FOUND,
    )

    # Step 6: Set HTTP-only cookie
    # Cookie settings for security:
    # - httponly: JavaScript cannot access (XSS protection)
    # - secure: Only HTTPS in production (man-in-middle protection)
    # - samesite: CSRF protection
    # - max_age: Cookie expiration
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=not settings.is_development,  # HTTPS only in prod
        samesite="lax",  # Allows same-site navigations
        max_age=settings.access_token_expire_minutes * 60,
        path="/",  # Cookie available for all paths
    )

    return response


@router.post(
    "/logout",
    summary="Logout user",
    description="Clears the authentication cookie.",
    status_code=status.HTTP_200_OK,
)
async def logout(response: Response) -> dict[str, str]:
    """
    Log out the current user.

    Clears the HTTP-only cookie by setting it to expire immediately.
    The 'delete_cookie' method sets max_age=0.

    Returns:
        Success message
    """
    # Delete the authentication cookie
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        secure=not settings.is_development,
        samesite="lax",
    )

    return {"message": "Successfully logged out"}


@router.get(
    "/status",
    summary="Check authentication status",
    description="Returns whether the user is authenticated and their profile.",
    response_model=AuthStatus,
)
async def auth_status(
    user: Annotated[User | None, Depends(get_optional_user)],
) -> AuthStatus:
    """
    Check if the current request is authenticated.

    Uses the optional user dependency - doesn't require auth.
    Returns authenticated=true with user data, or authenticated=false.

    This endpoint is called by the frontend on app load
    to determine if the user is logged in.
    """
    if user:
        return AuthStatus(
            authenticated=True,
            user=UserResponse.model_validate(user),
        )

    return AuthStatus(
        authenticated=False,
        user=None,
    )
