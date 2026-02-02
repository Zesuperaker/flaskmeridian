"""HTML templates generator (base.html and index.html)"""
import click


def create_base(templates_path):
    """Create base.html template"""
    base_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask App{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            background-color: #2c3e50;
            color: white;
            padding: 1rem 0;
            margin-bottom: 2rem;
        }

        header h1 {
            margin: 0;
        }

        main {
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        footer {
            text-align: center;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #ddd;
            color: #666;
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <div class="container">
            <h1>{% block header_title %}Flask Application{% endblock %}</h1>
        </div>
    </header>

    <main class="container">
        {% block content %}
        <p>Welcome to your Flask application built with FlaskMeridian!</p>
        {% endblock %}
    </main>

    <footer class="container">
        <p>&copy; 2024 Your Flask App. Built with FlaskMeridian.</p>
    </footer>

    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
'''
    with open(templates_path / 'base.html', 'w') as f:
        f.write(base_html)
    click.echo("✅ Created templates/base.html")


def create_index(templates_path):
    """Create index.html template"""
    index_html = '''{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block header_title %}Welcome to FlaskMeridian{% endblock %}

{% block content %}
<h2>Your Flask Application is Running!</h2>
<p>Your Flask application has been successfully set up with FlaskMeridian.</p>

<h3>Next Steps:</h3>
<ul>
    <li>Define your models in <code>db/models.py</code></li>
    <li>Create route blueprints in <code>routes/</code></li>
    <li>Add business logic in <code>services/</code></li>
    <li>Style your app in <code>static/css/style.css</code></li>
    <li>Add interactivity in <code>static/js/script.js</code></li>
</ul>

<p><strong>Happy building! 🚀</strong></p>
{% endblock %}
'''
    with open(templates_path / 'index.html', 'w') as f:
        f.write(index_html)
    click.echo("✅ Created templates/index.html")