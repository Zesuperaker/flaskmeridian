"""Routes files generator"""
import click


def create(routes_path):
    """Create routes directory files"""

    # __init__.py - FIXED to properly register blueprints
    init_content = '''"""Routes module for FlaskMeridian app"""
from flask import Blueprint
from .main import main_bp


def register_blueprints(app):
    """Register all route blueprints"""
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