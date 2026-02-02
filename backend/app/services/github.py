"""
GitHub API Service.

This module handles all interactions with the GitHub API:
- OAuth flow (authorization URL, token exchange)
- User profile fetching
- Repository data (expanded in Phase 3)
- Event data (expanded in Phase 3)

OAuth Flow Overview:
    1. User clicks "Login with GitHub"
    2. We redirect to GitHub's authorization page
    3. User authorizes our app
    4. GitHub redirects back with a 'code'
    5. We exchange the code for an access token
    6. We use the token to fetch user data

Rate Limiting:
    GitHub API has rate limits:
    - 5000 requests/hour for authenticated requests
    - 60 requests/hour for unauthenticated
    We cache responses to stay well under the limit.
"""
from typing import Any
from urllib.parse import urlencode

import httpx

from app.config import get_settings

settings = get_settings()

# GitHub API endpoints
GITHUB_API_BASE = "https://api.github.com"
GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"


def get_authorization_url() -> str:
    """
    Build the GitHub OAuth authorization URL.

    This URL is where we redirect users to authorize our app.
    After authorization, GitHub redirects back to our callback URL.

    Returns:
        Full URL to redirect user to

    URL Parameters:
        - client_id: Our GitHub OAuth App ID
        - redirect_uri: Where to redirect after auth
        - scope: Permissions we're requesting
    """
    params = {
        "client_id": settings.github_client_id,
        "redirect_uri": settings.github_redirect_uri,
        "scope": settings.github_scopes,
    }
    return f"{GITHUB_AUTHORIZE_URL}?{urlencode(params)}"


async def exchange_code_for_token(code: str) -> dict[str, Any]:
    """
    Exchange authorization code for access token.

    After user authorizes, GitHub redirects with a 'code' parameter.
    We exchange this code for an access token.

    Args:
        code: Authorization code from GitHub redirect

    Returns:
        Dict containing:
        - access_token: The OAuth token
        - token_type: Usually "bearer"
        - scope: Granted permissions
        OR
        - error: Error code
        - error_description: Human-readable error

    Security Note:
        This exchange happens server-side. The code is single-use
        and expires quickly, preventing replay attacks.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
                "redirect_uri": settings.github_redirect_uri,
            },
            headers={
                # Request JSON response instead of form-encoded
                "Accept": "application/json",
            },
        )

        # GitHub returns 200 even for errors, so check response content
        return response.json()


async def get_user_profile(access_token: str) -> dict[str, Any]:
    """
    Fetch authenticated user's GitHub profile.

    Uses the /user endpoint which returns the profile of the
    authenticated user (determined by the access token).

    Args:
        access_token: GitHub OAuth access token

    Returns:
        User profile dict from GitHub API

    API Docs:
        https://docs.github.com/en/rest/users/users#get-the-authenticated-user

    Response includes:
        - id: Unique GitHub ID
        - login: Username
        - name: Display name
        - email: Email (if public or authorized)
        - avatar_url: Profile picture
        - bio: Biography
        - company: Company
        - location: Location
        - followers/following: Counts
        - public_repos: Repository count
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
                # API version header (recommended)
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

        # Raise exception for HTTP errors
        response.raise_for_status()

        return response.json()


async def get_user_emails(access_token: str) -> list[dict[str, Any]]:
    """
    Fetch user's email addresses.

    Users may have multiple emails. This endpoint returns all of them
    if the 'user:email' scope was granted.

    Args:
        access_token: GitHub OAuth access token

    Returns:
        List of email dicts with 'email', 'primary', 'verified' fields

    Useful when:
        User has private email but we need to contact them.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/user/emails",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

        response.raise_for_status()

        return response.json()


def check_rate_limit_headers(headers: dict) -> dict[str, int]:
    """
    Extract rate limit information from response headers.

    GitHub includes these headers in every API response.
    Useful for monitoring and debugging.

    Headers:
        - X-RateLimit-Limit: Max requests per hour
        - X-RateLimit-Remaining: Requests left
        - X-RateLimit-Reset: Unix timestamp when limit resets
        - X-RateLimit-Used: Requests used this hour

    Returns:
        Dict with rate limit info
    """
    return {
        "limit": int(headers.get("X-RateLimit-Limit", 5000)),
        "remaining": int(headers.get("X-RateLimit-Remaining", 5000)),
        "reset": int(headers.get("X-RateLimit-Reset", 0)),
        "used": int(headers.get("X-RateLimit-Used", 0)),
    }
