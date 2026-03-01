"""Requirements files generator - includes python-dotenv for environment variables"""
import click


def create(project_path):
    """Create requirements.txt with Flask dependencies and python-dotenv"""

    requirements_content = '''flask==3.1.3
flask-sqlalchemy==3.1.1
click==8.3.1
python-dotenv==1.0.0
'''
    with open(project_path / 'requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements_content)

    click.echo("✅ Created requirements.txt (includes python-dotenv)")