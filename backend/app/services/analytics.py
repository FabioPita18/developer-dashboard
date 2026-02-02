"""
Analytics Service - Data Processing for Dashboard.

This service processes raw GitHub data into analytics formats:
- User statistics (aggregated from all repos)
- Contribution timeline (from events)
- Language breakdown (from all repos)
- Repository rankings (sorted by stars)
- Activity heatmap (by day/hour)

Data Flow:
    1. Fetch raw data from GitHub API
    2. Process/aggregate the data
    3. Cache the results
    4. Return formatted response

All methods use caching to minimize API calls.
"""
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.analytics import (
    ContributionPoint,
    HeatmapPoint,
    LanguageBreakdown,
    Repository,
    UserStats,
)
from app.services import cache, github

# GitHub language colors for charts
# Source: https://github.com/ozh/github-colors
LANGUAGE_COLORS: dict[str, str] = {
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "Java": "#b07219",
    "Go": "#00ADD8",
    "Rust": "#dea584",
    "Ruby": "#701516",
    "PHP": "#4F5D95",
    "C#": "#178600",
    "C++": "#f34b7d",
    "C": "#555555",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Shell": "#89e051",
    "Swift": "#F05138",
    "Kotlin": "#A97BFF",
    "Scala": "#c22d40",
    "Vue": "#41b883",
    "Dart": "#00B4AB",
    "Jupyter Notebook": "#DA5B0B",
}

DEFAULT_LANGUAGE_COLOR = "#8b8b8b"


async def get_user_stats(
    db: AsyncSession,
    user: User,
) -> UserStats:
    """
    Get aggregated statistics for a user.

    Calculates totals across all repositories:
    - Total stars received
    - Total forks
    - Number of public repos
    - Number of private repos
    - Estimated total commits

    Args:
        db: Database session
        user: User model instance

    Returns:
        UserStats with aggregated data
    """
    cache_key = "user_stats"

    # Try cache first
    cached = await cache.get_cached(db, user.id, cache_key)
    if cached:
        return UserStats(**cached)

    # Fetch fresh data
    repos = await github.get_all_repos(user.access_token)

    # Calculate aggregates
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    total_forks = sum(r.get("forks_count", 0) for r in repos)
    public_repos = sum(1 for r in repos if not r.get("private", False))
    private_repos = sum(1 for r in repos if r.get("private", False))

    # Estimate commits from events (rough approximation)
    events = await github.get_all_events(user.access_token, user.username)
    total_commits = sum(
        len(e.get("payload", {}).get("commits", []))
        for e in events
        if e.get("type") == "PushEvent"
    )

    stats = UserStats(
        total_stars=total_stars,
        total_forks=total_forks,
        public_repos=public_repos,
        private_repos=private_repos,
        total_commits=total_commits,
    )

    # Cache the result
    await cache.set_cached(db, user.id, cache_key, stats.model_dump())

    return stats


async def get_contribution_timeline(
    db: AsyncSession,
    user: User,
    days: int = 30,
) -> list[ContributionPoint]:
    """
    Get contribution timeline for the past N days.

    Processes user events to count daily contributions:
    - Commits (from PushEvent)
    - Pull Requests (from PullRequestEvent with action=opened)
    - Issues (from IssuesEvent with action=opened)

    Args:
        db: Database session
        user: User model instance
        days: Number of days to include

    Returns:
        List of ContributionPoints, one per day
    """
    cache_key = f"contributions_{days}"

    # Try cache
    cached = await cache.get_cached(db, user.id, cache_key)
    if cached:
        return [ContributionPoint(**p) for p in cached]

    # Fetch events
    events = await github.get_all_events(user.access_token, user.username)

    # Initialize daily buckets
    # Use timezone-aware cutoff since GitHub event timestamps include timezone info
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    daily_data: dict[str, dict[str, int]] = defaultdict(
        lambda: {"commits": 0, "pull_requests": 0, "issues": 0}
    )

    for event in events:
        # Parse event timestamp
        created_at_str = event.get("created_at", "")
        try:
            created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
        except ValueError:
            continue

        # Skip events outside our window
        if created_at < cutoff:
            continue

        date_key = created_at.strftime("%Y-%m-%d")
        event_type = event.get("type", "")
        payload = event.get("payload", {})

        if event_type == "PushEvent":
            # Count commits in this push
            commits = len(payload.get("commits", []))
            daily_data[date_key]["commits"] += commits

        elif event_type == "PullRequestEvent":
            if payload.get("action") == "opened":
                daily_data[date_key]["pull_requests"] += 1

        elif event_type == "IssuesEvent":
            if payload.get("action") == "opened":
                daily_data[date_key]["issues"] += 1

    # Convert to list of ContributionPoints
    # Include all days in range, even if zero activity
    result = []
    current = datetime.utcnow()

    for i in range(days):
        date = current - timedelta(days=i)
        date_key = date.strftime("%Y-%m-%d")
        data = daily_data.get(date_key, {"commits": 0, "pull_requests": 0, "issues": 0})

        result.append(ContributionPoint(
            date=date_key,
            commits=data["commits"],
            pull_requests=data["pull_requests"],
            issues=data["issues"],
        ))

    # Sort by date ascending
    result.sort(key=lambda x: x.date)

    # Cache
    await cache.set_cached(
        db, user.id, cache_key,
        [p.model_dump() for p in result]
    )

    return result


async def get_language_breakdown(
    db: AsyncSession,
    user: User,
) -> list[LanguageBreakdown]:
    """
    Get language breakdown across all repositories.

    Aggregates bytes of code per language from all repos,
    calculates percentages, and assigns colors for charts.

    Args:
        db: Database session
        user: User model instance

    Returns:
        List of LanguageBreakdown, sorted by percentage descending
    """
    cache_key = "languages"

    # Try cache
    cached = await cache.get_cached(db, user.id, cache_key)
    if cached:
        return [LanguageBreakdown(**lang) for lang in cached]

    # Fetch all repos
    repos = await github.get_all_repos(user.access_token)

    # Aggregate languages
    language_bytes: dict[str, int] = defaultdict(int)

    for repo in repos:
        # Skip forks (don't count code we didn't write)
        if repo.get("fork", False):
            continue

        # Get languages for this repo
        owner = repo.get("owner", {}).get("login", "")
        repo_name = repo.get("name", "")

        if not owner or not repo_name:
            continue

        try:
            repo_languages = await github.get_repo_languages(
                user.access_token, owner, repo_name
            )
            for lang, bytes_count in repo_languages.items():
                language_bytes[lang] += bytes_count
        except Exception:
            # Skip repos we can't access
            continue

    # Calculate total and percentages
    total_bytes = sum(language_bytes.values())

    if total_bytes == 0:
        return []

    result = []
    for lang, bytes_count in language_bytes.items():
        percentage = (bytes_count / total_bytes) * 100
        color = LANGUAGE_COLORS.get(lang, DEFAULT_LANGUAGE_COLOR)

        result.append(LanguageBreakdown(
            language=lang,
            bytes=bytes_count,
            percentage=round(percentage, 2),
            color=color,
        ))

    # Sort by percentage descending, take top 10
    result.sort(key=lambda x: x.percentage, reverse=True)
    result = result[:10]

    # Cache
    await cache.set_cached(
        db, user.id, cache_key,
        [lang.model_dump() for lang in result]
    )

    return result


async def get_top_repositories(
    db: AsyncSession,
    user: User,
    limit: int = 10,
) -> list[Repository]:
    """
    Get user's top repositories sorted by stars.

    Args:
        db: Database session
        user: User model instance
        limit: Maximum number of repos to return

    Returns:
        List of Repository objects
    """
    cache_key = f"repositories_{limit}"

    # Try cache
    cached = await cache.get_cached(db, user.id, cache_key)
    if cached:
        return [Repository(**r) for r in cached]

    # Fetch repos
    repos = await github.get_all_repos(user.access_token)

    # Sort by stars
    repos.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)

    # Convert to Repository objects
    # Note: Repository schema uses 'stars', 'forks', 'is_private' field names
    result = []
    for repo in repos[:limit]:
        result.append(Repository(
            name=repo.get("name", ""),
            full_name=repo.get("full_name", ""),
            description=repo.get("description"),
            html_url=repo.get("html_url", ""),
            language=repo.get("language"),
            stars=repo.get("stargazers_count", 0),
            forks=repo.get("forks_count", 0),
            is_private=repo.get("private", False),
            updated_at=repo.get("updated_at", ""),
        ))

    # Cache
    await cache.set_cached(
        db, user.id, cache_key,
        [r.model_dump() for r in result]
    )

    return result


async def get_activity_heatmap(
    db: AsyncSession,
    user: User,
) -> list[HeatmapPoint]:
    """
    Get activity heatmap data (day x hour matrix).

    Counts events by day of week and hour of day
    to show when the user is most active.

    Args:
        db: Database session
        user: User model instance

    Returns:
        List of HeatmapPoints (day 0-6, hour 0-23)
    """
    cache_key = "heatmap"

    # Try cache
    cached = await cache.get_cached(db, user.id, cache_key)
    if cached:
        return [HeatmapPoint(**p) for p in cached]

    # Fetch events
    events = await github.get_all_events(user.access_token, user.username)

    # Count by day/hour
    # Using a dict with (day, hour) tuple as key
    counts: dict[tuple[int, int], int] = defaultdict(int)

    for event in events:
        created_at_str = event.get("created_at", "")
        try:
            created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
        except ValueError:
            continue

        day = created_at.weekday()  # Monday=0, Sunday=6
        # Convert to Sunday=0 format for consistency with JS
        day = (day + 1) % 7

        hour = created_at.hour
        counts[(day, hour)] += 1

    # Convert to list of HeatmapPoints
    # Include all day/hour combinations (even zeros)
    result = []
    for day in range(7):
        for hour in range(24):
            count = counts.get((day, hour), 0)
            result.append(HeatmapPoint(
                day=day,
                hour=hour,
                count=count,
            ))

    # Cache
    await cache.set_cached(
        db, user.id, cache_key,
        [p.model_dump() for p in result]
    )

    return result
