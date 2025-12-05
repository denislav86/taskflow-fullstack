# TaskFlow

<div align="center">

![TaskFlow Logo](https://via.placeholder.com/120x120/22c55e/ffffff?text=✓)

**A modern, full-stack task management application**

[![CI](https://github.com/denislav86/taskflow-fullstack/actions/workflows/ci.yml/badge.svg)](https://github.com/denislav86/taskflow-fullstack/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-61dafb.svg)](https://reactjs.org/)
[![pnpm](https://img.shields.io/badge/pnpm-8-f69220.svg)](https://pnpm.io/)

[Features](#features) • [Quick Start](#quick-start) • [Architecture](#architecture) • [Development](#development) • [API Docs](#api-documentation)

</div>

---

## Overview

TaskFlow is a **portfolio-ready, full-stack task management application** built with FastAPI and React. It demonstrates modern web development practices including JWT authentication, RESTful API design, responsive UI, and containerized deployment.

### Perfect for:
- 📚 **Learning** - Full-stack development patterns
- 💼 **Portfolio** - Showcase your skills
- 🚀 **SaaS Starter** - Foundation for your next project
- 🏢 **Internal Tools** - Team task management

## Features

| Feature | Description |
|---------|-------------|
| ✅ **CRUD Operations** | Create, read, update, and delete tasks |
| 🔐 **JWT Authentication** | Secure login with access & refresh tokens |
| 🔍 **Advanced Filtering** | Filter by status, priority, search text |
| 📊 **Analytics Dashboard** | Track productivity with charts |
| 🌓 **Dark/Light Mode** | Beautiful theme switching |
| 📱 **Responsive Design** | Works on all devices |
| 🐳 **Docker Ready** | One command setup |
| ✅ **Test Coverage** | Comprehensive pytest tests |
| 🚀 **CI/CD** | GitHub Actions pipeline |

---

## Quick Start

### Prerequisites

- [Docker](https://www.docker.com/get-started) & Docker Compose v2+
- [Git](https://git-scm.com/)
- Make (optional, for convenience commands)

### One-Command Setup

```bash
# Clone the repository
git clone https://github.com/denislav86/taskflow-fullstack.git
cd taskflow-fullstack

# Start everything (builds, migrates, seeds)
make setup
```

This will:
1. Build all Docker containers
2. Start PostgreSQL, Backend, and Frontend
3. Run database migrations
4. Seed demo data

### Access the Application

| Service | URL |
|---------|-----|
| 🌐 Frontend | http://localhost:3000 |
| ⚡ Backend API | http://localhost:8000 |
| 📚 API Docs | http://localhost:8000/docs |
| 📖 ReDoc | http://localhost:8000/redoc |

### Demo Credentials

```
Email:    demo@taskflow.dev
Password: demo1234
```

---

## Architecture

### System Overview

```mermaid
graph TB
    subgraph Client
        Browser[Web Browser]
    end
    
    subgraph Docker["Docker Compose"]
        subgraph Frontend["Frontend Container :3000"]
            React[React + Vite]
        end
        
        subgraph Backend["Backend Container :8000"]
            FastAPI[FastAPI]
            Alembic[Alembic Migrations]
        end
        
        subgraph Database["Database Container :5432"]
            PostgreSQL[(PostgreSQL)]
        end
    end
    
    Browser --> React
    React -->|HTTP/REST| FastAPI
    FastAPI -->|SQLAlchemy| PostgreSQL
    Alembic -->|Migrations| PostgreSQL
```

### Request Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant F as Frontend
    participant B as Backend
    participant D as Database
    
    C->>F: User Action
    F->>B: API Request + JWT
    B->>B: Validate Token
    B->>D: Query/Mutation
    D-->>B: Result
    B-->>F: JSON Response
    F-->>C: Updated UI
```

### Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 18, TypeScript, Vite | UI Framework |
| | TanStack Query | Server State |
| | Zustand | Client State |
| | Tailwind CSS | Styling |
| | React Router | Routing |
| **Backend** | FastAPI | API Framework |
| | SQLAlchemy 2.0 | ORM |
| | Pydantic v2 | Validation |
| | Alembic | Migrations |
| | python-jose | JWT Auth |
| **Database** | PostgreSQL 15 | Data Storage |
| **DevOps** | Docker, pnpm | Containerization |
| | GitHub Actions | CI/CD |

---

## Project Structure

```
taskflow-fullstack/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py              # Dependency injection
│   │   │   └── routers/             # API endpoints
│   │   │       ├── auth.py
│   │   │       ├── tasks.py
│   │   │       └── analytics.py
│   │   ├── core/
│   │   │   ├── config.py            # Settings
│   │   │   ├── database.py          # DB connection
│   │   │   ├── exceptions.py        # Custom exceptions
│   │   │   └── security.py          # JWT & hashing
│   │   ├── models/                  # SQLAlchemy models
│   │   ├── schemas/                 # Pydantic schemas
│   │   ├── services/                # Business logic
│   │   └── main.py                  # FastAPI app
│   ├── alembic/                     # DB migrations
│   ├── tests/                       # pytest tests
│   ├── scripts/seed.py              # Demo data
│   ├── Dockerfile                   # Dev image
│   ├── Dockerfile.prod              # Production image
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/              # Header, Layout
│   │   │   ├── tasks/               # Task components
│   │   │   └── ui/                  # Reusable UI
│   │   ├── hooks/                   # React Query hooks
│   │   ├── pages/                   # Route pages
│   │   ├── services/                # API functions
│   │   ├── store/                   # Zustand stores
│   │   ├── types/                   # TypeScript types
│   │   └── App.tsx
│   ├── Dockerfile                   # Dev image
│   ├── Dockerfile.prod              # Production image
│   └── package.json
│
├── .github/workflows/ci.yml         # CI/CD pipeline
├── docker-compose.yml               # Development
├── docker-compose.prod.yml          # Production
├── Makefile                         # Dev commands
└── README.md
```

---

## Development

### Available Commands

```bash
make help                 # Show all commands

# 🐳 Docker Commands
make up                   # Start services (foreground)
make up-d                 # Start services (background)
make down                 # Stop services
make build                # Rebuild containers
make logs                 # View all logs
make logs-backend         # View backend logs
make logs-frontend        # View frontend logs

# 💻 Development
make backend-shell        # Shell into backend
make frontend-shell       # Shell into frontend
make db-shell             # PostgreSQL shell
make lint                 # Run all linters
make typecheck            # TypeScript check

# 🗄️ Database
make migrate              # Run migrations
make migrate-create name="description"
make seed                 # Seed demo data
make db-reset             # Reset database

# 🧪 Testing
make test                 # Run backend tests
make test-cov             # Tests with coverage
```

### Docker Development Strategy

This project uses an optimized Docker setup for local development:

#### Backend Caching Strategy
- **Layer 1**: System dependencies (rarely changes)
- **Layer 2**: Python dependencies via `requirements.txt`
- **Layer 3**: Application code (hot-reloaded)

```dockerfile
# requirements.txt is copied first
COPY requirements.txt .
RUN pip install -r requirements.txt

# Source code mounted via docker-compose volumes
```

#### Frontend Caching Strategy
- Uses **pnpm** for fast, efficient dependency management
- Smart entrypoint script detects dependency changes
- Only reinstalls when `package.json` or `pnpm-lock.yaml` change

```dockerfile
# Dependencies installed in image
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Entrypoint checks for changes at runtime
ENTRYPOINT ["/docker-entrypoint.sh"]
```

### Running Without Docker

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://user:pass@localhost:5432/taskflow
export SECRET_KEY=secret-key

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
corepack enable
pnpm install

# Start dev server
pnpm dev
```

---

## CI/CD Pipeline

The GitHub Actions workflow runs on every push and PR:

```mermaid
graph LR
    subgraph Backend
        BT[Tests] --> BL[Lint]
        BL --> BD[Docker Build]
    end
    
    subgraph Frontend
        FL[Lint] --> FT[TypeScript]
        FT --> FB[Build]
        FL --> FD[Docker Build]
    end
```

### Pipeline Jobs

| Job | Description | Triggers |
|-----|-------------|----------|
| `backend-test` | pytest + flake8 | All pushes |
| `backend-build` | Docker image build | After tests pass |
| `frontend-lint` | ESLint + TypeScript | All pushes |
| `frontend-build` | Vite production build | After lint passes |
| `frontend-docker` | Docker image build | After lint passes |

---

## API Documentation

### Authentication

#### Register
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Tasks

#### List Tasks
```http
GET /tasks?status=todo&priority=high&search=meeting&page=1&page_size=10
Authorization: Bearer <access_token>
```

#### Create Task
```http
POST /tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "New task",
  "description": "Task description",
  "status": "todo",
  "priority": "medium",
  "due_date": "2024-01-25T12:00:00Z"
}
```

### Analytics

```http
GET /analytics/summary
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "total_tasks": 12,
  "completed_tasks": 5,
  "pending_tasks": 4,
  "in_progress_tasks": 3,
  "overdue_tasks": 1,
  "completed_this_week": 3,
  "high_priority_pending": 2,
  "completion_rate": 41.7
}
```

---

## Environment Variables

### Backend

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection | `postgresql://taskflow:taskflow@db:5432/taskflow` |
| `SECRET_KEY` | JWT signing key | Required in production |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | `7` |
| `CORS_ORIGINS` | Allowed origins | `["http://localhost:3000"]` |
| `DEBUG` | Debug mode | `false` |

### Frontend

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` |

---

## Production Deployment

### Using Production Docker Compose

```bash
# Create .env file with production values
cp .env.example .env.prod
# Edit .env.prod with your values

# Build and start
docker compose -f docker-compose.prod.yml up -d --build
```

### Production Checklist

- [ ] Set strong `SECRET_KEY`
- [ ] Set strong `POSTGRES_PASSWORD`
- [ ] Configure `CORS_ORIGINS` for your domain
- [ ] Set up HTTPS (nginx/traefik)
- [ ] Configure proper logging
- [ ] Set up monitoring

---

## Future Improvements

### Planned Features
- [ ] Email verification
- [ ] Password reset flow
- [ ] Task categories/labels
- [ ] Task comments & attachments
- [ ] Team collaboration
- [ ] Real-time notifications (WebSocket)
- [ ] Calendar view
- [ ] Mobile app (React Native)

### Infrastructure
- [ ] Kubernetes deployment
- [ ] Redis caching
- [ ] Background jobs (Celery)
- [ ] S3 file storage

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow existing code style
- Add tests for new features
- Update documentation
- Keep PRs focused and small

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - JavaScript UI library
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Lucide Icons](https://lucide.dev/) - Beautiful icons
- [pnpm](https://pnpm.io/) - Fast, disk space efficient package manager

---

<div align="center">

**Built with ❤️ for the developer community**

[⬆ Back to Top](#taskflow)

</div>
