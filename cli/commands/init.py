"""Init command for generating new Flask projects in current directory with environment variables"""
import click
from pathlib import Path
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

    Environment variables (secrets) are stored in .env file which is
    protected in .gitignore - never commit secrets to version control!

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

        # Create main app file (with or without auth)
        if with_auth:
            app_py.create_with_auth(cwd, 'sqlite')
        else:
            app_py.create(cwd, cwd.name)

        # ========================
        # Generate Configuration Files
        # ========================
        # Import environment and gitignore generators
        from cli.templates import env_file, gitignore_generator

        # Create .env with secure generated secrets
        env_file.create(cwd)

        # Create .env.example for documentation
        env_file.create_sample(cwd)

        # Create .gitignore to protect secrets and common files
        gitignore_generator.create(cwd)

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
        click.echo(f"  ├── .env (secrets - protected by .gitignore)")
        click.echo(f"  ├── .env.example (documentation template)")
        click.echo(f"  ├── .gitignore (protects secrets!)")
        click.echo(f"  └── app.py")

        if with_auth:
            click.echo(f"\n🔧 Adding Flask-Security-Too authentication...\n")

            # Import auth setup modules
            from cli.templates.auth import (
                auth_models,
                auth_templates,
                auth_requirements,
            )

            # 1. Create User and Role models
            auth_models.update_models(cwd / 'db')

            # 2. Create auth HTML templates
            auth_templates.create(cwd / 'templates')

            # 3. Update requirements.txt with Flask-Security-Too, argon2, and python-dotenv
            auth_requirements.update(cwd / 'requirements.txt')

            click.echo(f"\n✨ Flask-Security-Too authentication configured!")
            click.echo(f"\n🔐 Built-in Authentication Routes (Flask-Security):")
            click.echo(f"   • /login              - User login")
            click.echo(f"   • /register           - User registration")
            click.echo(f"   • /logout             - User logout")
            click.echo(f"   • /forgot-password    - Password reset request")
            click.echo(f"   • /reset-password/<token> - Password reset confirmation")
            click.echo(f"\n🔒 Security Features Included:")
            click.echo(f"   ✓ User registration & login")
            click.echo(f"   ✓ Argon2 password hashing")
            click.echo(f"   ✓ Role-based access control (RBAC)")
            click.echo(f"   ✓ Password reset functionality")
            click.echo(f"   ✓ CSRF protection")
            click.echo(f"   ✓ Automatic Flask-Login integration")
            click.echo(f"   ✓ Auth templates (login, signup, profile)")

        click.echo(f"\n🚀 Get started:")
        click.echo(f"  1. Install dependencies:")
        click.echo(f"     pip install -r requirements.txt")

        click.echo(f"\n  2. Verify .env was created with secrets:")
        click.echo(f"     cat .env")

        if with_auth:
            click.echo(f"\n  3. Run your app:")
            click.echo(f"     python app.py")
            click.echo(f"\n  4. Visit in browser:")
            click.echo(f"     • Home:     http://localhost:5000")
            click.echo(f"     • Register: http://localhost:5000/register")
            click.echo(f"     • Login:    http://localhost:5000/login")
            click.echo(f"     • Profile:  http://localhost:5000/profile")
        else:
            click.echo(f"\n  3. Run your app:")
            click.echo(f"     python app.py")
            click.echo(f"\n  4. Visit http://localhost:5000")

        click.echo(f"\n🔐 Security Notes:")
        click.echo(f"   • .env is in .gitignore - never commit secrets!")
        click.echo(f"   • .env.example shows structure without secrets")
        click.echo(f"   • Share .env.example with team, not .env")
        click.echo(f"   • Copy .env.example → .env on new machines")

        click.echo(f"\n{'=' * 60}\n")

    except Exception as e:
        click.echo(f"❌ Error initializing project: {e}", err=True)
        raise


if __name__ == '__main__':
    init()