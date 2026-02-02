"""Requirements files generator"""
import click


def create(project_path):
    """Create requirements.txt with Flask dependencies"""

    requirements_content = '''flask==3.1.2
flask-sqlalchemy==3.1.1
click==8.3.1
'''
    with open(project_path / 'requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements_content)

    click.echo("✅ Created requirements.txt")