"""Requirements files generator - includes python-dotenv and optional database drivers"""
import click


def create(project_path, db_type='sqlite'):
    """Create requirements.txt with Flask dependencies, python-dotenv, and db driver

    Args:
        project_path: Path to project directory
        db_type: Database type ('sqlite' or 'postgres')
    """

    requirements_content = '''flask==3.1.3
flask-sqlalchemy==3.1.1
click==8.3.1
python-dotenv==1.0.0
'''

    # Add database driver based on selection
    if db_type == 'postgres':
        requirements_content += 'psycopg2-binary==2.9.11\n'

    with open(project_path / 'requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements_content)

    if db_type == 'postgres':
        click.echo("✅ Created requirements.txt (includes psycopg2-binary==2.9.11)")
    else:
        click.echo("✅ Created requirements.txt (SQLite - no driver needed)")