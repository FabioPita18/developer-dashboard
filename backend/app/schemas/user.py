"""
User Pydantic Schemas.

These schemas define the shape of user data for API requests/responses.
They provide validation and serialization.

Pydantic v2 Key Points:
- Use model_config = ConfigDict(...), NOT class Config
- Use from_attributes=True, NOT orm_mode=True
- Use model_validate() to create from ORM objects
- Use model_dump() to convert to dict

Security Note:
    UserResponse NEVER includes access_token!
    Create separate schemas for internal vs. API use.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    """
    Base user schema with common fields.

    Used as a base class for other user schemas.
    """

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
    )

    username: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="GitHub username",
        examples=["octocat"],
    )
    email: Optional[str] = Field(
        default=None,
        max_length=255,
        description="User email address (may be null if private)",
        examples=["octocat@github.com"],
    )
    name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Display name",
        examples=["The Octocat"],
    )


class UserResponse(UserBase):
    """
    User data for API responses.

    This schema is safe to expose publicly.
    NEVER includes access_token!

    Used by:
    - GET /api/users/me
    - GET /api/auth/status (when authenticated)
    """

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "github_id": 583231,
                "username": "octocat",
                "email": "octocat@github.com",
                "name": "The Octocat",
                "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                "bio": "I love coding!",
                "company": "@github",
                "location": "San Francisco",
                "blog": "https://github.blog",
                "public_repos": 8,
                "followers": 10000,
                "following": 9,
                "created_at": "2023-01-01T00:00:00Z",
                "last_login_at": "2024-01-15T10:30:00Z",
            }
        },
    )

    id: int = Field(..., description="Internal user ID")
    github_id: int = Field(..., description="GitHub user ID")
    avatar_url: Optional[str] = Field(
        default=None,
        description="GitHub avatar URL",
    )
    bio: Optional[str] = Field(
        default=None,
        description="User biography",
    )
    company: Optional[str] = Field(
        default=None,
        description="Company name",
    )
    location: Optional[str] = Field(
        default=None,
        description="User location",
    )
    blog: Optional[str] = Field(
        default=None,
        description="Blog/website URL",
    )
    public_repos: int = Field(
        default=0,
        description="Number of public repositories",
    )
    followers: int = Field(
        default=0,
        description="Number of followers",
    )
    following: int = Field(
        default=0,
        description="Number of users following",
    )
    created_at: datetime = Field(
        ...,
        description="Account creation timestamp",
    )
    last_login_at: datetime = Field(
        ...,
        description="Last login timestamp",
    )


class AuthStatus(BaseModel):
    """
    Authentication status response.

    Used by GET /api/auth/status to indicate whether
    the current request is authenticated.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "authenticated": True,
                    "user": {
                        "id": 1,
                        "username": "octocat",
                    },
                },
                {
                    "authenticated": False,
                    "user": None,
                },
            ]
        },
    )

    authenticated: bool = Field(
        ...,
        description="Whether the request is authenticated",
    )
    user: Optional[UserResponse] = Field(
        default=None,
        description="User data if authenticated, null otherwise",
    )
