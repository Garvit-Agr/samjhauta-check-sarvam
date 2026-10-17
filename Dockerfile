# Use official lightweight Python image
FROM python:3.12-slim-bookworm

# Install uv for ultra-fast and reliable dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Set environment variables for production
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0 \
    PORT=8000 \
    PATH="/app/.venv/bin:$PATH"

# Copy dependency specifications first (enables Docker layer caching)
COPY pyproject.toml uv.lock ./

# Install all project dependencies using uv
RUN uv sync --frozen --no-install-project

# Copy application source code and static assets
COPY . .

# Final project installation
RUN uv sync --frozen

# Expose container port
EXPOSE 8000

# Start production server
CMD ["python", "main.py"]
