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
from flask_security import Security, SQLAlchemyUserDatastore
from db.database import init_db, db
from db.models import User, Role
from routes import register_blueprints


def create_app(config=None):
    """Application factory"""
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = {db_uri}
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Flask-Security configuration
    app.config['SECRET_KEY'] = 'change-me-in-production'  # Use: python -c "import secrets; print(secrets.token_urlsafe(32))"
    app.config['SECURITY_PASSWORD_SALT'] = 'change-me-in-production'  # Use: python -c "import secrets; print(secrets.token_urlsafe(32))"
    
    # Password hashing configuration - CRITICAL: use argon2
    app.config['SECURITY_PASSWORD_SCHEMES'] = ['argon2']
    app.config['SECURITY_DEPRECATED_PASSWORD_SCHEMES'] = []
    
    # Registration and account management
    app.config['SECURITY_REGISTERABLE'] = True  # Allow user registration
    app.config['SECURITY_CONFIRMABLE'] = False  # Disable email confirmation (set to True in production)
    app.config['SECURITY_RECOVERABLE'] = False   # Allow password reset

    # Email configuration (optional for development since CONFIRMABLE=False)
    # For production, uncomment and configure:
    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # app.config['MAIL_PORT'] = 587
    # app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_USERNAME'] = 'your-email@example.com'
    # app.config['MAIL_PASSWORD'] = 'your-app-password'
    # app.config['SECURITY_EMAIL_SENDER'] = 'your-email@example.com'

    if config:
        app.config.update(config)

    # Initialize database
    init_db(app)

    # Setup Flask-Security (automatically registers all auth routes)
    # Routes provided by Flask-Security:
    # - GET/POST /login
    # - GET/POST /register
    # - GET /logout
    # - GET/POST /forgot-password (if RECOVERABLE=True)
    # - GET/POST /reset-password/<token> (if RECOVERABLE=True)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # Initialize default roles
    with app.app_context():
        _initialize_default_roles()

    # Register blueprints
    register_blueprints(app)

    return app


def _initialize_default_roles():
    """Create default roles if they don't exist"""
    default_roles = [
        ('admin', 'Administrator - full system access'),
        ('user', 'Regular user'),
        ('moderator', 'Content moderator'),
    ]

    for name, description in default_roles:
        if not Role.query.filter_by(name=name).first():
            role = Role(name=name, description=description)
            db.session.add(role)
            db.session.commit()


# Create app instance for Flask CLI
app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Make database models available in flask shell"""
    from flask_security import hash_password
    return {{
        'db': db,
        'User': User,
        'Role': Role,
        'hash_password': hash_password,
    }}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''

    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    click.echo("✅ Updated app.py with Flask-Security-Too argon2 configuration")
    click.echo("✅ Configured password hashing with argon2 (SECURITY_PASSWORD_SCHEMES)")
    click.echo("✅ Email confirmation DISABLED for development (SECURITY_CONFIRMABLE=False)")
    click.echo("⚠️  For production, enable SECURITY_CONFIRMABLE=True and configure email settings")

    if db_type == 'postgres':
        click.echo("⚠️  Remember to update SQLALCHEMY_DATABASE_URI in app.py with your PostgreSQL credentials")