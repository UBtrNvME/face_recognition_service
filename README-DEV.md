# Local Development Guide

## Quick Start

### Option 1: Backend in Docker, Frontend Locally (Recommended)

1. **Start backend services (PostgreSQL + Backend) in Docker:**
   ```bash
   make dev-up-backend
   ```
   This starts only the database and backend services.

2. **Run frontend locally with hot reload:**
   ```bash
   cd apps/frontend
   npm install  # First time only
   npm run dev
   ```
   Frontend will be available at `http://localhost:3000` with hot reload enabled.

### Option 2: Everything Locally

1. **Start only PostgreSQL in Docker:**
   ```bash
   docker-compose up postgres -d
   ```

2. **Run backend locally:**
   ```bash
   cd apps/backend
   # Install dependencies with uv (if not already done)
   uv sync
   
   # Run migrations
   alembic upgrade head
   
   # Start backend
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Run frontend locally:**
   ```bash
   cd apps/frontend
   npm install  # First time only
   npm run dev
   ```

## Development URLs

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Notes

- The Vite dev server is configured to proxy `/api/*` requests to `http://localhost:8000`
- Hot reload works automatically for frontend changes
- Backend changes require restart (unless using `--reload` flag with uvicorn)

