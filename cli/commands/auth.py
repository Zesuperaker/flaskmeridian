"""Auth command for generating Flask-Security-Too authentication system with environment variables"""
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
    ⚡ Set up Flask-Security-Too authentication system with environment variables

    Creates:
    - User and Role database models with RBAC
    - Auth HTML templates (login, signup, profile)
    - Built-in authentication routes (no custom code needed!)
    - .env file with secure secrets
    - .gitignore to protect secrets

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

        # Import auth setup modules
        from cli.templates.auth import (
            auth_models,
            auth_templates,
            auth_requirements,
        )

        # Import environment and gitignore generators
        from cli.templates import env_files, gitignore_generator

        # 1. Create User and Role models
        auth_models.update_models(Path('db'))

        # 2. Create auth HTML templates
        auth_templates.create(Path('templates'))

        # 3. Update requirements.txt with Flask-Security-Too, argon2, and python-dotenv
        auth_requirements.update(Path('requirements.txt'))

        # 4. Generate .env if it doesn't exist (preserve existing if present)
        env_file = Path('.env')
        if not env_file.exists():
            env_files.create(Path.cwd())
        else:
            click.echo("ℹ️  .env already exists (preserving existing secrets)")

        # 5. Generate .env.example if it doesn't exist
        env_example = Path('.env.example')
        if not env_example.exists():
            env_files.create_sample(Path.cwd())

        # 6. Generate or update .gitignore
        if not Path('.gitignore').exists():
            gitignore_generator.create(Path.cwd())
        else:
            click.echo("ℹ️  .gitignore already exists")

        click.echo(f"\n{'=' * 60}")
        click.echo(f"✨ Flask-Security-Too Authentication Successfully Added!")
        click.echo(f"{'=' * 60}\n")

        click.echo("📋 What was created:")
        click.echo("  ✅ User and Role models (db/models/user.py, db/models/role.py)")
        click.echo("  ✅ Auth templates (templates/security/login_user.html, register_user.html)")
        click.echo("  ✅ Flask-Security configuration in app.py")
        click.echo("  ✅ Dependencies in requirements.txt")
        click.echo("  ✅ .env with secure generated secrets")
        click.echo("  ✅ .env.example as documentation template")
        click.echo("  ✅ .gitignore protecting secrets")

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
        click.echo("  ✓ Environment-based secret management")

        click.echo(f"\n🔌 Database: {db_type.upper()}")

        if db_type == 'postgres':
            click.echo("\n⚠️  PostgreSQL Configuration Required:")
            click.echo("   Update DATABASE_URL in .env:")
            click.echo("   DATABASE_URL=postgresql://user:password@localhost/dbname")

        click.echo(f"\n📦 Next Steps:")
        click.echo(f"   1. Install dependencies:")
        click.echo(f"      pip install -r requirements.txt")

        click.echo(f"\n   2. Verify .env was created:")
        click.echo(f"      cat .env")

        click.echo(f"\n   3. Check that .env is protected:")
        click.echo(f"      grep '.env' .gitignore")

        if db_type == 'postgres':
            click.echo(f"\n   4. Update DATABASE_URL in .env with PostgreSQL connection")
            click.echo(f"\n   5. Delete old database and restart:")
        else:
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