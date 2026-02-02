"""Database files generator - refactored with models/ subdirectory"""
import click


def create(db_path):
    """Create database-related files with organized structure"""

    # Create models subdirectory
    models_path = db_path / 'models'
    models_path.mkdir(exist_ok=True)

    # ========================
    # db/__init__.py
    # ========================
    db_init_content = '''"""Database module for FlaskMeridian app"""
from .database import db
from .models import BaseModel

__all__ = ['db', 'BaseModel']
'''
    with open(db_path / '__init__.py', 'w', encoding='utf-8') as f:
        f.write(db_init_content)

    # ========================
    # db/database.py
    # ========================
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

    # ========================
    # db/models/__init__.py
    # ========================
    models_init_content = '''"""Database models for FlaskMeridian app"""
from .base import BaseModel

__all__ = ['BaseModel']
'''
    with open(models_path / '__init__.py', 'w', encoding='utf-8') as f:
        f.write(models_init_content)

    # ========================
    # db/models/base.py
    # ========================
    base_model_content = '''"""Base model with common attributes"""
from ..database import db


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

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'
'''
    with open(models_path / 'base.py', 'w', encoding='utf-8') as f:
        f.write(base_model_content)

    click.echo("✅ Created db/database.py")
    click.echo("✅ Created db/models/")
    click.echo("✅ Created db/models/base.py")
    click.echo("✅ Created db/__init__.py and db/models/__init__.py")