"""Init command for generating new Flask projects in current directory"""
import click
from pathlib import Path
import shutil
from cli.templates import (
    html_templates,
    static_files,
    db_files,
    routes_files,
    services_files,
    app_py,
    requirements_files,
)


@click.command()
@click.option(
    '--with-auth',
    is_flag=True,
    help='Include Flask-Security-Too authentication system'
)
def init(with_auth):
    """Initialize a Flask project in the current directory

    This sets up a complete Flask project structure with all necessary
    files and configuration in your current directory.

    Usage:
        # Create a new project directory first
        mkdir my_app
        cd my_app
        flaskmeridian init

        # Or with authentication included
        flaskmeridian init --with-auth
    """

    # Check if we're already in a Flask project
    if Path('app.py').exists():
        click.echo("❌ Error: app.py already exists in this directory", err=True)
        return

    cwd = Path.cwd()

    try:
        click.echo(f"🚀 Initializing FlaskMeridian project in {cwd.name}/\n")

        # Create main directories
        (cwd / 'templates').mkdir(exist_ok=True)
        (cwd / 'services').mkdir(exist_ok=True)
        (cwd / 'routes').mkdir(exist_ok=True)
        (cwd / 'db').mkdir(exist_ok=True)
        (cwd / 'static').mkdir(exist_ok=True)
        (cwd / 'static' / 'js').mkdir(exist_ok=True)
        (cwd / 'static' / 'css').mkdir(exist_ok=True)

        click.echo(f"✅ Created project directories")

        # Create template files
        html_templates.create_base(cwd / 'templates')
        html_templates.create_index(cwd / 'templates')

        # Create static files
        static_files.create(cwd / 'static')

        # Create db files
        db_files.create(cwd / 'db')

        # Create routes directory files
        routes_files.create(cwd / 'routes')

        # Create services directory files
        services_files.create(cwd / 'services')

        # Create requirements.txt
        requirements_files.create(cwd)

        # Create main app file
        app_py.create(cwd, cwd.name)

        click.echo(f"\n{'=' * 60}")
        click.echo(f"✨ FlaskMeridian project initialized successfully!")
        click.echo(f"{'=' * 60}\n")

        click.echo("📁 Project structure created:\n")
        click.echo(f"  templates/")
        click.echo(f"  ├── base.html")
        click.echo(f"  └── index.html")
        click.echo(f"  static/")
        click.echo(f"  ├── css/")
        click.echo(f"  │   └── style.css")
        click.echo(f"  └── js/")
        click.echo(f"  │   └── script.js")
        click.echo(f"  services/")
        click.echo(f"  routes/")
        click.echo(f"  ├── __init__.py")
        click.echo(f"  └── main.py")
        click.echo(f"  db/")
        click.echo(f"  ├── __init__.py")
        click.echo(f"  ├── database.py")
        click.echo(f"  └── models/")
        click.echo(f"  ├── requirements.txt")
        click.echo(f"  └── app.py")

        if with_auth:
            click.echo(f"\n🔧 Adding Flask-Security-Too authentication...\n")

            # Import auth setup modules
            from cli.templates.auth import (
                auth_models,
                auth_routes,
                auth_service,
                auth_templates,
                auth_config,
                auth_requirements,
            )

            # 1. Update models
            auth_models.update_models(cwd / 'db')

            # 2. Create auth routes
            auth_routes.create(cwd / 'routes')

            # 3. Create auth service
            auth_service.create(cwd / 'services')

            # 4. Create auth templates
            auth_templates.create(cwd / 'templates')

            # 5. Update routes __init__.py
            _update_routes_init_with_auth(cwd / 'routes')

            # 6. Update app.py with Flask-Security-Too configuration
            auth_config.update_app(cwd / 'app.py', 'sqlite')

            # 7. Update requirements.txt
            auth_requirements.update(cwd / 'requirements.txt')

            click.echo(f"\n✨ Flask-Security-Too authentication added!")
            click.echo(f"\n🔒 Security Features Included:")
            click.echo(f"   ✓ User registration & login")
            click.echo(f"   ✓ Argon2 password hashing")
            click.echo(f"   ✓ Role-based access control (RBAC)")
            click.echo(f"   ✓ User profile management")
            click.echo(f"   ✓ Login tracking")

        click.echo(f"\n🚀 Get started:")
        click.echo(f"  1. Install dependencies:")
        click.echo(f"     pip install -r requirements.txt")

        if with_auth:
            click.echo(f"\n  2. Update secrets in app.py:")
            click.echo(f"     - Change SECRET_KEY")
            click.echo(f"     - Change SECURITY_PASSWORD_SALT")

        click.echo(f"\n  3. Run your app:")
        click.echo(f"     python app.py")

        click.echo(f"\n  4. Visit http://localhost:5000")

        click.echo(f"\n{'=' * 60}\n")

    except Exception as e:
        click.echo(f"❌ Error initializing project: {e}", err=True)
        raise


def _update_routes_init_with_auth(routes_path):
    """Update routes/__init__.py to register auth blueprint"""
    init_file = routes_path / '__init__.py'

    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'auth' in content.lower():
        return

    updated_content = '''"""Routes module for FlaskMeridian app"""
from flask import Blueprint
from .auth import auth_bp
from .main import main_bp


def register_blueprints(app):
    """Register all route blueprints"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
'''
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    click.echo("✅ Updated routes/__init__.py to register auth blueprint")


if __name__ == '__main__':
    init()