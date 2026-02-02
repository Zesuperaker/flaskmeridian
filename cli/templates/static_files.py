"""Static files (CSS and JS) generator"""
import click


def create(static_path):
    """Create static CSS and JS files"""

    # Create style.css
    css_content = '''/* Main stylesheet */
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --text-color: #333;
    --border-color: #ddd;
    --background-color: #f5f5f5;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: var(--text-color);
    background-color: var(--background-color);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* Add your custom styles here */
'''
    with open(static_path / 'css' / 'style.css', 'w') as f:
        f.write(css_content)

    # Create script.js
    js_content = '''// Main JavaScript file

document.addEventListener('DOMContentLoaded', function() {
    console.log('FlaskMeridian app loaded!');
    // Add your scripts here
});
'''
    with open(static_path / 'js' / 'script.js', 'w') as f:
        f.write(js_content)

    click.echo("✅ Created static/css/style.css and static/js/script.js")