"""
FastAPI Application Factory.

This module creates and configures the FastAPI application.
We'll expand this in Phase 2 with full configuration.

Learning Notes:
- FastAPI is a modern Python web framework based on Starlette
- It uses Python type hints for automatic validation and documentation
- CORS middleware is needed for cross-origin requests from the frontend
- The app object is the main entry point for the ASGI server (Uvicorn)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Application metadata
# These values appear in the auto-generated API documentation
app = FastAPI(
    title="Developer Dashboard API",
    description="Backend API for GitHub analytics dashboard",
    version="0.1.0",
    docs_url="/docs",      # Swagger UI endpoint
    redoc_url="/redoc",    # ReDoc endpoint (alternative docs)
)

# CORS configuration
# CORS (Cross-Origin Resource Sharing) controls which origins can access the API
# In Phase 2, we'll load this from environment variables
app.add_middleware(
    CORSMiddleware,
    # Origins that can access the API (the frontend URL)
    allow_origins=["http://localhost:3000"],
    # Allow cookies to be sent with requests (needed for JWT in HTTP-only cookies)
    allow_credentials=True,
    # HTTP methods allowed
    allow_methods=["*"],
    # HTTP headers allowed
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Used by Docker and load balancers to verify the service is running.
    Returns a simple JSON response.

    Returns:
        dict: Status information including version
    """
    return {"status": "healthy", "version": "0.1.0"}


@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint.

    Provides basic API information and links to documentation.

    Returns:
        dict: API information with documentation links
    """
    return {
        "message": "Developer Dashboard API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }
