"""Auth routes generator - login, signup, logout, profile"""
import click
from pathlib import Path


def create(routes_path):
    """Create auth.py with authentication routes"""

    auth_routes_content = '''"""Authentication routes for Flask-Security-Too"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from flask_security import auth_required, current_user
from db import db
from db.models import User
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        errors = []

        if not email or not username or not password:
            errors.append('All fields are required')

        if password != confirm_password:
            errors.append('Passwords do not match')

        if len(password) < 8:  # Flask-Security default minimum
            errors.append('Password must be at least 8 characters long')

        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('auth.signup'))

        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.signup'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return redirect(url_for('auth.signup'))

        try:
            # Use auth service to create user
            # Password is automatically hashed via hash_password()
            user = AuthService.create_user(
                email=email,
                username=username,
                password=password,
                roles=['user']
            )
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('auth.signup'))
        except Exception as e:
            flash(f'Error creating account: {str(e)}', 'error')
            return redirect(url_for('auth.signup'))

    return render_template('auth/signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember_me') is not None

        if not email or not password:
            flash('Email and password are required', 'error')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()

        # Verify credentials using Flask-Security's password verification
        if user and AuthService.verify_password(user, password):
            if not user.active:
                flash('Your account has been disabled', 'error')
                return redirect(url_for('auth.login'))

            # Login user using Flask-Login (via Flask-Security)
            login_user(user, remember=remember)

            # Track login
            AuthService.track_login(user, request.remote_addr)

            flash(f'Welcome back, {user.get_full_name()}!', 'success')

            # Redirect to next page or home
            next_page = request.args.get('next')
            if not next_page or not _url_has_allowed_host_and_scheme(next_page):
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@auth_required()
def logout():
    """User logout route"""
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@auth_required()
def profile():
    """User profile view"""
    return render_template('auth/profile.html', user=current_user)


@auth_bp.route('/profile/update', methods=['POST'])
@auth_required()
def update_profile():
    """Update user profile"""
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()

    try:
        current_user.first_name = first_name
        current_user.last_name = last_name
        db.session.commit()
        flash('Profile updated successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating profile: {str(e)}', 'error')

    return redirect(url_for('auth.profile'))


def _url_has_allowed_host_and_scheme(url, allowed_hosts=None):
    """Check if URL is safe for redirect"""
    if allowed_hosts is None:
        allowed_hosts = {'localhost', '127.0.0.1'}

    return not url.startswith(('http://', 'https://', '//', '\\\\'))
'''

    auth_file = routes_path / 'auth.py'
    with open(auth_file, 'w', encoding='utf-8') as f:
        f.write(auth_routes_content)

    click.echo("✅ Created routes/auth.py with authentication routes")