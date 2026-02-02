"""Auth templates generator - HTML templates for login, signup, profile"""
import click
from pathlib import Path


def create(templates_path):
    """Create auth templates directory and pages"""

    auth_dir = templates_path / 'auth'
    auth_dir.mkdir(exist_ok=True)

    # Login template
    login_template = '''{% extends "base.html" %}

{% block title %}Sign In{% endblock %}
{% block header_title %}Sign In to Your Account{% endblock %}

{% block extra_css %}
<style>
    .auth-container {
        max-width: 400px;
        margin: 3rem auto;
    }

    .auth-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid #f0f0f0;
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
        color: #2c3e50;
        font-size: 0.95rem;
    }

    .form-group input {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 1rem;
        transition: all 0.2s;
        box-sizing: border-box;
    }

    .form-group input:focus {
        outline: none;
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }

    .checkbox-group {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    }

    .checkbox-group input[type="checkbox"] {
        width: auto;
        margin: 0;
    }

    .checkbox-group label {
        margin: 0;
        font-weight: normal;
        font-size: 0.9rem;
    }

    .btn-signin {
        width: 100%;
        padding: 0.85rem;
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }

    .btn-signin:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
    }

    .auth-footer {
        text-align: center;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #f0f0f0;
    }

    .auth-footer p {
        margin: 0;
        color: #666;
        font-size: 0.95rem;
    }

    .auth-footer a {
        color: #3498db;
        text-decoration: none;
        font-weight: 600;
    }

    .auth-footer a:hover {
        text-decoration: underline;
    }

    .alert {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
    }

    .alert-error {
        background-color: #fadbd8;
        border: 1px solid #f5b7b1;
        color: #922b21;
    }

    .alert-success {
        background-color: #d5f4e6;
        border: 1px solid #a9dfbf;
        color: #145a32;
    }
</style>
{% endblock %}

{% block content %}
<div class="auth-container">
    <div class="auth-card">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form method="POST">
            <div class="form-group">
                <label for="email">Email Address</label>
                <input type="email" id="email" name="email" placeholder="you@example.com" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter your password" required>
            </div>

            <div class="checkbox-group">
                <input type="checkbox" id="remember_me" name="remember_me">
                <label for="remember_me">Remember me for 30 days</label>
            </div>

            <button type="submit" class="btn-signin">Sign In</button>
        </form>

        <div class="auth-footer">
            <p>Don't have an account? <a href="{{ url_for('auth.signup') }}">Create one now</a></p>
        </div>
    </div>
</div>
{% endblock %}
'''

    # Signup template
    signup_template = '''{% extends "base.html" %}

{% block title %}Create Account{% endblock %}
{% block header_title %}Create Your Account{% endblock %}

{% block extra_css %}
<style>
    .auth-container {
        max-width: 450px;
        margin: 2rem auto;
    }

    .auth-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid #f0f0f0;
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
        color: #2c3e50;
        font-size: 0.95rem;
    }

    .form-group input {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 1rem;
        transition: all 0.2s;
        box-sizing: border-box;
    }

    .form-group input:focus {
        outline: none;
        border-color: #27ae60;
        box-shadow: 0 0 0 3px rgba(39, 174, 96, 0.1);
    }

    .password-note {
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.3rem;
    }

    .btn-signup {
        width: 100%;
        padding: 0.85rem;
        background-color: #27ae60;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }

    .btn-signup:hover {
        background-color: #229954;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
    }

    .auth-footer {
        text-align: center;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #f0f0f0;
    }

    .auth-footer p {
        margin: 0;
        color: #666;
        font-size: 0.95rem;
    }

    .auth-footer a {
        color: #3498db;
        text-decoration: none;
        font-weight: 600;
    }

    .auth-footer a:hover {
        text-decoration: underline;
    }

    .alert {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
    }

    .alert-error {
        background-color: #fadbd8;
        border: 1px solid #f5b7b1;
        color: #922b21;
    }

    .alert-success {
        background-color: #d5f4e6;
        border: 1px solid #a9dfbf;
        color: #145a32;
    }
</style>
{% endblock %}

{% block content %}
<div class="auth-container">
    <div class="auth-card">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form method="POST">
            <div class="form-group">
                <label for="email">Email Address</label>
                <input type="email" id="email" name="email" placeholder="you@example.com" required>
            </div>

            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" placeholder="Choose a username" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Minimum 8 characters" required>
                <div class="password-note">Must be at least 8 characters</div>
            </div>

            <div class="form-group">
                <label for="confirm_password">Confirm Password</label>
                <input type="password" id="confirm_password" name="confirm_password" placeholder="Re-enter your password" required>
            </div>

            <button type="submit" class="btn-signup">Create Account</button>
        </form>

        <div class="auth-footer">
            <p>Already have an account? <a href="{{ url_for('auth.login') }}">Sign in here</a></p>
        </div>
    </div>
</div>
{% endblock %}
'''

    # Profile template
    profile_template = '''{% extends "base.html" %}

{% block title %}My Profile{% endblock %}
{% block header_title %}My Profile{% endblock %}

{% block extra_css %}
<style>
    .profile-container {
        max-width: 600px;
        margin: 2rem auto;
    }

    .profile-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid #f0f0f0;
        margin-bottom: 2rem;
    }

    .profile-header {
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .user-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3498db, #2980b9);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }

    .user-info h2 {
        margin: 0 0 0.5rem 0;
        color: #2c3e50;
    }

    .user-email {
        color: #666;
        font-size: 0.95rem;
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
        color: #2c3e50;
        font-size: 0.95rem;
    }

    .form-group input {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 1rem;
        box-sizing: border-box;
    }

    .form-group input:focus {
        outline: none;
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }

    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }

    .btn-update {
        padding: 0.85rem 1.5rem;
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }

    .btn-update:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
    }

    .btn-logout {
        padding: 0.85rem 1.5rem;
        background-color: #e74c3c;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        margin-left: 1rem;
    }

    .btn-logout:hover {
        background-color: #c0392b;
    }

    .button-group {
        display: flex;
        gap: 1rem;
        margin-top: 2rem;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .stat-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
    }

    .stat-label {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stat-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 0.5rem;
    }

    .alert {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
    }

    .alert-success {
        background-color: #d5f4e6;
        border: 1px solid #a9dfbf;
        color: #145a32;
    }
</style>
{% endblock %}

{% block content %}
<div class="profile-container">
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <div class="profile-card">
        <div class="profile-header">
            <div class="user-avatar">
                {{ current_user.username[0].upper() }}
            </div>
            <div class="user-info">
                <h2>{{ current_user.get_full_name() or current_user.username }}</h2>
                <div class="user-email">{{ current_user.email }}</div>
            </div>
        </div>

        <form method="POST" action="{{ url_for('auth.update_profile') }}">
            <div class="form-row">
                <div class="form-group">
                    <label for="first_name">First Name</label>
                    <input type="text" id="first_name" name="first_name" value="{{ current_user.first_name or '' }}">
                </div>
                <div class="form-group">
                    <label for="last_name">Last Name</label>
                    <input type="text" id="last_name" name="last_name" value="{{ current_user.last_name or '' }}">
                </div>
            </div>

            <div class="button-group">
                <button type="submit" class="btn-update">Update Profile</button>
                <a href="{{ url_for('auth.logout') }}" class="btn-logout">Logout</a>
            </div>
        </form>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Member Since</div>
                <div class="stat-value">{{ current_user.created_at.strftime('%b %Y') }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Login Count</div>
                <div class="stat-value">{{ current_user.login_count or 0 }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Last Login</div>
                <div class="stat-value">{{ (current_user.current_login_at.strftime('%b %d') if current_user.current_login_at else 'N/A') }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Roles</div>
                <div class="stat-value">{{ current_user.roles|length }}</div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

    with open(auth_dir / 'login.html', 'w', encoding='utf-8') as f:
        f.write(login_template)

    with open(auth_dir / 'signup.html', 'w', encoding='utf-8') as f:
        f.write(signup_template)

    with open(auth_dir / 'profile.html', 'w', encoding='utf-8') as f:
        f.write(profile_template)

    click.echo("✅ Created templates/auth/ with login, signup, and profile templates")