"""Environment configuration files generator - creates .env with secrets"""
import click
import secrets


def create(project_path):
    """Create .env file with generated secrets for Flask-Security"""

    # Generate secure random secrets
    secret_key = secrets.token_urlsafe(32)
    password_salt = secrets.token_urlsafe(32)

    env_content = f'''# Flask-Security Configuration
# IMPORTANT: Never commit this file! It's already in .gitignore
# Generate new secrets for production using:
# python -c "import secrets; print(secrets.token_urlsafe(32))"

SECRET_KEY={secret_key}
SECURITY_PASSWORD_SALT={password_salt}

# Database
# SQLite: sqlite:///app.db
# PostgreSQL: postgresql://user:password@localhost/dbname
DATABASE_URL=sqlite:///app.db

# Flask Environment
FLASK_ENV=development
FLASK_DEBUG=True

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
    click.echo("   ⚠️  .env is in .gitignore - never commit secrets!")


def create_sample(project_path):
    """Create .env.example file showing structure without real secrets"""

    env_example = '''# Flask-Security Configuration (Example)
# Copy this to .env and fill in your actual values
# NEVER commit .env to version control!

SECRET_KEY=your-secret-key-here
SECURITY_PASSWORD_SALT=your-password-salt-here

# Database
# SQLite: sqlite:///app.db
# PostgreSQL: postgresql://user:password@localhost/dbname
DATABASE_URL=sqlite:///app.db

# Flask Environment
FLASK_ENV=development
FLASK_DEBUG=True

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