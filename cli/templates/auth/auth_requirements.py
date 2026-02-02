"""Auth requirements generator - updates requirements.txt with Flask-Security-Too"""
import click
from pathlib import Path


def update(req_path):
    """Update requirements.txt with Flask-Security-Too"""

    with open(req_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already present
    if 'flask-security-too' in content.lower():
        click.echo("ℹ️  Flask-Security-Too already in requirements.txt")
        return

    # Add Flask-Security-Too
    with open(req_path, 'a', encoding='utf-8') as f:
        f.write('flask-security-too==5.7.1\n')

    click.echo("✅ Added flask-security-too==5.7.1 to requirements.txt")