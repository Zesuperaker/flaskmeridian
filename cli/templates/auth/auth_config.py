"""Auth config generator - updates app.py with Flask-Security-Too configuration"""
import click
from pathlib import Path


def update_app(app_path, db_type):
    """Update app.py to include Flask-Security-Too configuration with argon2"""

    with open(app_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already configured
    if 'Flask-Security' in content or 'Security(' in content:
        click.echo("⚠️  app.py already appears to have Flask-Security-Too configured (skipping)")
        return

    # Build the database URI based on type
    if db_type == 'postgres':
        db_uri = "'postgresql://user:password@localhost/flaskmeridian_db'"
    else:
        db_uri = "'sqlite:///app.db'"

    # Updated app.py content with Flask-Security-Too with argon2 configuration
    updated_content = f'''"""FlaskMeridian Application with Flask-Security-Too Authentication"""
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from db.database import init_db, db
from db.models import User, Role
from routes import register_blueprints
from services.auth_service import AuthService


def create_app(config=None):
    """Application factory"""
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = {db_uri}
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Flask-Security configuration
    app.config['SECRET_KEY'] = 'change-me-in-production'  # Use: secrets.token_urlsafe(32)
    app.config['SECURITY_PASSWORD_SALT'] = 'change-me-in-production'  # Use: secrets.token_urlsafe(32)
    
    # Password hashing configuration - CRITICAL: use argon2
    app.config['SECURITY_PASSWORD_SCHEMES'] = ['argon2']
    app.config['SECURITY_DEPRECATED_PASSWORD_SCHEMES'] = []

    if config:
        app.config.update(config)

    # Initialize database
    init_db(app)

    # Setup Flask-Security (handles Flask-Login automatically)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # Create default roles
    with app.app_context():
        AuthService.initialize_default_roles()

    # Register blueprints
    register_blueprints(app)

    return app


# Create app instance for Flask CLI
app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Make database models available in flask shell"""
    return {{
        'db': db,
        'User': User,
        'Role': Role,
        'AuthService': AuthService,
        'hash_password': hash_password,
    }}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''

    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    click.echo("✅ Updated app.py with Flask-Security-Too argon2 configuration")
    click.echo("✅ Configured password hashing with argon2 (SECURITY_PASSWORD_SCHEMES)")

    if db_type == 'postgres':
        click.echo("⚠️  Remember to update DATABASE_URI in app.py with your PostgreSQL credentials")