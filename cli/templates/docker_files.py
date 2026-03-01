"""Docker configuration files generator - Dockerfile and docker-compose.yml"""
import click
from pathlib import Path


def create(project_path, db_type='sqlite'):
    """Create Dockerfile and docker-compose.yml based on database type

    Args:
        project_path: Path to project directory
        db_type: Database type ('sqlite' or 'postgres')
    """

    # ========================
    # Dockerfile - Production-ready multi-stage build
    # ========================
    dockerfile_content = '''# FlaskMeridian Application Dockerfile
# Multi-stage build for optimized production image

# ==================== BUILD STAGE ====================
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies to venv
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# ==================== RUNTIME STAGE ====================
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Copy venv from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY . .

# Set environment
ENV PATH="/opt/venv/bin:$PATH" \\
    PYTHONUNBUFFERED=1 \\
    PYTHONDONTWRITEBYTECODE=1 \\
    FLASK_APP=app.py

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=5)"

# Run application with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
'''

    # ========================
    # docker-compose.yml - SQLite version
    # ========================
    if db_type == 'sqlite':
        docker_compose_content = '''# FlaskMeridian Docker Compose - SQLite Version
version: '3.9'

services:
  app:
    build: .
    container_name: flaskmeridian_app
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
      - DATABASE_URL=sqlite:///app.db
    volumes:
      - .:/app
      - ./instance:/app/instance
    command: flask run --host=0.0.0.0
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  app_data:
    driver: local
'''
    else:
        # PostgreSQL version
        docker_compose_content = '''# FlaskMeridian Docker Compose - PostgreSQL Version
version: '3.9'

services:
  db:
    image: postgres:15-alpine
    container_name: flaskmeridian_db
    environment:
      POSTGRES_USER: flaskuser
      POSTGRES_PASSWORD: flaskpassword
      POSTGRES_DB: flaskmeridian_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U flaskuser"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    build: .
    container_name: flaskmeridian_app
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
      - DATABASE_URL=postgresql://flaskuser:flaskpassword@db:5432/flaskmeridian_db
    volumes:
      - .:/app
    command: sh -c "flask db upgrade && gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 60 app:app"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  postgres_data:
    driver: local
'''

    # ========================
    # .dockerignore
    # ========================
    dockerignore_content = '''# Git
.git
.gitignore
.gitattributes

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.pytest_cache/
.coverage
htmlcov/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment
.env
.env.local
.env.*.local

# Database
*.db
*.sqlite
*.sqlite3
instance/

# Misc
.cache
.mypy_cache/
.dmypy.json
dmypy.json
.pyre/
Thumbs.db
node_modules/
'''

    # ========================
    # docker-compose.override.yml for development
    # ========================
    docker_compose_override = '''# Docker Compose Override for Development
# This file is automatically used by docker-compose when present
# It overrides settings in docker-compose.yml for local development

version: '3.9'

services:
  app:
    command: flask run --host=0.0.0.0
    environment:
      - FLASK_DEBUG=True
    stdin_open: true
    tty: true
'''

    if db_type == 'postgres':
        docker_compose_override += '''
  db:
    environment:
      POSTGRES_USER: flaskuser
      POSTGRES_PASSWORD: flaskpassword
      POSTGRES_DB: flaskmeridian_db
'''

    # ========================
    # Write files
    # ========================
    with open(project_path / 'Dockerfile', 'w', encoding='utf-8') as f:
        f.write(dockerfile_content)
    click.echo("✅ Created Dockerfile (multi-stage production build)")

    with open(project_path / 'docker-compose.yml', 'w', encoding='utf-8') as f:
        f.write(docker_compose_content)

    if db_type == 'postgres':
        click.echo("✅ Created docker-compose.yml (with PostgreSQL service)")
    else:
        click.echo("✅ Created docker-compose.yml (SQLite version)")

    with open(project_path / 'docker-compose.override.yml', 'w', encoding='utf-8') as f:
        f.write(docker_compose_override)
    click.echo("✅ Created docker-compose.override.yml (development overrides)")

    with open(project_path / '.dockerignore', 'w', encoding='utf-8') as f:
        f.write(dockerignore_content)
    click.echo("✅ Created .dockerignore")

    # Print Docker usage instructions
    _print_docker_usage(db_type)


def _print_docker_usage(db_type):
    """Print Docker usage instructions"""
    click.echo("\n" + "=" * 70)
    click.echo("🐳 Docker Setup Complete!")
    click.echo("=" * 70 + "\n")

    click.echo("Quick Start with Docker:\n")

    click.echo("1. Build the image:")
    click.echo("   docker-compose build\n")

    click.echo("2. Start the application:")
    click.echo("   docker-compose up\n")

    click.echo("3. Application will be available at:")
    click.echo("   http://localhost:5000\n")

    if db_type == 'postgres':
        click.echo("4. Initialize the database:")
        click.echo("   docker-compose exec app flask db upgrade\n")

        click.echo("5. Database credentials (from docker-compose.yml):")
        click.echo("   Host: db")
        click.echo("   Port: 5432")
        click.echo("   User: flaskuser")
        click.echo("   Password: flaskpassword")
        click.echo("   Database: flaskmeridian_db\n")

    click.echo("Development Mode:")
    click.echo("   - docker-compose.override.yml enables FLASK_DEBUG=True")
    click.echo("   - Auto-reload enabled")
    click.echo("   - Run: docker-compose up\n")

    click.echo("Production Mode:")
    click.echo("   - Remove docker-compose.override.yml")
    click.echo("   - Uses gunicorn with 4 workers")
    click.echo("   - Run: docker-compose -f docker-compose.yml up\n")

    click.echo("Useful Commands:")
    click.echo("   docker-compose logs -f          # View logs")
    click.echo("   docker-compose down              # Stop all services")
    click.echo("   docker-compose ps                # List running services")

    if db_type == 'postgres':
        click.echo("   docker-compose exec db psql -U flaskuser -d flaskmeridian_db  # Access database\n")
    else:
        click.echo("")