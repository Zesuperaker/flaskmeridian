"""Environment configuration files generator - creates .env with secrets and db config"""
import click
import secrets


def create(project_path, db_type='sqlite'):
    """Create .env file with generated secrets and database configuration

    Args:
        project_path: Path to project directory
        db_type: Database type ('sqlite' or 'postgres')
    """

    # Generate secure random secrets
    secret_key = secrets.token_urlsafe(32)
    password_salt = secrets.token_urlsafe(32)

    # Set database URL based on type
    if db_type == 'postgres':
        database_url = 'postgresql://user:password@localhost/flaskmeridian_db'
    else:
        database_url = 'sqlite:///app.db'

    env_content = f'''# Flask-Security Configuration
# IMPORTANT: Never commit this file! It's already in .gitignore
# Generate new secrets for production using:
# python -c "import secrets; print(secrets.token_urlsafe(32))"

SECRET_KEY={secret_key}
SECURITY_PASSWORD_SALT={password_salt}

# Database
# SQLite: sqlite:///app.db
# PostgreSQL: postgresql://user:password@localhost/dbname
DATABASE_URL={database_url}

# Flask Environment
FLASK_ENV=development
FLASK_DEBUG=False
FLASK_PORT=5000

# Email Configuration (optional - for password reset in production)
# Uncomment and configure when using SECURITY_RECOVERABLE=True
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-app-password
'''

    env_file = project_path / '.env'
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)

    click.echo("✅ Created .env with secure generated secrets")
    click.echo(f"   📝 Key: {secret_key[:20]}...")
    click.echo(f"   📝 Salt: {password_salt[:20]}...")

    if db_type == 'postgres':
        click.echo(f"   🗄️  Database: PostgreSQL")
        click.echo(f"   ⚠️  Update DATABASE_URL in .env with your credentials")
    else:
        click.echo(f"   🗄️  Database: SQLite (app.db)")

    click.echo("   ⚠️  .env is in .gitignore - never commit secrets!")
    click.echo("   ℹ️  FLASK_DEBUG=False by default (safe for production)")
    click.echo("   ℹ️  Set FLASK_DEBUG=True for development with auto-reload")


def create_sample(project_path, db_type='sqlite'):
    """Create .env.example file showing structure without real secrets

    Args:
        project_path: Path to project directory
        db_type: Database type ('sqlite' or 'postgres')
    """

    # Set database URL based on type
    if db_type == 'postgres':
        database_url = 'postgresql://user:password@localhost/flaskmeridian_db'
    else:
        database_url = 'sqlite:///app.db'

    env_example = f'''# Flask-Security Configuration (Example)
# Copy this to .env and fill in your actual values
# NEVER commit .env to version control!

SECRET_KEY=your-secret-key-here
SECURITY_PASSWORD_SALT=your-password-salt-here

# Database
# SQLite: sqlite:///app.db
# PostgreSQL: postgresql://user:password@localhost/dbname
DATABASE_URL={database_url}

# Flask Environment
# Set FLASK_DEBUG=True for development with auto-reload
# Always use FLASK_DEBUG=False in production
FLASK_ENV=development
FLASK_DEBUG=False
FLASK_PORT=5000

# Email Configuration (optional - for password reset in production)
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-app-password
'''

    env_example_file = project_path / '.env.example'
    with open(env_example_file, 'w', encoding='utf-8') as f:
        f.write(env_example)

    click.echo("✅ Created .env.example (template for documentation)")