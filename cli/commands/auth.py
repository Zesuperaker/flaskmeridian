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
    - Flask-Security-Too configuration in app.py
    - Auth HTML templates (login, signup, profile)
    - Built-in authentication routes (no custom code needed!)

    Built-in Routes (Flask-Security):
    - /login           - Login form & handler
    - /register        - Registration form & handler
    - /logout          - Logout handler
    - /forgot-password - Password reset request
    - /reset-password/<token> - Password reset confirmation

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

        # Import auth setup modules (no auth_routes - Flask-Security provides everything)
        from cli.templates.auth import (
            auth_models,
            auth_templates,
            auth_config,
            auth_requirements,
        )

        # 1. Create User and Role models
        auth_models.update_models(Path('db'))

        # 2. Create auth HTML templates
        auth_templates.create(Path('templates'))

        # 3. Update app.py with Flask-Security-Too configuration
        auth_config.update_app(Path('app.py'), db_type)

        # 4. Update requirements.txt with Flask-Security-Too and argon2
        auth_requirements.update(Path('requirements.txt'))

        click.echo(f"\n{'=' * 60}")
        click.echo(f"✨ Flask-Security-Too Authentication Successfully Added!")
        click.echo(f"{'=' * 60}\n")

        click.echo("📋 What was created:")
        click.echo("  ✅ User and Role models (db/models/user.py, db/models/role.py)")
        click.echo("  ✅ Auth templates (templates/auth/login.html, signup.html, profile.html)")
        click.echo("  ✅ Flask-Security configuration in app.py")
        click.echo("  ✅ Dependencies in requirements.txt")

        click.echo(f"\n🔐 Built-in Authentication Routes (provided by Flask-Security):")
        click.echo("  • GET/POST /login            - User login page & handler")
        click.echo("  • GET/POST /register         - User registration page & handler")
        click.echo("  • GET /logout                - Logout handler")
        click.echo("  • GET /forgot-password       - Password reset request")
        click.echo("  • GET/POST /reset-password/<token> - Password reset form")

        click.echo(f"\n🔒 Security Features Included:")
        click.echo("  ✓ Argon2 password hashing (modern, secure)")
        click.echo("  ✓ Password verification with Flask-Security")
        click.echo("  ✓ Role-Based Access Control (RBAC)")
        click.echo("  ✓ CSRF protection (automatic)")
        click.echo("  ✓ Session management with remember-me")
        click.echo("  ✓ Login tracking & rate limiting")
        click.echo("  ✓ Account activation/deactivation")
        click.echo("  ✓ Password reset functionality")

        click.echo(f"\n🔌 Database: {db_type.upper()}")

        if db_type == 'postgres':
            click.echo("\n⚠️  PostgreSQL Configuration Required:")
            click.echo("   Update DATABASE_URI in app.py:")
            click.echo("   app.config['SQLALCHEMY_DATABASE_URI'] = \\")
            click.echo("       'postgresql://user:password@localhost/dbname'")

        click.echo(f"\n📦 Next Steps:")
        click.echo(f"   1. Install dependencies:")
        click.echo(f"      pip install -r requirements.txt")

        click.echo(f"\n   2. Update secrets in app.py (CRITICAL for production):")
        click.echo(f"      import secrets")
        click.echo(f"      secrets.token_urlsafe(32)  # For SECRET_KEY")
        click.echo(f"      secrets.token_urlsafe(32)  # For SECURITY_PASSWORD_SALT")

        if db_type == 'postgres':
            click.echo(f"\n   3. Update PostgreSQL connection string in app.py")

        click.echo(f"\n   4. Delete old database and restart:")
        click.echo(f"      rm app.db")
        click.echo(f"      python app.py")

        click.echo(f"\n   5. Test authentication in browser:")
        click.echo(f"      • Register: http://localhost:5000/register")
        click.echo(f"      • Login:    http://localhost:5000/login")
        click.echo(f"      • Profile:  http://localhost:5000/profile")
        click.echo(f"      • Logout:   http://localhost:5000/logout")

        click.echo(f"\n🛡️  Protecting Routes:")
        click.echo(f"")
        click.echo(f"   from flask_security import auth_required, current_user")
        click.echo(f"")
        click.echo(f"   @app.route('/dashboard')")
        click.echo(f"   @auth_required()")
        click.echo(f"   def dashboard():")
        click.echo(f"       return f'Welcome {{current_user.email}}!'")
        click.echo(f"")
        click.echo(f"   # Check roles:")
        click.echo(f"   if current_user.has_role('admin'):")
        click.echo(f"       # Admin only code")

        click.echo(f"\n📚 Database Models:")
        click.echo(f"   User model includes:")
        click.echo(f"   - email, username, password (hashed with argon2)")
        click.echo(f"   - first_name, last_name")
        click.echo(f"   - active status")
        click.echo(f"   - login tracking (login_count, last_login_at, etc.)")
        click.echo(f"   - roles relationship (many-to-many with Role)")
        click.echo(f"")
        click.echo(f"   Role model includes:")
        click.echo(f"   - name, description")

        click.echo(f"\n{'=' * 60}\n")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise


if __name__ == '__main__':
    auth()