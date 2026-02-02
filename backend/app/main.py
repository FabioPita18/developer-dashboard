"""
FastAPI Application Factory.

This module creates and configures the FastAPI application.

Application setup includes:
- CORS middleware for frontend access
- Router registration
- Lifespan events (startup/shutdown)
- Health check endpoint
- OpenAPI documentation configuration
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers.analytics import router as analytics_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.

    Code before 'yield' runs on startup.
    Code after 'yield' runs on shutdown.

    Use this for:
    - Database connection setup/teardown
    - Background task initialization
    - Cache warming
    - Cleanup operations
    """
    # Startup
    print(f"Starting {settings.app_name}...")
    print(f"Environment: {settings.environment}")
    print(f"Debug mode: {settings.debug}")

    yield  # Application runs here

    # Shutdown
    print("Shutting down...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Backend API for Developer Dashboard - "
                "GitHub analytics and visualization.",
    version="0.1.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# =============================================================================
# CORS Middleware
# =============================================================================
# CORS (Cross-Origin Resource Sharing) controls which origins can access our API.
# This is essential for the frontend to communicate with the backend.

app.add_middleware(
    CORSMiddleware,
    # Allow requests from frontend URL
    allow_origins=[settings.frontend_url],
    # Allow cookies/credentials (needed for HTTP-only JWT cookie)
    allow_credentials=True,
    # Allow all HTTP methods
    allow_methods=["*"],
    # Allow all headers
    allow_headers=["*"],
    # Cache preflight requests for 1 hour
    max_age=3600,
)

# =============================================================================
# Include Routers
# =============================================================================

# Authentication routes
app.include_router(auth_router)

# User profile routes
app.include_router(users_router)

# Analytics data routes
app.include_router(analytics_router)


# =============================================================================
# Root Endpoints
# =============================================================================

@app.get(
    "/",
    summary="API Information",
    description="Returns basic information about the API.",
    tags=["General"],
)
async def root() -> dict[str, str]:
    """
    Root endpoint with API information.

    Provides links to documentation and health check.
    """
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
    }


@app.get(
    "/health",
    summary="Health Check",
    description="Returns the health status of the API.",
    tags=["General"],
)
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Used by:
    - Docker health checks
    - Load balancers
    - Kubernetes readiness probes
    - Monitoring systems

    Returns simple healthy status if API is running.
    Could be extended to check database, cache, etc.
    """
    return {
        "status": "healthy",
        "environment": settings.environment,
    }
