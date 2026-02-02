"""Create command for generating new Flask projects"""
import click
from pathlib import Path
from cli.templates import (
    html_templates,
    static_files,
    db_files,
    routes_files,
    services_files,
    app_py,
)


@click.command()
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

        # Create main app file
        app_py.create(project_path, project_name)

        click.echo(f"\n✨ FlaskMeridian project '{project_name}' created successfully!")
        click.echo(f"📁 Project structure:\n")
        click.echo(f"  {project_name}/")
        click.echo(f"  ├── templates/")
        click.echo(f"  │   ├── base.html")
        click.echo(f"  │   └── index.html")
        click.echo(f"  ├── static/")
        click.echo(f"  │   ├── css/")
        click.echo(f"  │   │   └── style.css")
        click.echo(f"  │   └── js/")
        click.echo(f"  │       └── script.js")
        click.echo(f"  ├── services/")
        click.echo(f"  │   └── __init__.py")
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
        raise