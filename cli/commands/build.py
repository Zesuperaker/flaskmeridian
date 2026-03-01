"""Build command - unified interactive project generation for FlaskMeridian"""
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
    env_file,
    gitignore_generator,
)


def _setup_project_structure(project_path):
    """Create all directories and files common to both auth and non-auth projects"""

    # Create main directories
    (project_path / 'templates').mkdir(exist_ok=True)
    (project_path / 'services').mkdir(exist_ok=True)
    (project_path / 'routes').mkdir(exist_ok=True)
    (project_path / 'db').mkdir(exist_ok=True)
    (project_path / 'static').mkdir(exist_ok=True)
    (project_path / 'static' / 'js').mkdir(exist_ok=True)
    (project_path / 'static' / 'css').mkdir(exist_ok=True)

    click.echo(f"✅ Created project directories")

    # Create template files
    html_templates.create_base(project_path / 'templates')
    html_templates.create_index(project_path / 'templates')

    # Create static files
    static_files.create(project_path / 'static')

    # Create db files
    db_files.create(project_path / 'db')

    # Create routes directory files
    routes_files.create(project_path / 'routes')

    # Create services directory files
    services_files.create(project_path / 'services')

    # Create requirements.txt
    requirements_files.create(project_path)


def _setup_auth(project_path):
    """Add Flask-Security-Too authentication to the project"""
    from cli.templates.auth import (
        auth_models,
        auth_templates,
        auth_requirements,
    )

    # Create User and Role models
    auth_models.update_models(project_path / 'db')

    # Create auth HTML templates
    auth_templates.create(project_path / 'templates')

    # Update requirements.txt with Flask-Security-Too, argon2, and python-dotenv
    auth_requirements.update(project_path / 'requirements.txt')


def _setup_config_files(project_path, with_auth=False):
    """Generate .env, .env.example, and .gitignore"""
    # Create .env with secure generated secrets
    env_file.create(project_path)

    # Create .env.example for documentation
    env_file.create_sample(project_path)

    # Create .gitignore to protect secrets and common files
    gitignore_generator.create(project_path)


def _print_success_message(project_path, with_auth):
    """Print completion message with next steps"""
    click.echo(f"\n{'=' * 70}")
    click.echo(f"✨ FlaskMeridian project initialized successfully!")
    click.echo(f"{'=' * 70}\n")

    is_current_dir = project_path == Path.cwd()

    if is_current_dir:
        click.echo(f"📁 Project structure created in current directory\n")
    else:
        click.echo(f"📁 Project created in: {project_path}\n")

    click.echo(f"📦 Next Steps:")
    click.echo(f"")

    if not is_current_dir:
        click.echo(f"  1. Navigate to project:")
        click.echo(f"     cd {project_path.name}")
        click.echo(f"")
        click.echo(f"  2. Install dependencies:")
    else:
        click.echo(f"  1. Install dependencies:")

    click.echo(f"     pip install -r requirements.txt")
    click.echo(f"")

    if with_auth:
        click.echo(f"  3. Run your app:")
        click.echo(f"     python app.py")
        click.echo(f"")
        click.echo(f"  4. Visit in browser:")
        click.echo(f"     • Home:     http://localhost:5000")
        click.echo(f"     • Register: http://localhost:5000/register")
        click.echo(f"     • Login:    http://localhost:5000/login")
        click.echo(f"")
        click.echo(f"🔐 Built-in Authentication Routes (Flask-Security-Too):")
        click.echo(f"   • /login              - User login")
        click.echo(f"   • /register           - User registration")
        click.echo(f"   • /logout             - User logout")
        click.echo(f"   • /forgot-password    - Password reset request")
        click.echo(f"   • /reset-password/<token> - Password reset confirmation")
        click.echo(f"")
        click.echo(f"🔒 Security Features:")
        click.echo(f"   ✓ Argon2 password hashing")
        click.echo(f"   ✓ Role-based access control (RBAC)")
        click.echo(f"   ✓ CSRF protection")
        click.echo(f"   ✓ Session management with remember-me")
        click.echo(f"   ✓ Login tracking")
        click.echo(f"   ✓ Account activation/deactivation")
        click.echo(f"   ✓ Password reset functionality")
    else:
        click.echo(f"  3. Run your app:")
        click.echo(f"     python app.py")
        click.echo(f"")
        click.echo(f"  4. Visit http://localhost:5000")

    click.echo(f"")
    click.echo(f"🔐 Security Notes:")
    click.echo(f"   • .env is in .gitignore - never commit secrets!")
    click.echo(f"   • .env.example shows structure without secrets")
    click.echo(f"   • Share .env.example with team, not .env")
    click.echo(f"")
    click.echo(f"📚 Documentation:")
    click.echo(f"   • See Readme.md for usage examples")
    click.echo(f"   • Check .env.example for config options")

    click.echo(f"\n{'=' * 70}\n")


@click.command()
def build():
    """🚀 FlaskMeridian Build - Interactive project setup

    Answer a few quick questions to generate your Flask project with
    optional authentication. Everything is set up and ready to go!

    Usage:
        flaskmeridian build
    """

    click.echo(f"\n{'=' * 70}")
    click.echo("🚀 FlaskMeridian Build - Interactive Project Setup")
    click.echo(f"{'=' * 70}\n")

    # ========================
    # Question 1: Location
    # ========================
    click.echo("Question 1: Where would you like to create the project?\n")
    click.echo("  1) In current directory")
    click.echo("  2) In a new subdirectory\n")

    location_choice = click.prompt("Enter your choice", type=click.Choice(['1', '2']))

    if location_choice == '1':
        # Create in current directory
        project_path = Path.cwd()

        # Check if we're already in a Flask project
        if Path('app.py').exists():
            click.echo("\n❌ Error: app.py already exists in this directory", err=True)
            return

        click.echo(f"\n✅ Will create project in current directory: {project_path.name}/\n")
    else:
        # Create in new subdirectory
        project_name = click.prompt("\nEnter project name")
        project_path = Path(project_name)

        if project_path.exists():
            click.echo(f"\n❌ Directory '{project_name}' already exists", err=True)
            return

        project_path.mkdir()
        click.echo(f"\n✅ Created project directory: {project_name}\n")

    # ========================
    # Question 2: Authentication
    # ========================
    click.echo("Question 2: Include Flask-Security-Too authentication?\n")
    click.echo("  1) No (basic Flask)")
    click.echo("  2) Yes (with login, registration, RBAC)\n")

    auth_choice = click.prompt("Enter your choice", type=click.Choice(['1', '2']))
    with_auth = auth_choice == '2'

    # ========================
    # Setup Project
    # ========================
    try:
        click.echo("\n" + "=" * 70)
        click.echo("🔨 Building your FlaskMeridian project...\n")

        # 1. Create common project structure
        _setup_project_structure(project_path)

        # 2. Create app.py (with or without auth)
        if with_auth:
            app_py.create_with_auth(project_path, 'sqlite')
        else:
            app_py.create(project_path, project_path.name)

        # 3. Create config files (.env, .env.example, .gitignore)
        _setup_config_files(project_path, with_auth)

        # 4. Add authentication if requested
        if with_auth:
            click.echo("")
            _setup_auth(project_path)

        # 5. Print success message
        _print_success_message(project_path, with_auth)

    except Exception as e:
        click.echo(f"\n❌ Error building project: {e}", err=True)
        raise


if __name__ == '__main__':
    build()