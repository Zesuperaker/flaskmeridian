"""Services files generator"""
import click


def create(services_path):
    """Create services directory files"""

    # __init__.py
    init_content = '''"""Services module for FlaskMeridian app

Services contain business logic and are reusable across routes.
"""
'''
    with open(services_path / '__init__.py', 'w') as f:
        f.write(init_content)

    click.echo("✅ Created services/__init__.py")