"""
Analytics Pydantic Schemas.

These schemas define the structure of analytics API responses.
They should match exactly with the TypeScript types in the frontend.

Each schema represents a specific type of analytics data:
- UserStats: Aggregate statistics
- ContributionPoint: Timeline data points
- LanguageBreakdown: Language statistics
- Repository: Repository information
- HeatmapPoint: Activity heatmap data
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserStats(BaseModel):
    """
    Aggregated user statistics across all repositories.

    Calculated by summing stats from all user repositories.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_stars": 1234,
                "total_forks": 567,
                "public_repos": 42,
                "private_repos": 8,
                "total_commits": 2500,
            }
        },
    )

    total_stars: int = Field(
        ...,
        ge=0,
        description="Total stars across all repositories",
    )
    total_forks: int = Field(
        ...,
        ge=0,
        description="Total forks across all repositories",
    )
    public_repos: int = Field(
        ...,
        ge=0,
        description="Number of public repositories",
    )
    private_repos: int = Field(
        ...,
        ge=0,
        description="Number of private repositories",
    )
    total_commits: int = Field(
        default=0,
        ge=0,
        description="Estimated total commits (from events)",
    )


class ContributionPoint(BaseModel):
    """
    Single data point on the contribution timeline.

    Represents activity for a single day.
    Used to build line charts showing contribution trends.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2024-01-15",
                "commits": 5,
                "pull_requests": 2,
                "issues": 1,
            }
        },
    )

    date: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Date in ISO format (YYYY-MM-DD)",
        examples=["2024-01-15"],
    )
    commits: int = Field(
        default=0,
        ge=0,
        description="Number of commits on this day",
    )
    pull_requests: int = Field(
        default=0,
        ge=0,
        description="Number of pull requests on this day",
    )
    issues: int = Field(
        default=0,
        ge=0,
        description="Number of issues opened on this day",
    )


class LanguageBreakdown(BaseModel):
    """
    Language statistics for pie/donut charts.

    Represents a single language's contribution to the codebase.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "language": "Python",
                "bytes": 150000,
                "percentage": 45.5,
                "color": "#3572A5",
            }
        },
    )

    language: str = Field(
        ...,
        min_length=1,
        description="Programming language name",
    )
    bytes: int = Field(
        ...,
        ge=0,
        description="Total bytes of code in this language",
    )
    percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of total code (0-100)",
    )
    color: str = Field(
        ...,
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="Hex color code for charts",
        examples=["#3572A5"],
    )


class Repository(BaseModel):
    """
    Repository information for display.

    Contains the key information about a repository
    for showing in lists and cards.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "hello-world",
                "full_name": "octocat/hello-world",
                "description": "My first repository on GitHub!",
                "html_url": "https://github.com/octocat/hello-world",
                "language": "Python",
                "stars": 100,
                "forks": 25,
                "is_private": False,
                "updated_at": "2024-01-15T10:30:00Z",
            }
        },
    )

    name: str = Field(
        ...,
        description="Repository name",
    )
    full_name: str = Field(
        ...,
        description="Full name in owner/repo format",
    )
    description: Optional[str] = Field(
        default=None,
        description="Repository description",
    )
    html_url: str = Field(
        ...,
        description="GitHub URL for the repository",
    )
    language: Optional[str] = Field(
        default=None,
        description="Primary programming language",
    )
    stars: int = Field(
        ...,
        ge=0,
        description="Number of stars",
    )
    forks: int = Field(
        ...,
        ge=0,
        description="Number of forks",
    )
    is_private: bool = Field(
        default=False,
        description="Whether repository is private",
    )
    updated_at: str = Field(
        ...,
        description="Last updated timestamp (ISO format)",
    )


class HeatmapPoint(BaseModel):
    """
    Activity heatmap data point.

    Represents activity count for a specific day-hour combination.
    Used to create GitHub-style contribution heatmaps.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "day": 1,
                "hour": 14,
                "count": 5,
            }
        },
    )

    day: int = Field(
        ...,
        ge=0,
        le=6,
        description="Day of week (0=Sunday, 6=Saturday)",
    )
    hour: int = Field(
        ...,
        ge=0,
        le=23,
        description="Hour of day (0-23)",
    )
    count: int = Field(
        ...,
        ge=0,
        description="Number of activities",
    )
