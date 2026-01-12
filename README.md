# Developer Dashboard

> GitHub analytics and contribution visualization dashboard with real-time data insights

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://developer-dashboard.vercel.app)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB?logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind](https://img.shields.io/badge/Tailwind-3.4-06B6D4?logo=tailwindcss)](https://tailwindcss.com/)
[![Tests](https://img.shields.io/badge/tests-passing-success)](https://github.com/yourusername/developer-dashboard/actions)

## 📋 Overview

A modern, full-stack analytics dashboard that visualizes GitHub activity, contribution patterns, and repository statistics. Built with FastAPI and React, it provides developers with actionable insights into their coding habits, most-used languages, and contribution trends over time.

## 🎯 Problem Statement

Developers need a comprehensive way to:
- Visualize their GitHub contributions and activity patterns
- Track their most-used programming languages
- Analyze repository performance (stars, forks, activity)
- Identify their most productive coding times and days
- Share their developer metrics with potential employers

GitHub provides raw data, but lacks beautiful, customizable visualization tools that developers can showcase in their portfolios.

## ✨ Solution

An interactive dashboard featuring:
- **GitHub OAuth Integration**: Secure authentication with GitHub
- **Contribution Analytics**: Detailed graphs of commits, PRs, and issues over time
- **Language Breakdown**: Visual representation of programming languages used
- **Repository Insights**: Top repositories by stars, forks, and recent activity
- **Activity Heatmap**: Discover your most productive coding times
- **Responsive Design**: Beautiful UI that works on all devices
- **Smart Caching**: Fast load times with PostgreSQL-backed data caching

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15 (data caching)
- **Authentication**: GitHub OAuth
- **HTTP Client**: httpx (async GitHub API calls)
- **Background Tasks**: FastAPI BackgroundTasks
- **Testing**: pytest with pytest-asyncio
- **Deployment**: Railway

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS 3.4
- **Charts**: Recharts
- **Routing**: React Router v6
- **State Management**: React Context API + TanStack Query
- **HTTP Client**: Axios
- **Deployment**: Vercel

### DevOps
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions (separate pipelines for frontend/backend)
- **Testing**: pytest (backend), Jest + React Testing Library (frontend)
- **Code Quality**: ESLint, Prettier, Black

## 🚀 Key Features

### Current (MVP)
- [x] GitHub OAuth authentication
- [x] User profile overview (contributions, commits, PRs, issues)
- [x] Contribution timeline graph (commits over time)
- [x] Programming languages breakdown (pie chart)
- [x] Top repositories by stars and forks
- [x] Repository activity timeline
- [x] Contribution heatmap (activity by day/hour)
- [x] Smart data caching (24-hour refresh)
- [x] Responsive design (mobile, tablet, desktop)
- [x] Dark mode support
- [x] Loading states and error handling

### Future Enhancements
- [ ] Compare profiles with other developers
- [ ] Weekly/monthly activity email reports
- [ ] Export data to PDF
- [ ] Integration with GitLab and Bitbucket
- [ ] Organization analytics
- [ ] Custom date range selection
- [ ] Social sharing (Twitter/LinkedIn cards)

## 📸 Screenshots

### Dashboard Overview
![Dashboard](docs/screenshots/dashboard.png)

### Contribution Timeline
![Contributions](docs/screenshots/contributions.png)

### Language Breakdown
![Languages](docs/screenshots/languages.png)

### Activity Heatmap
![Heatmap](docs/screenshots/heatmap.png)

## 📡 API Endpoints

### Authentication
```
GET    /api/auth/github/          # Initiate GitHub OAuth flow
GET    /api/auth/callback/        # OAuth callback handler
POST   /api/auth/logout/          # Logout user
```

### User Data
```
GET    /api/users/me/             # Get current user profile
GET    /api/users/me/stats/       # Get user statistics summary
GET    /api/users/me/refresh/     # Force refresh cached data
```

### Analytics
```
GET    /api/analytics/contributions/     # Contribution timeline data
GET    /api/analytics/languages/         # Language breakdown
GET    /api/analytics/repositories/      # Repository statistics
GET    /api/analytics/heatmap/           # Activity heatmap data
```

## 💻 Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker (optional)
- GitHub OAuth App (create at https://github.com/settings/developers)

### GitHub OAuth Setup

1. Go to GitHub Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Fill in:
   - **Application name**: Developer Dashboard (Local)
   - **Homepage URL**: http://localhost:5173
   - **Authorization callback URL**: http://localhost:8000/api/auth/callback
4. Save the Client ID and Client Secret

### Backend Setup
```bash
# Clone repository
git clone https://github.com/yourusername/developer-dashboard.git
cd developer-dashboard

# Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your GitHub OAuth credentials and database URL

# Run database migrations
alembic upgrade head

# Run development server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`  
API docs at `http://localhost:8000/docs`

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your backend API URL

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

### Docker Setup (Recommended)
```bash
# From project root
docker-compose up --build

# Run migrations
docker-compose exec backend alembic upgrade head

# View logs
docker-compose logs -f
```

Access:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🧪 Running Tests

### Backend Tests
```bash
cd backend
pytest --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

### E2E Tests
```bash
npm run test:e2e
```

## 🔐 Environment Variables

### Backend (.env)
```bash
# Application
APP_NAME=Developer Dashboard
DEBUG=True
API_VERSION=v1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/devdash_db

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_REDIRECT_URI=http://localhost:8000/api/auth/callback

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS
CORS_ORIGINS=http://localhost:5173,https://developer-dashboard.vercel.app

# Caching
CACHE_TTL=86400  # 24 hours in seconds
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000/api
VITE_GITHUB_CLIENT_ID=your-github-client-id
```

## 📦 Deployment

### Backend (Railway)

1. **Create Railway project and add PostgreSQL**
```bash
   railway init
   railway add postgresql
```

2. **Set environment variables** in Railway dashboard
   - Add all backend environment variables
   - Update `GITHUB_REDIRECT_URI` to production URL
   - Update `CORS_ORIGINS` to include production frontend URL

3. **Deploy**
```bash
   railway up
```

### Frontend (Vercel)

1. **Connect repository to Vercel**
2. **Configure build settings**:
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`
3. **Set environment variables**:
   - `VITE_API_URL`: Your Railway backend URL
   - `VITE_GITHUB_CLIENT_ID`: Your GitHub OAuth Client ID
4. Deploy automatically on push to `main`

### Update GitHub OAuth Settings

After deployment, update your GitHub OAuth App:
- **Homepage URL**: https://developer-dashboard.vercel.app
- **Authorization callback URL**: https://your-backend.railway.app/api/auth/callback

## 📁 Project Structure
```
developer-dashboard/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # Database connection
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   └── cache.py
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── user.py
│   │   │   └── analytics.py
│   │   ├── routers/           # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── analytics.py
│   │   ├── services/          # Business logic
│   │   │   ├── github.py      # GitHub API client
│   │   │   ├── cache.py       # Caching logic
│   │   │   └── analytics.py   # Analytics processing
│   │   └── utils/             # Helper functions
│   ├── tests/
│   ├── alembic/               # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── charts/        # Chart components
│   │   │   │   ├── ContributionChart.tsx
│   │   │   │   ├── LanguageChart.tsx
│   │   │   │   └── HeatmapChart.tsx
│   │   │   ├── dashboard/     # Dashboard components
│   │   │   │   ├── StatsCard.tsx
│   │   │   │   ├── RepoCard.tsx
│   │   │   │   └── ProfileHeader.tsx
│   │   │   ├── layout/        # Layout components
│   │   │   │   ├── Navigation.tsx
│   │   │   │   └── Footer.tsx
│   │   │   └── common/        # Reusable components
│   │   ├── pages/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── DashboardPage.tsx
│   │   │   └── NotFoundPage.tsx
│   │   ├── services/          # API services
│   │   │   └── api.ts
│   │   ├── contexts/          # React contexts
│   │   │   └── AuthContext.tsx
│   │   ├── hooks/             # Custom hooks
│   │   │   └── useAuth.ts
│   │   ├── types/             # TypeScript types
│   │   │   └── index.ts
│   │   ├── utils/             # Utility functions
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🎨 Key Technical Highlights

### GitHub API Integration
```python
# backend/app/services/github.py
class GitHubService:
    async def get_user_stats(self, access_token: str):
        """Fetch comprehensive user statistics from GitHub API"""
        async with httpx.AsyncClient() as client:
            # User profile
            profile = await self._get_profile(client, access_token)
            # Repositories
            repos = await self._get_repos(client, access_token)
            # Contributions
            contributions = await self._get_contributions(client, access_token)
            
        return self._aggregate_stats(profile, repos, contributions)
```

### Smart Caching Strategy
- Cache GitHub API responses for 24 hours
- Background task to refresh data automatically
- Manual refresh option for users
- Reduces API rate limit usage

### Responsive Charts
```typescript
// frontend/src/components/charts/ContributionChart.tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export function ContributionChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="commits" stroke="#3b82f6" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

## 🔒 Security Features

- GitHub OAuth for secure authentication
- JWT tokens for API authentication
- HTTP-only cookies for token storage
- CORS configuration for production
- Rate limiting on API endpoints
- SQL injection prevention (SQLAlchemy)
- XSS protection (React default escaping)

## 📊 GitHub API Rate Limits

- **Authenticated requests**: 5,000 per hour
- **Unauthenticated**: 60 per hour
- Dashboard caches data for 24 hours to minimize API usage
- Background refresh tasks respect rate limits

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Fabio [Your Last Name]**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Portfolio: [fabio-portfolio.vercel.app](https://fabio-portfolio.vercel.app)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) and [React](https://react.dev/)
- Charts powered by [Recharts](https://recharts.org/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- GitHub data via [GitHub REST API](https://docs.github.com/en/rest)
- Deployment on [Railway](https://railway.app/) and [Vercel](https://vercel.com/)

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

---

**Live Demo**: 🚀 https://developer-dashboard.vercel.app  
**API Documentation**: 📚 https://developer-dashboard-api.railway.app/docs
