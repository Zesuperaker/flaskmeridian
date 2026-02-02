import click
import os
from pathlib import Path


@click.group()
def cli():
    """FlaskMeridian - Fast Flask setup and automation CLI tool"""
    pass


@cli.command()
@click.argument('project_name')
def create(project_name):
    """Create a new Flask project with directory structure and boilerplate"""
    project_path = Path(project_name)

    if project_path.exists():
        click.echo(f"❌ Directory '{project_name}' already exists", err=True)
        return

    try:
        # Create main directories
        project_path.mkdir()
        (project_path / 'templates').mkdir()
        (project_path / 'services').mkdir()
        (project_path / 'routes').mkdir()
        (project_path / 'db').mkdir()
        (project_path / 'static').mkdir()
        (project_path / 'static' / 'js').mkdir()
        (project_path / 'static' / 'css').mkdir()

        click.echo(f"✅ Created project directory: {project_name}")

        # Create base.html
        create_base_html(project_path / 'templates')

        # Create static files
        create_static_files(project_path / 'static')

        # Create db files
        create_db_files(project_path / 'db')

        # Create routes directory files
        create_routes_files(project_path / 'routes')

        # Create services directory files
        create_services_files(project_path / 'services')

        # Create main app file
        create_app_file(project_path, project_name)

        click.echo(f"\n✨ FlaskMeridian project '{project_name}' created successfully!")
        click.echo(f"📁 Project structure:\n")
        click.echo(f"  {project_name}/")
        click.echo(f"  ├── templates/")
        click.echo(f"  │   └── base.html")
        click.echo(f"  ├── static/")
        click.echo(f"  │   ├── css/")
        click.echo(f"  │   │   └── style.css")
        click.echo(f"  │   └── js/")
        click.echo(f"  │       └── script.js")
        click.echo(f"  ├── services/")
        click.echo(f"  ├── routes/")
        click.echo(f"  │   ├── __init__.py")
        click.echo(f"  │   └── main.py")
        click.echo(f"  ├── db/")
        click.echo(f"  │   ├── __init__.py")
        click.echo(f"  │   ├── database.py")
        click.echo(f"  │   └── models.py")
        click.echo(f"  └── app.py")
        click.echo(f"\n🚀 Get started:")
        click.echo(f"  cd {project_name}")
        click.echo(f"  pip install flask flask-sqlalchemy")
        click.echo(f"  python app.py")

    except Exception as e:
        click.echo(f"❌ Error creating project: {e}", err=True)


def create_base_html(templates_path):
    """Create base.html template"""
    base_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask App{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            background-color: #2c3e50;
            color: white;
            padding: 1rem 0;
            margin-bottom: 2rem;
        }

        header h1 {
            margin: 0;
        }

        main {
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        footer {
            text-align: center;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #ddd;
            color: #666;
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <div class="container">
            <h1>{% block header_title %}Flask Application{% endblock %}</h1>
        </div>
    </header>

    <main class="container">
        {% block content %}
        <p>Welcome to your Flask application built with FlaskMeridian!</p>
        {% endblock %}
    </main>

    <footer class="container">
        <p>&copy; 2024 Your Flask App. Built with FlaskMeridian.</p>
    </footer>

    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
'''
    with open(templates_path / 'base.html', 'w') as f:
        f.write(base_html)
    click.echo("✅ Created templates/base.html")


def create_static_files(static_path):
    """Create static CSS and JS files"""

    # Create style.css
    css_content = '''/* Main stylesheet */
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --text-color: #333;
    --border-color: #ddd;
    --background-color: #f5f5f5;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: var(--text-color);
    background-color: var(--background-color);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* Add your custom styles here */
'''
    with open(static_path / 'css' / 'style.css', 'w') as f:
        f.write(css_content)

    # Create script.js
    js_content = '''// Main JavaScript file

document.addEventListener('DOMContentLoaded', function() {
    console.log('FlaskMeridian app loaded!');
    // Add your scripts here
});
'''
    with open(static_path / 'js' / 'script.js', 'w') as f:
        f.write(js_content)

    click.echo("✅ Created static/css/style.css and static/js/script.js")


def create_db_files(db_path):
    """Create database-related files"""

    # __init__.py
    init_content = '''"""Database module for FlaskMeridian app"""
from .database import db
from .models import *

__all__ = ['db']
'''
    with open(db_path / '__init__.py', 'w') as f:
        f.write(init_content)

    # database.py
    database_content = '''"""Database initialization and configuration"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)

    with app.app_context():
        db.create_all()
'''
    with open(db_path / 'database.py', 'w') as f:
        f.write(database_content)

    # models.py
    models_content = '''"""Database models for FlaskMeridian app"""
from .database import db


class BaseModel(db.Model):
    """Base model with common attributes"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime, 
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )


# Define your models here
# Example:
# class User(BaseModel):
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
'''
    with open(db_path / 'models.py', 'w') as f:
        f.write(models_content)

    click.echo("✅ Created db/__init__.py, db/database.py, db/models.py")


def create_routes_files(routes_path):
    """Create routes directory files"""

    # __init__.py
    init_content = '''"""Routes module for FlaskMeridian app"""
from flask import Blueprint

def register_blueprints(app):
    """Register all route blueprints"""
    # Import and register blueprints here
    # Example: app.register_blueprint(auth_bp)
    pass
'''
    with open(routes_path / '__init__.py', 'w') as f:
        f.write(init_content)

    # main.py
    main_content = '''"""Main routes for the application"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__, url_prefix='/')


@main_bp.route('/')
def index():
    """Homepage route"""
    return render_template('index.html')


@main_bp.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy'}, 200
'''
    with open(routes_path / 'main.py', 'w') as f:
        f.write(main_content)

    click.echo("✅ Created routes/__init__.py and routes/main.py")


def create_services_files(services_path):
    """Create services directory files"""

    # __init__.py
    init_content = '''"""Services module for FlaskMeridian app

Services contain business logic and are reusable across routes.
"""
'''
    with open(services_path / '__init__.py', 'w') as f:
        f.write(init_content)

    click.echo("✅ Created services/__init__.py")


def create_app_file(project_path, project_name):
    """Create main Flask app file"""

    app_content = f'''"""FlaskMeridian Application"""
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


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
'''
    with open(project_path / 'app.py', 'w') as f:
        f.write(app_content)

    click.echo("✅ Created app.py")


if __name__ == '__main__':
    cli()