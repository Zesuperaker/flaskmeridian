"""Main app.py generator - updated for new db/models structure"""
import click


def create(project_path, project_name):
    """Create main Flask app file with updated imports"""

    app_content = '''"""FlaskMeridian Application"""
from flask import Flask
from db.database import db, init_db
from routes import register_blueprints


def create_app(config=None):
    """Application factory"""
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config:
        app.config.update(config)

    # Initialize database
    init_db(app)

    # Register blueprints
    register_blueprints(app)

    return app


# Create app instance for Flask CLI
app = create_app()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''
    with open(project_path / 'app.py', 'w', encoding='utf-8') as f:
        f.write(app_content)

    click.echo("✅ Created app.py")


def create_with_auth(project_path, db_type='sqlite'):
    """Create app.py with Flask-Security-Too configuration"""

    if db_type == 'postgres':
        db_uri = "'postgresql://user:password@localhost/flaskmeridian_db'"
    else:
        db_uri = "'sqlite:///app.db'"

    app_content = f'''"""FlaskMeridian Application with Flask-Security-Too"""
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from db.database import db, init_db
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
    }}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''
    with open(project_path / 'app.py', 'w', encoding='utf-8') as f:
        f.write(app_content)

    click.echo("✅ Created app.py with Flask-Security-Too configuration")

    if db_type == 'postgres':
        click.echo("⚠️  Remember to update DATABASE_URI in app.py with your PostgreSQL credentials")