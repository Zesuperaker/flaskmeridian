"""Database files generator"""
import click


def create(db_path):
    """Create database-related files"""

    # __init__.py
    init_content = '''"""Database module for FlaskMeridian app"""
from .database import db
from .models import *

__all__ = ['db']
'''
    with open(db_path / '__init__.py', 'w', encoding='utf-8') as f:
        f.write(init_content)

    # database.py
    database_content = '''"""Database initialization and configuration"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)

    with app.app_context():
        db.create_all()
'''
    with open(db_path / 'database.py', 'w', encoding='utf-8') as f:
        f.write(database_content)

    # models.py
    models_content = '''"""Database models for FlaskMeridian app"""
from .database import db


class BaseModel(db.Model):
    """Base model with common attributes"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime, 
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )


# Define your models here
# Example:
# class User(BaseModel):
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
'''
    with open(db_path / 'models.py', 'w', encoding='utf-8') as f:
        f.write(models_content)

    click.echo("✅ Created db/__init__.py, db/database.py, db/models.py")