"""Main app.py generator"""
import click


def create(project_path, project_name):
    """Create main Flask app file with proper app factory pattern"""

    app_content = '''"""FlaskMeridian Application"""
from flask import Flask
from db.database import init_db, db
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
    with open(project_path / 'app.py', 'w') as f:
        f.write(app_content)

    click.echo("✅ Created app.py")