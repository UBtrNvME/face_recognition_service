FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for dlib and opencv
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first (better caching)
COPY pyproject.toml uv.lock ./

# Install deps (including alembic for migrations)
RUN uv pip install --system --no-cache .

# Copy application code
COPY app ./app
COPY alembic.ini ./
COPY alembic ./alembic

# Create directory for dlib models (can be mounted as volume)
RUN mkdir -p /app/models

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
