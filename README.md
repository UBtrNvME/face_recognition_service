# Face Recognition Service

A production-grade face recognition service built with FastAPI, SQLAlchemy, PostgreSQL with pgvector, and dlib.

## Features

- User authentication with JWT tokens
- Face enrollment and matching
- PostgreSQL with pgvector for efficient vector similarity search
- Docker Compose setup for easy deployment
- Alembic migrations for database schema management

## Prerequisites

- Docker and Docker Compose
- Make (optional, for convenience commands)

## Quick Start

### Development

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Start the development environment:
   ```bash
   make dev-up
   ```

   Or manually:
   ```bash
   docker-compose up -d
   ```

3. The API will be available at:
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Production

1. Copy the production environment file:
   ```bash
   cp .env.prod.example .env.prod
   ```

2. **IMPORTANT**: Update `.env.prod` with strong passwords and secret keys!

3. Start the production environment:
   ```bash
   make prod-up
   ```

   Or manually:
   ```bash
   docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
   ```

## Makefile Commands

### Development
- `make dev-up` - Start development environment
- `make dev-down` - Stop development environment
- `make dev-logs` - View development logs
- `make dev-shell` - Open shell in backend container

### Production
- `make prod-up` - Start production environment
- `make prod-down` - Stop production environment
- `make prod-logs` - View production logs

### Database Migrations
- `make migrate` - Run all pending migrations
- `make migrate-create MESSAGE='description'` - Create a new migration
- `make migrate-upgrade` - Upgrade database to head
- `make migrate-downgrade` - Downgrade database by one revision

### Other
- `make test` - Run tests
- `make clean` - Clean up containers and volumes

## Database Migrations

Migrations are automatically run when the backend container starts. To create a new migration:

```bash
make migrate-create MESSAGE='add new field to users'
```

Or manually:
```bash
docker-compose exec backend alembic revision --autogenerate -m "add new field to users"
```

## Environment Variables

See `.env.example` for all available environment variables. Key variables:

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key (use a strong random string in production)
- `POSTGRES_USER` - PostgreSQL username
- `POSTGRES_PASSWORD` - PostgreSQL password
- `POSTGRES_DB` - Database name

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info (protected)

### Users
- `GET /api/v1/users` - List users (paginated)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `POST /api/v1/users` - Create user
- `PATCH /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Face Recognition
- `POST /api/v1/face/enroll?user_id=123` - Enroll faces for a user
- `POST /api/v1/face/match` - Match faces against database

## Dlib Models

The service requires dlib model files:
- `shape_predictor_68_face_landmarks.dat`
- `dlib_face_recognition_resnet_model_v1.dat`

Place these files in the `apps/backend/models/` directory or mount them as a volume.

## Development

### Running Migrations Locally

If you want to run migrations without Docker:

```bash
cd apps/backend
make migrate-local
```

### Creating Migrations Locally

```bash
cd apps/backend
make migrate-create-local MESSAGE='description'
```

## License

MIT

