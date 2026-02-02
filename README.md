# Developer Dashboard

> Full-stack GitHub analytics dashboard — visualize contributions, languages, and coding patterns.

[![Backend CI](https://github.com/FabioPita18/developer-dashboard/actions/workflows/backend.yml/badge.svg)](https://github.com/FabioPita18/developer-dashboard/actions/workflows/backend.yml)
[![Frontend CI](https://github.com/FabioPita18/developer-dashboard/actions/workflows/frontend.yml/badge.svg)](https://github.com/FabioPita18/developer-dashboard/actions/workflows/frontend.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB?logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind](https://img.shields.io/badge/Tailwind-3.4-06B6D4?logo=tailwindcss)](https://tailwindcss.com/)

## Overview

A modern analytics dashboard that connects to the GitHub API via OAuth and presents developers with interactive visualizations of their activity. Built as a portfolio project demonstrating a production-grade full-stack architecture with async Python, strict TypeScript, and automated CI/CD.

### Features

- **GitHub OAuth** — secure login, JWT sessions stored in HTTP-only cookies
- **Contribution Timeline** — daily commit, PR, and issue counts powered by the GitHub Search Commits API
- **Language Breakdown** — aggregated bytes-of-code across all repositories, displayed as a donut chart
- **Top Repositories** — ranked by stars with language tags and visibility badges
- **Activity Heatmap** — day-of-week / hour-of-day matrix showing when you code most
- **Smart Caching** — PostgreSQL-backed 24-hour cache to minimize GitHub API usage
- **Dark Mode** — toggle with system-preference detection and localStorage persistence
- **Responsive Design** — mobile-first layout with Tailwind CSS

## Tech Stack

### Backend

| Package | Version | Role |
|---------|---------|------|
| Python | 3.11+ | Runtime |
| FastAPI | 0.128.0 | Web framework |
| Uvicorn | 0.27.0 | ASGI server |
| SQLAlchemy | 2.0.25 | Async ORM (2.0 `Mapped[]` syntax) |
| asyncpg | 0.29.0 | PostgreSQL async driver |
| Pydantic | 2.12.5 | Validation (`ConfigDict`, not `class Config`) |
| pydantic-settings | 2.1.0 | Environment configuration |
| Alembic | 1.13.1 | Database migrations |
| httpx | 0.26.0 | Async HTTP client |
| python-jose | 3.4.0 | JWT encoding/decoding |

### Frontend

| Package | Version | Role |
|---------|---------|------|
| Node.js | 22.x LTS | Runtime |
| React | 18.2.0 | UI framework |
| TypeScript | 5.3.3 | Strict mode, no `any` |
| Vite | 5.0.12 | Build tool |
| Tailwind CSS | 3.4.1 | Styling (dark mode: `class` strategy) |
| TanStack Query | 5.17.9 | Server state & caching |
| React Router | 6.21.3 | Client-side routing |
| Recharts | 2.10.4 | Charts |
| Axios | 1.6.5 | HTTP client |

### Infrastructure

| Component | Port | Notes |
|-----------|------|-------|
| PostgreSQL 16 | 5434 (host) / 5432 (container) | Persistent volume |
| Backend | 8000 | FastAPI + Uvicorn |
| Frontend | 3000 | Vite dev server |

### CI/CD

- **GitHub Actions** — separate workflows for backend (`lint`, `test`, `security`, `docker`) and frontend (`lint`, `typecheck`, `test`, `build`, `audit`)
- **Backend quality**: Black, isort, Flake8, mypy, pytest + coverage, pip-audit
- **Frontend quality**: ESLint, TypeScript strict check, Vitest + coverage, npm audit

## Project Structure

```
developer-dashboard/
├── .github/workflows/
│   ├── backend.yml            # Backend CI pipeline
│   ├── frontend.yml           # Frontend CI pipeline
│   └── pr-checks.yml          # Combined PR validation
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app factory, middleware, CORS
│   │   ├── config.py          # Pydantic Settings (env vars)
│   │   ├── database.py        # Async SQLAlchemy engine & sessions
│   │   ├── dependencies.py    # FastAPI DI (get_db, get_current_user)
│   │   ├── models/
│   │   │   ├── user.py        # User model (SQLAlchemy 2.0)
│   │   │   └── cache.py       # CachedData model (JSON column)
│   │   ├── schemas/
│   │   │   ├── user.py        # User request/response schemas
│   │   │   └── analytics.py   # Analytics response schemas
│   │   ├── routers/
│   │   │   ├── auth.py        # OAuth login, callback, logout, status
│   │   │   ├── users.py       # Profile, cache refresh
│   │   │   └── analytics.py   # Stats, contributions, languages, repos, heatmap
│   │   └── services/
│   │       ├── github.py      # GitHub API client (paginated, async)
│   │       ├── cache.py       # PostgreSQL caching layer
│   │       ├── analytics.py   # Data aggregation & processing
│   │       └── security.py    # JWT creation & verification
│   ├── tests/
│   │   ├── conftest.py        # Fixtures (in-memory SQLite, mock data)
│   │   ├── test_auth.py       # 9 tests — OAuth flow, JWT, logout
│   │   ├── test_analytics.py  # 9 tests — all analytics endpoints
│   │   ├── test_cache.py      # 6 tests — set/get, expiry, upsert
│   │   └── test_users.py      # 4 tests — profile, refresh
│   ├── alembic/               # Database migrations
│   ├── requirements.txt       # Production dependencies
│   ├── requirements-dev.txt   # Dev/test dependencies
│   ├── Dockerfile
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/        # Card, Loader, ErrorMessage, ProtectedRoute
│   │   │   ├── layout/        # Navigation, DashboardLayout
│   │   │   ├── dashboard/     # ProfileHeader, StatsCard, RepoCard
│   │   │   └── charts/        # ContributionChart, LanguageChart, HeatmapChart
│   │   ├── pages/             # Login, Callback, Dashboard, NotFound
│   │   ├── services/          # api.ts, authService.ts, analyticsService.ts
│   │   ├── hooks/             # useAnalytics.ts, useDarkMode.ts
│   │   ├── contexts/          # AuthContext.tsx
│   │   ├── types/             # TypeScript interfaces (mirrors backend schemas)
│   │   ├── App.tsx            # Root component with routing
│   │   ├── main.tsx           # Entry point
│   │   └── index.css          # Tailwind directives & global styles
│   ├── tests/
│   │   ├── setup.ts           # Vitest setup
│   │   ├── utils.tsx          # Test render helper (QueryClient + Router)
│   │   ├── components/        # StatsCard, RepoCard, Loader tests
│   │   └── hooks/             # useDarkMode tests
│   ├── package.json
│   ├── vite.config.ts
│   ├── vitest.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── .eslintrc.cjs
│   └── Dockerfile
├── docker-compose.yml         # PostgreSQL + backend + frontend
├── .env.example               # Environment variable template
├── LICENSE
└── README.md
```

## API Endpoints

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/auth/github` | No | Redirect to GitHub OAuth |
| GET | `/api/auth/callback` | No | Handle OAuth callback, set JWT cookie |
| POST | `/api/auth/logout` | No | Clear authentication cookie |
| GET | `/api/auth/status` | Optional | Check if authenticated, return user |

### Users

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/users/me` | Required | Get current user profile |
| POST | `/api/users/me/refresh` | Required | Clear cache and refresh data |

### Analytics

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/analytics/stats` | Required | Aggregated stats (stars, forks, commits) |
| GET | `/api/analytics/contributions?days=30` | Required | Daily contribution timeline (1-90 days) |
| GET | `/api/analytics/languages` | Required | Language breakdown across all repos |
| GET | `/api/analytics/repositories?limit=10` | Required | Top repositories by stars |
| GET | `/api/analytics/heatmap` | Required | Activity by day-of-week and hour (168 points) |

Interactive API docs available at `http://localhost:8000/docs` when running locally.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 22.x LTS
- PostgreSQL 16+ (or Docker)
- A GitHub OAuth App ([create one here](https://github.com/settings/developers))
  - **Homepage URL**: `http://localhost:3000`
  - **Callback URL**: `http://localhost:8000/api/auth/callback`

### Option 1: Docker (recommended)

```bash
# Clone and enter the project
git clone https://github.com/FabioPita18/developer-dashboard.git
cd developer-dashboard

# Copy and fill in environment variables
cp .env.example .env
# Edit .env with your GitHub OAuth credentials and a JWT secret

# Start all services
docker-compose up -d --build

# Run database migrations
docker-compose exec backend alembic upgrade head
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials and database URL

# Run migrations and start server
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## Running Tests

**Backend** (29 tests):

```bash
cd backend
pytest -v                                          # Run all tests
pytest --cov=app --cov-report=html                 # With coverage report
```

**Frontend** (20 tests):

```bash
cd frontend
npm test                                           # Watch mode
npm run test:coverage                              # With coverage report
```

**Linting:**

```bash
# Backend
black --check app tests && isort --check-only app tests && flake8 app tests && mypy app

# Frontend
npm run lint && npm run typecheck
```

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection (must use `+asyncpg`) | `postgresql+asyncpg://user:pass@localhost:5432/devdash` |
| `GITHUB_CLIENT_ID` | OAuth App client ID | `Iv1.abc123` |
| `GITHUB_CLIENT_SECRET` | OAuth App client secret | `secret_abc123` |
| `GITHUB_REDIRECT_URI` | OAuth callback URL | `http://localhost:8000/api/auth/callback` |
| `GITHUB_SCOPES` | Permissions to request | `read:user user:email repo` |
| `JWT_SECRET_KEY` | Secret for signing tokens | Generate with `openssl rand -hex 32` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token lifetime | `30` |
| `FRONTEND_URL` | Frontend origin for CORS | `http://localhost:3000` |
| `CACHE_TTL_SECONDS` | Cache lifetime | `86400` (24 hours) |

## Security

- JWT tokens stored in **HTTP-only cookies** (not localStorage) to prevent XSS
- **SameSite=Lax** cookie flag for CSRF protection
- **Secure** flag enabled in production (HTTPS only)
- GitHub access tokens are never exposed in API responses
- All inputs validated with Pydantic v2
- SQL injection prevented by SQLAlchemy parameterized queries
- CORS restricted to the configured frontend origin
- Dependencies audited via pip-audit and npm audit in CI

## GitHub API Rate Limits

- **Authenticated requests**: 5,000/hour
- **Search API**: 30/minute
- The 24-hour cache ensures normal dashboard usage stays well under these limits
- Rate limit headers are monitored on every API response

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
