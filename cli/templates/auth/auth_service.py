"""Auth service generator - business logic using Flask-Security-Too"""
import click
from pathlib import Path


def create(services_path):
    """Create auth_service.py using Flask-Security-Too's built-in functions"""

    service_content = '''"""Authentication service - business logic using Flask-Security-Too"""
from flask_security import hash_password
from werkzeug.security import check_password_hash
from db import db
from db.models import User, Role


class AuthService:
    """Service for handling authentication operations with Flask-Security-Too"""

    @staticmethod
    def create_user(email, username, password, first_name=None, last_name=None, roles=None):
        """
        Create a new user

        Args:
            email: User's email address
            username: User's username
            password: User's plaintext password (will be hashed)
            first_name: Optional first name
            last_name: Optional last name
            roles: Optional list of role names to assign

        Returns:
            User instance

        Raises:
            ValueError: If email or username already exists
        """
        # Check if user exists
        if User.query.filter_by(email=email).first():
            raise ValueError(f"Email '{email}' is already registered")

        if User.query.filter_by(username=username).first():
            raise ValueError(f"Username '{username}' is already taken")

        # Hash password using Flask-Security's hash_password
        hashed_password = hash_password(password)

        # Create user
        user = User(
            email=email,
            username=username,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            active=True
        )

        # Assign roles
        if roles:
            for role_name in roles:
                role = Role.query.filter_by(name=role_name).first()
                if role:
                    user.roles.append(role)
        else:
            # Assign default 'user' role
            user_role = Role.query.filter_by(name='user').first()
            if user_role:
                user.roles.append(user_role)

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def verify_password(user, password):
        """
        Verify user password

        Args:
            user: User instance
            password: Plaintext password to verify

        Returns:
            Boolean indicating if password is correct
        """
        return check_password_hash(user.password, password)

    @staticmethod
    def update_password(user, new_password):
        """
        Update user password

        Args:
            user: User instance
            new_password: New plaintext password

        Returns:
            Updated user instance
        """
        user.password = hash_password(new_password)
        db.session.commit()
        return user

    @staticmethod
    def track_login(user, ip_address):
        """
        Track user login information

        Args:
            user: User instance
            ip_address: IP address of the login
        """
        from datetime import datetime

        user.last_login_at = user.current_login_at
        user.last_login_ip = user.current_login_ip
        user.current_login_at = datetime.utcnow()
        user.current_login_ip = ip_address
        user.login_count = (user.login_count or 0) + 1

        db.session.commit()

    @staticmethod
    def deactivate_user(user):
        """Deactivate a user account"""
        user.active = False
        db.session.commit()
        return user

    @staticmethod
    def activate_user(user):
        """Activate a user account"""
        user.active = True
        db.session.commit()
        return user

    @staticmethod
    def add_role_to_user(user, role_name):
        """
        Add a role to a user

        Args:
            user: User instance
            role_name: Name of the role to add

        Returns:
            Updated user instance
        """
        role = Role.query.filter_by(name=role_name).first()
        if role and role not in user.roles:
            user.roles.append(role)
            db.session.commit()
        return user

    @staticmethod
    def remove_role_from_user(user, role_name):
        """
        Remove a role from a user

        Args:
            user: User instance
            role_name: Name of the role to remove

        Returns:
            Updated user instance
        """
        role = Role.query.filter_by(name=role_name).first()
        if role and role in user.roles:
            user.roles.remove(role)
            db.session.commit()
        return user

    @staticmethod
    def create_role(name, description=None):
        """
        Create a new role

        Args:
            name: Role name
            description: Optional role description

        Returns:
            Role instance
        """
        if Role.query.filter_by(name=name).first():
            raise ValueError(f"Role '{name}' already exists")

        role = Role(name=name, description=description)
        db.session.add(role)
        db.session.commit()

        return role

    @staticmethod
    def initialize_default_roles():
        """Create default roles if they don't exist"""
        default_roles = [
            ('admin', 'Administrator - full system access'),
            ('user', 'Regular user'),
            ('moderator', 'Content moderator'),
        ]

        for name, description in default_roles:
            if not Role.query.filter_by(name=name).first():
                AuthService.create_role(name, description)
'''

    service_file = services_path / 'auth_service.py'
    with open(service_file, 'w', encoding='utf-8') as f:
        f.write(service_content)

    click.echo("✅ Created services/auth_service.py with authentication business logic")