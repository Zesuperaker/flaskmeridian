"""Auth models generator - User and Role models for Flask-Security-Too"""
import click
from pathlib import Path


def update_models(db_path):
    """Update models.py to include User and Role models"""

    models_file = db_path / 'models.py'

    new_models = '''
# ============================================================================
# AUTHENTICATION MODELS (Flask-Security-Too)
# ============================================================================

# Association table for User-Role many-to-many relationship
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(BaseModel):
    """User role for RBAC (Role-Based Access Control)"""
    __tablename__ = 'role'

    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Role {self.name}>'


class User(BaseModel):
    """User model with Flask-Security integration"""
    __tablename__ = 'user'

    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Account status
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    # User metadata
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

    def has_role(self, role_name):
        """Check if user has a specific role"""
        return any(role.name == role_name for role in self.roles)

    def get_full_name(self):
        """Get user display name"""
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.username
'''

    with open(models_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already exists
    if 'class User(BaseModel):' in content or 'class Role(BaseModel):' in content:
        click.echo("⚠️  Auth models already exist in db/models.py (skipping)")
        return

    # Add new models
    if '# Define your models here' in content:
        content = content.replace(
            '# Define your models here',
            new_models + '\n\n# Define your additional models here'
        )
    else:
        content += '\n' + new_models

    with open(models_file, 'w', encoding='utf-8') as f:
        f.write(content)

    click.echo("✅ Updated db/models.py with User and Role models")