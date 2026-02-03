"""Routes files generator - simplified for Flask-Security-Too"""
import click


def create(routes_path):
    """Create routes directory files - simplified for Flask-Security-Too

    Note: Flask-Security-Too automatically registers authentication routes:
    - /login, /register, /logout, /forgot-password, /reset-password/<token>

    This function only creates the main app routes.
    """

    # __init__.py - simplified (no auth blueprint registration)
    init_content = '''"""Routes module for FlaskMeridian app

Flask-Security-Too automatically registers authentication routes:
- GET/POST /login              - User login
- GET/POST /register           - User registration
- GET /logout                  - User logout
- GET/POST /forgot-password    - Password reset request
- GET/POST /reset-password/<token> - Password reset confirmation

This file registers application-specific blueprints only.
"""
from .main import main_bp


def register_blueprints(app):
    """Register application blueprints
    
    Flask-Security-Too handles authentication routes automatically via the
    Security() initialization in app.py. This function registers custom
    application blueprints only.
    """
    app.register_blueprint(main_bp)
'''
    with open(routes_path / '__init__.py', 'w', encoding='utf-8') as f:
        f.write(init_content)

    # main.py - renders index.html instead of index route that doesn't exist
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
    with open(routes_path / 'main.py', 'w', encoding='utf-8') as f:
        f.write(main_content)

    click.echo("✅ Created routes/__init__.py and routes/main.py")