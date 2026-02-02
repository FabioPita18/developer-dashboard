"""
GitHub API Service - Extended for Analytics.

This module handles all interactions with the GitHub API:
- OAuth flow (authorization URL, token exchange)
- User profile fetching
- Repository listing with pagination
- Repository language breakdown
- User events (activity feed)
- Rate limit monitoring

Pagination:
    GitHub API uses Link headers for pagination.
    Most endpoints return max 100 items per page.
    We handle pagination automatically in get_all_* methods.

Rate Limiting:
    GitHub API has rate limits:
    - 5000 requests/hour for authenticated requests
    - 60 requests/hour for unauthenticated
    We cache responses to stay well under the limit.
"""
import re
from typing import Any
from urllib.parse import urlencode

import httpx

from app.config import get_settings

settings = get_settings()

# GitHub API endpoints
GITHUB_API_BASE = "https://api.github.com"
GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"

# Default timeout for API requests (seconds)
DEFAULT_TIMEOUT = 30.0


# =============================================================================
# Internal Helpers
# =============================================================================

def _get_auth_headers(access_token: str) -> dict[str, str]:
    """
    Build authentication headers for GitHub API requests.

    Using Bearer token format as recommended by GitHub.
    The API version header pins us to a specific API version.
    """
    return {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _parse_link_header(link_header: str | None) -> dict[str, str]:
    """
    Parse GitHub's Link header for pagination.

    GitHub returns pagination info in the Link header:
    <url>; rel="next", <url>; rel="last"

    Args:
        link_header: The Link header value

    Returns:
        Dict mapping rel to URL: {"next": "url", "last": "url"}

    Example:
        Input:  '<https://api.github.com/repos?page=2>; rel="next"'
        Output: {"next": "https://api.github.com/repos?page=2"}
    """
    if not link_header:
        return {}

    links = {}
    # Pattern to match: <url>; rel="name"
    pattern = r'<([^>]+)>;\s*rel="([^"]+)"'

    for match in re.finditer(pattern, link_header):
        url, rel = match.groups()
        links[rel] = url

    return links


# =============================================================================
# OAuth Methods
# =============================================================================

def get_authorization_url() -> str:
    """
    Build the GitHub OAuth authorization URL.

    This URL is where we redirect users to authorize our app.
    After authorization, GitHub redirects back to our callback URL.

    Returns:
        Full URL to redirect user to
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
        Dict containing access_token, token_type, scope
        OR error dict if something went wrong

    Security Note:
        This exchange happens server-side. The code is single-use
        and expires quickly, preventing replay attacks.
    """
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
                "redirect_uri": settings.github_redirect_uri,
            },
            headers={"Accept": "application/json"},
        )
        return response.json()


# =============================================================================
# User Methods
# =============================================================================

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
    """
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/user",
            headers=_get_auth_headers(access_token),
        )
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
    """
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/user/emails",
            headers=_get_auth_headers(access_token),
        )
        response.raise_for_status()
        return response.json()


# =============================================================================
# Repository Methods
# =============================================================================

async def get_user_repos(
    access_token: str,
    page: int = 1,
    per_page: int = 100,
    sort: str = "updated",
    direction: str = "desc",
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    """
    Fetch user's repositories (single page).

    Args:
        access_token: GitHub OAuth token
        page: Page number (1-indexed)
        per_page: Items per page (max 100)
        sort: Sort field (created, updated, pushed, full_name)
        direction: Sort direction (asc, desc)

    Returns:
        Tuple of (repos list, pagination links)

    API Docs:
        https://docs.github.com/en/rest/repos/repos#list-repositories-for-the-authenticated-user
    """
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/user/repos",
            params={
                "page": page,
                "per_page": per_page,
                "sort": sort,
                "direction": direction,
                "visibility": "all",  # Include private repos
                "affiliation": "owner,collaborator,organization_member",
            },
            headers=_get_auth_headers(access_token),
        )
        response.raise_for_status()

        links = _parse_link_header(response.headers.get("Link"))
        return response.json(), links


async def get_all_repos(access_token: str) -> list[dict[str, Any]]:
    """
    Fetch ALL user repositories, handling pagination.

    Automatically fetches all pages until no more data.

    Args:
        access_token: GitHub OAuth token

    Returns:
        Complete list of all repositories

    Note:
        This can make multiple API calls. For users with many repos,
        consider caching the results.
    """
    all_repos: list[dict[str, Any]] = []
    page = 1
    max_pages = 50  # Safety limit to prevent infinite loops

    while page <= max_pages:
        repos, links = await get_user_repos(access_token, page=page)
        all_repos.extend(repos)

        # Check if there are more pages
        if "next" not in links or not repos:
            break

        page += 1

    return all_repos


async def get_repo_languages(
    access_token: str,
    owner: str,
    repo: str,
) -> dict[str, int]:
    """
    Get language breakdown for a repository.

    Args:
        access_token: GitHub OAuth token
        owner: Repository owner username
        repo: Repository name

    Returns:
        Dict mapping language name to bytes of code
        Example: {"Python": 50000, "JavaScript": 30000}

    API Docs:
        https://docs.github.com/en/rest/repos/repos#list-repository-languages
    """
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/languages",
            headers=_get_auth_headers(access_token),
        )
        response.raise_for_status()
        return response.json()


# =============================================================================
# Event Methods (Activity Feed)
# =============================================================================

async def get_user_events(
    access_token: str,
    username: str,
    page: int = 1,
    per_page: int = 100,
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    """
    Get user's public events (activity feed).

    Events include pushes, PRs, issues, comments, etc.
    GitHub keeps only 90 days of events, max 300 total.

    Args:
        access_token: For authentication (higher rate limits)
        username: GitHub username
        page: Page number
        per_page: Items per page (max 100)

    Returns:
        Tuple of (events list, pagination links)

    Event Types:
        - PushEvent: Commits pushed
        - PullRequestEvent: PR opened/closed/merged
        - IssuesEvent: Issue opened/closed
        - CreateEvent: Branch/tag created
        - DeleteEvent: Branch/tag deleted
        - WatchEvent: Repository starred
        - ForkEvent: Repository forked

    API Docs:
        https://docs.github.com/en/rest/activity/events#list-events-for-the-authenticated-user
    """
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/users/{username}/events",
            params={
                "page": page,
                "per_page": per_page,
            },
            headers=_get_auth_headers(access_token),
        )
        response.raise_for_status()

        links = _parse_link_header(response.headers.get("Link"))
        return response.json(), links


async def get_all_events(access_token: str, username: str) -> list[dict[str, Any]]:
    """
    Fetch all available user events.

    GitHub limits to 300 events total (3 pages of 100).

    Args:
        access_token: GitHub OAuth token
        username: GitHub username

    Returns:
        List of all available events (max 300)
    """
    all_events: list[dict[str, Any]] = []
    page = 1
    max_pages = 3  # GitHub limits to 300 events

    while page <= max_pages:
        events, links = await get_user_events(
            access_token,
            username,
            page=page,
        )
        all_events.extend(events)

        if "next" not in links or not events:
            break

        page += 1

    return all_events


# =============================================================================
# Commit Search Methods
# =============================================================================


async def search_user_commits(
    access_token: str,
    username: str,
    since: str,
    until: str,
    page: int = 1,
    per_page: int = 100,
) -> tuple[list[dict[str, Any]], int, dict[str, str]]:
    """
    Search for commits by a user within a date range.

    Uses the GitHub Search Commits API which is more reliable
    than the Events API for counting actual commits.

    The Events API has a 300-event cap and doesn't reliably
    capture all PushEvents, whereas the Search API returns
    actual commit objects.

    Args:
        access_token: GitHub OAuth token
        username: GitHub username (commit author)
        since: Start date in YYYY-MM-DD format
        until: End date in YYYY-MM-DD format
        page: Page number (1-indexed)
        per_page: Items per page (max 100)

    Returns:
        Tuple of (commit items list, total count, pagination links)

    API Docs:
        https://docs.github.com/en/rest/search/search#search-commits
    """
    query = f"author:{username} committer-date:{since}..{until}"

    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/search/commits",
            params={
                "q": query,
                "page": page,
                "per_page": per_page,
                "sort": "committer-date",
                "order": "asc",
            },
            headers=_get_auth_headers(access_token),
        )
        response.raise_for_status()

        data = response.json()
        links = _parse_link_header(response.headers.get("Link"))

        return data.get("items", []), data.get("total_count", 0), links


async def get_all_user_commits(
    access_token: str,
    username: str,
    since: str,
    until: str,
) -> list[dict[str, Any]]:
    """
    Fetch all commits by a user within a date range.

    Handles pagination automatically. GitHub Search API
    returns max 1000 results, which is sufficient for
    a 30-day contribution timeline.

    Args:
        access_token: GitHub OAuth token
        username: GitHub username
        since: Start date YYYY-MM-DD
        until: End date YYYY-MM-DD

    Returns:
        List of all commit search result items
    """
    all_commits: list[dict[str, Any]] = []
    page = 1
    max_pages = 10  # 10 pages x 100 = 1000 commits max

    while page <= max_pages:
        commits, total_count, links = await search_user_commits(
            access_token, username, since, until,
            page=page,
        )
        all_commits.extend(commits)

        if "next" not in links or not commits:
            break

        page += 1

    return all_commits


# =============================================================================
# Rate Limit Utilities
# =============================================================================

def check_rate_limit_headers(headers: dict) -> dict[str, int]:
    """
    Extract rate limit information from response headers.

    GitHub includes these headers in every API response.
    Useful for monitoring and debugging.

    Returns:
        Dict with limit, remaining, reset, used
    """
    return {
        "limit": int(headers.get("X-RateLimit-Limit", 5000)),
        "remaining": int(headers.get("X-RateLimit-Remaining", 5000)),
        "reset": int(headers.get("X-RateLimit-Reset", 0)),
        "used": int(headers.get("X-RateLimit-Used", 0)),
    }


async def get_rate_limit(access_token: str) -> dict[str, Any]:
    """
    Get current rate limit status.

    Useful for monitoring and debugging.

    API Docs:
        https://docs.github.com/en/rest/rate-limit
    """
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/rate_limit",
            headers=_get_auth_headers(access_token),
        )
        response.raise_for_status()
        return response.json()
