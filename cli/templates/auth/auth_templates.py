"""Auth templates generator - HTML templates for Flask-Security-Too

Flask-Security-Too Conventions:
- Templates go in templates/security/ directory
- Expected template names:
  * login_user.html
  * register_user.html
  * forgot_password.html
  * reset_password.html
  * change_password.html
- Endpoints: security.login, security.register, security.logout, etc.
- Forms provided via Jinja2 context: login_user_form, register_form, etc.
"""
import click
from pathlib import Path


def create(templates_path):
    """Create security templates directory and pages for Flask-Security-Too

    Note: Flask-Security-Too REQUIRES templates/security/ directory structure
    """

    # Flask-Security-Too REQUIRES templates/security/ directory
    security_dir = templates_path / 'security'
    security_dir.mkdir(exist_ok=True)

    # ========================
    # login_user.html
    # ========================
    login_template = '''{% extends "base.html" %}
{% from "security/macros.html" import render_form_without_hidden, render_field %}

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

    .error-list {
        list-style: none;
        padding: 0;
        margin: 0.5rem 0 0 0;
    }

    .error-list li {
        color: #922b21;
        font-size: 0.85rem;
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

        <form method="POST" action="{{ url_for('security.login') }}" novalidate>
            {{ login_user_form.hidden_tag() }}

            <!-- Email Field -->
            <div class="form-group">
                {{ login_user_form.email.label }}
                {{ login_user_form.email(class="form-control", placeholder="you@example.com") }}
                {% if login_user_form.email.errors %}
                    <ul class="error-list">
                    {% for error in login_user_form.email.errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                    </ul>
                {% endif %}
            </div>

            <!-- Password Field -->
            <div class="form-group">
                {{ login_user_form.password.label }}
                {{ login_user_form.password(class="form-control", placeholder="Enter your password") }}
                {% if login_user_form.password.errors %}
                    <ul class="error-list">
                    {% for error in login_user_form.password.errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                    </ul>
                {% endif %}
            </div>

            <!-- Remember Me Checkbox -->
            {% if login_user_form.remember %}
            <div class="checkbox-group">
                {{ login_user_form.remember() }}
                {{ login_user_form.remember.label }}
            </div>
            {% endif %}

            <!-- Submit Button -->
            {{ login_user_form.submit(class="btn-signin") }}
        </form>

        <div class="auth-footer">
            <p>Don't have an account? <a href="{{ url_for('security.register') }}">Create one now</a></p>
            {% if config.SECURITY_RECOVERABLE %}
            <p><a href="{{ url_for('security.forgot_password') }}">Forgot password?</a></p>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
'''

    # ========================
    # register_user.html
    # ========================
    signup_template = '''{% extends "base.html" %}
{% from "security/macros.html" import render_form_without_hidden, render_field %}

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

    .error-list {
        list-style: none;
        padding: 0;
        margin: 0.5rem 0 0 0;
    }

    .error-list li {
        color: #922b21;
        font-size: 0.85rem;
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

        <form method="POST" action="{{ url_for('security.register') }}" novalidate>
            {{ register_user_form.hidden_tag() }}

            <!-- Email Field -->
            <div class="form-group">
                {{ register_user_form.email.label }}
                {{ register_user_form.email(class="form-control", placeholder="you@example.com") }}
                {% if register_user_form.email.errors %}
                    <ul class="error-list">
                    {% for error in register_user_form.email.errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                    </ul>
                {% endif %}
            </div>

            <!-- Password Field -->
            <div class="form-group">
                {{ register_user_form.password.label }}
                {{ register_user_form.password(class="form-control", placeholder="Minimum 8 characters") }}
                <div class="password-note">Must be at least 8 characters</div>
                {% if register_user_form.password.errors %}
                    <ul class="error-list">
                    {% for error in register_user_form.password.errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                    </ul>
                {% endif %}
            </div>

            <!-- Password Confirmation Field -->
            <div class="form-group">
                {{ register_user_form.password_confirm.label }}
                {{ register_user_form.password_confirm(class="form-control", placeholder="Re-enter your password") }}
                {% if register_user_form.password_confirm.errors %}
                    <ul class="error-list">
                    {% for error in register_user_form.password_confirm.errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                    </ul>
                {% endif %}
            </div>

            <!-- Submit Button -->
            {{ register_user_form.submit(class="btn-signup", value="Create Account") }}
        </form>

        <div class="auth-footer">
            <p>Already have an account? <a href="{{ url_for('security.login') }}">Sign in here</a></p>
        </div>
    </div>
</div>
{% endblock %}
'''

    # ========================
    # macros.html - Flask-Security macros
    # ========================
    macros_template = '''{% macro render_form_without_hidden(form, action=None) -%}
<form method="POST"{% if action %} action="{{ action }}"{% endif %}>
    {% for field in form %}
        {% if field.widget.input_type != 'hidden' %}
            {{ render_field(field) }}
        {% else %}
            {{ field() }}
        {% endif %}
    {% endfor %}
</form>
{%- endmacro %}

{% macro render_field(field) -%}
<div class="form-group">
    {% if field.type != 'BooleanField' %}
        {{ field.label }}
    {% endif %}
    {% if field.type == 'BooleanField' %}
        <div class="checkbox">
            {{ field() }}
            {{ field.label }}
        </div>
    {% else %}
        {{ field(class="form-control") }}
    {% endif %}
    {% if field.errors %}
        <ul class="error-list">
        {%- for error in field.errors %}
            <li>{{ error }}</li>
        {%- endfor %}
        </ul>
    {% endif %}
</div>
{%- endmacro %}
'''

    with open(security_dir / 'login_user.html', 'w', encoding='utf-8') as f:
        f.write(login_template)

    with open(security_dir / 'register_user.html', 'w', encoding='utf-8') as f:
        f.write(signup_template)

    with open(security_dir / 'macros.html', 'w', encoding='utf-8') as f:
        f.write(macros_template)

    click.echo("✅ Created templates/security/ with Flask-Security-Too templates")
    click.echo("   - login_user.html")
    click.echo("   - register_user.html")
    click.echo("   - macros.html")