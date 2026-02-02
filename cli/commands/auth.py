"""Auth command for generating Flask-Security-Too authentication system"""
import click
from pathlib import Path


@click.command()
@click.option(
    '--db-type',
    type=click.Choice(['sqlite', 'postgres']),
    default='sqlite',
    help='Database type for authentication'
)
def auth(db_type):
    """
    ⚡ Set up Flask-Security-Too authentication system

    Creates:
    - User and Role database models with RBAC
    - Authentication routes (login, signup, logout, profile)
    - Authentication service with business logic
    - Professional HTML templates
    - Flask-Security-Too configuration

    Usage:
        flaskmeridian auth              # SQLite
        flaskmeridian auth --db-type=postgres  # PostgreSQL
    """

    app_py = Path('app.py')
    if not app_py.exists():
        click.echo("❌ Error: app.py not found. Run this from your FlaskMeridian project root", err=True)
        return

    try:
        click.echo("🔧 Setting up Flask-Security-Too authentication system...\n")

        # Import all template generators
        from cli.templates.auth import (
            auth_models,
            auth_routes,
            auth_service,
            auth_templates,
            auth_config,
            auth_requirements,
        )

        # 1. Update models
        auth_models.update_models(Path('db'))

        # 2. Create auth routes
        auth_routes.create(Path('routes'))

        # 3. Create auth service
        auth_service.create(Path('services'))

        # 4. Create auth templates
        auth_templates.create(Path('templates'))

        # 5. Update routes __init__.py
        _update_routes_init(Path('routes'))

        # 6. Update app.py with Flask-Security-Too configuration
        auth_config.update_app(Path('app.py'), db_type)

        # 7. Update requirements.txt
        auth_requirements.update(Path('requirements.txt'))

        click.echo(f"\n{'=' * 60}")
        click.echo(f"✨ Authentication System Successfully Added!")
        click.echo(f"{'=' * 60}\n")

        click.echo("📋 What was created:")
        click.echo("  ✅ User and Role models (db/models.py)")
        click.echo("  ✅ Auth routes (routes/auth.py)")
        click.echo("  ✅ Auth service (services/auth_service.py)")
        click.echo("  ✅ Auth templates (templates/auth/)")
        click.echo("  ✅ Flask-Security configuration (app.py)")
        click.echo("  ✅ Dependencies (requirements.txt)")

        click.echo(f"\n🔌 Database: {db_type.upper()}")

        if db_type == 'postgres':
            click.echo("\n⚠️  PostgreSQL Configuration Required:")
            click.echo("   Update in app.py:")
            click.echo("   app.config['SQLALCHEMY_DATABASE_URI'] = \\")
            click.echo("       'postgresql://user:password@localhost/dbname'")

        click.echo(f"\n📦 Flask-Security-Too Includes:")
        click.echo("   • Password hashing (via passlib)")
        click.echo("   • Email validation (via email-validator)")
        click.echo("   • Session management (via flask-login)")

        click.echo(f"\n🚀 Next Steps:")
        click.echo(f"   1. Install dependencies:")
        click.echo(f"      pip install -r requirements.txt")
        click.echo(f"\n   2. Update configuration in app.py:")
        click.echo(f"      - Set SECRET_KEY")
        click.echo(f"      - Set SECURITY_PASSWORD_SALT")
        if db_type == 'postgres':
            click.echo(f"      - Update database URI")

        click.echo(f"\n   3. Start your app:")
        click.echo(f"      python app.py")

        click.echo(f"\n   4. Test authentication:")
        click.echo(f"      • Signup:  http://localhost:5000/auth/signup")
        click.echo(f"      • Login:   http://localhost:5000/auth/login")
        click.echo(f"      • Profile: http://localhost:5000/auth/profile")

        click.echo(f"\n🔒 Security Features:")
        click.echo(f"   ✓ Passlib password hashing (industry standard)")
        click.echo(f"   ✓ Automatic email validation")
        click.echo(f"   ✓ Session management with remember-me")
        click.echo(f"   ✓ CSRF protection")
        click.echo(f"   ✓ Role-based access control (RBAC)")
        click.echo(f"   ✓ Login tracking")
        click.echo(f"   ✓ Account activation/deactivation")

        click.echo(f"\n{'=' * 60}\n")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise


def _update_routes_init(routes_path):
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
    auth()