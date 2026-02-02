"""Auth models generator - creates User and Role models in models/ subdirectory"""
import click
from pathlib import Path


def update_models(db_path):
    """Create User and Role models in db/models/ directory"""

    models_path = db_path / 'models'

    # Check if models already exist
    if (models_path / 'user.py').exists() or (models_path / 'role.py').exists():
        click.echo("⚠️  Auth models already exist in db/models/ (skipping)")
        return

    # ========================
    # db/models/role.py
    # ========================
    role_content = '''"""Role model for RBAC (Role-Based Access Control)"""
from .base import BaseModel
from ..database import db


class Role(BaseModel):
    """User role for role-based access control"""
    __tablename__ = 'role'

    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Role {self.name}>'

    def __str__(self):
        return self.name
'''
    with open(models_path / 'role.py', 'w', encoding='utf-8') as f:
        f.write(role_content)

    # ========================
    # db/models/user.py
    # ========================
    user_content = '''"""User model with Flask-Security-Too integration"""
from .base import BaseModel
from ..database import db


# Association table for User-Role many-to-many relationship
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), primary_key=True)
)


class User(BaseModel):
    """User model with authentication and role support"""
    __tablename__ = 'user'

    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)

    # Account status
    active = db.Column(db.Boolean(), default=True, index=True)
    
    # Flask-Security requirement: unique identifier per user
    fs_uniquifier = db.Column(
        db.String(255), 
        unique=True, 
        nullable=False,
        default=lambda: __import__('uuid').uuid4().hex
    )

    # User profile information
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    # Login tracking
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer, default=0)

    # Relationships
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    def __repr__(self):
        return f'<User {self.email}>'

    def __str__(self):
        return self.email

    def has_role(self, role_name):
        """Check if user has a specific role"""
        return any(role.name == role_name for role in self.roles)

    def get_full_name(self):
        """Get user display name"""
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name:
            return self.first_name
        return self.username

    def add_role(self, role):
        """Add a role to the user"""
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role):
        """Remove a role from the user"""
        if role in self.roles:
            self.roles.remove(role)
'''
    with open(models_path / 'user.py', 'w', encoding='utf-8') as f:
        f.write(user_content)

    # ========================
    # Update db/models/__init__.py
    # ========================
    _update_models_init(models_path)

    click.echo("✅ Created db/models/role.py")
    click.echo("✅ Created db/models/user.py")
    click.echo("✅ Updated db/models/__init__.py")


def _update_models_init(models_path):
    """Update models/__init__.py to export User and Role"""

    init_file = models_path / '__init__.py'

    updated_content = '''"""Database models for FlaskMeridian app"""
from .base import BaseModel
from .role import Role
from .user import User

__all__ = ['BaseModel', 'Role', 'User']
'''

    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)