# TaskFlow

<div align="center">

![TaskFlow Logo](https://via.placeholder.com/120x120/22c55e/ffffff?text=✓)

**A modern, full-stack task management application**

[![CI](https://github.com/yourusername/taskflow/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/taskflow/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-61dafb.svg)](https://reactjs.org/)

[Features](#features) • [Tech Stack](#tech-stack) • [Quick Start](#quick-start) • [API Documentation](#api-documentation) • [Screenshots](#screenshots)

</div>

---

## Overview

TaskFlow is a portfolio-ready, full-stack task management application built with FastAPI and React. It demonstrates modern web development practices including JWT authentication, RESTful API design, responsive UI, and containerized deployment.

Perfect for:
- 📚 Learning full-stack development
- 💼 Portfolio projects
- 🚀 SaaS starter template
- 🏢 Internal team tools

## Features

- ✅ **Complete CRUD Operations** - Create, read, update, and delete tasks
- 🔐 **JWT Authentication** - Secure login with access & refresh tokens
- 🔍 **Advanced Filtering** - Filter by status, priority, and search text
- 📊 **Analytics Dashboard** - Track productivity with charts and metrics
- 🌓 **Dark/Light Mode** - Beautiful UI with theme switching
- 📱 **Responsive Design** - Works on desktop and mobile
- 🐳 **Docker Ready** - One command to run everything
- ✅ **Test Coverage** - Comprehensive backend tests

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM with type hints
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **pytest** - Testing framework

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **React Query** - Data fetching
- **Zustand** - State management
- **React Router** - Client-side routing
- **Tailwind CSS** - Styling
- **Recharts** - Charts

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD pipeline

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Browser                          │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    React Frontend (Port 3000)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐│
│  │  Pages   │  │Components│  │  Hooks   │  │ Services (API)   ││
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘│
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (Port 8000)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐│
│  │ Routers  │──│ Services │──│  Models  │──│    Schemas       ││
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘│
└─────────────────────────────┬───────────────────────────────────┘
                              │ SQLAlchemy
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PostgreSQL (Port 5432)                        │
│  ┌──────────────────────┐  ┌───────────────────────────────────┐│
│  │       users          │  │              tasks                ││
│  └──────────────────────┘  └───────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
taskflow-fullstack/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py          # Dependency injection
│   │   │   └── routers/         # API endpoints
│   │   ├── core/
│   │   │   ├── config.py        # Settings
│   │   │   ├── database.py      # Database setup
│   │   │   ├── exceptions.py    # Custom exceptions
│   │   │   └── security.py      # JWT & password hashing
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   └── main.py              # FastAPI app
│   ├── alembic/                 # Database migrations
│   ├── tests/                   # pytest tests
│   ├── scripts/
│   │   └── seed.py              # Demo data seeding
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/          # Header, Layout, etc.
│   │   │   ├── tasks/           # Task-related components
│   │   │   └── ui/              # Reusable UI components
│   │   ├── hooks/               # React Query hooks
│   │   ├── pages/               # Route pages
│   │   ├── services/            # API service functions
│   │   ├── store/               # Zustand stores
│   │   ├── types/               # TypeScript types
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile
│   └── package.json
├── .github/workflows/ci.yml     # CI pipeline
├── docker-compose.yml
├── Makefile
└── README.md
```

## Quick Start

### Prerequisites

- [Docker](https://www.docker.com/get-started) & Docker Compose
- [Git](https://git-scm.com/)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/taskflow.git
   cd taskflow
   ```

2. **Start the application**
   ```bash
   make setup
   ```
   This will:
   - Build all Docker containers
   - Run database migrations
   - Seed demo data

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Demo Credentials

```
Email:    demo@taskflow.dev
Password: demo1234
```

## Available Commands

```bash
make help           # Show all available commands

# Docker
make up             # Start all services
make down           # Stop all services
make build          # Rebuild containers
make logs           # View logs

# Development
make backend-shell  # Shell into backend container
make frontend-shell # Shell into frontend container
make db-shell       # PostgreSQL shell

# Database
make migrate        # Run migrations
make seed           # Seed demo data

# Testing
make test           # Run backend tests
make lint           # Run linters
```

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

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
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

Response:
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

Response:
```json
{
  "items": [
    {
      "id": 1,
      "title": "Team meeting",
      "description": "Weekly sync",
      "status": "todo",
      "priority": "high",
      "due_date": "2024-01-20T14:00:00Z",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "owner_id": 1
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
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

#### Get Summary
```http
GET /analytics/summary
Authorization: Bearer <access_token>
```

Response:
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

## Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x500/1f2937/ffffff?text=Dashboard+Screenshot)

### Analytics
![Analytics](https://via.placeholder.com/800x500/1f2937/ffffff?text=Analytics+Screenshot)

### Dark Mode
![Dark Mode](https://via.placeholder.com/800x500/111827/ffffff?text=Dark+Mode+Screenshot)

## Development

### Running Without Docker

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://user:pass@localhost:5432/taskflow
export SECRET_KEY=your-secret-key

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Running Tests
```bash
# Backend tests
cd backend
pytest -v

# Frontend lint
cd frontend
npm run lint
```

## Environment Variables

### Backend
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://taskflow:taskflow@db:5432/taskflow` |
| `SECRET_KEY` | JWT signing key | `your-super-secret-key` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | `7` |
| `CORS_ORIGINS` | Allowed CORS origins | `["http://localhost:3000"]` |

### Frontend
| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` |

## Future Improvements

- [ ] Email verification
- [ ] Password reset flow
- [ ] Task categories/labels
- [ ] Task comments
- [ ] File attachments
- [ ] Team collaboration
- [ ] Notifications
- [ ] Calendar view
- [ ] Mobile app (React Native)
- [ ] Kubernetes deployment

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - JavaScript UI library
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Lucide Icons](https://lucide.dev/) - Beautiful icons

---

<div align="center">
  Made with ❤️ for the developer community
</div>

