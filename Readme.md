# FlaskMeridian

A fast and efficient CLI tool for setting up and automating Flask applications.

## Installation

Install FlaskMeridian directly from GitHub:

```bash
pip install git+https://github.com/Zesuperaker/flaskmeridian.git
```

Or if you prefer to use `pipx` for CLI tools:

```bash
pipx install git+https://github.com/Zesuperaker/flaskmeridian.git
```

## Usage

### Create a new Flask project

```bash
flaskmeridian create my_project
```

This creates a new Flask project with the following structure:

```
my_project/
├── templates/
│   └── base.html          # Base HTML template with styling
├── static/
│   ├── css/
│   │   └── style.css      # Main stylesheet with CSS variables
│   └── js/
│       └── script.js      # Main JavaScript file
├── services/              # Business logic and reusable services
├── routes/                # Application routes/blueprints
│   ├── __init__.py
│   └── main.py           # Example main routes
├── db/                    # Database configuration and models
│   ├── __init__.py
│   ├── database.py       # SQLAlchemy initialization
│   └── models.py         # Database models
└── app.py                # Main application file
```

## Project Structure

### templates/
Houses all Jinja2 HTML templates. The `base.html` provides a responsive base layout that can be extended by other templates and includes references to static CSS and JS files.

### static/
Contains all static assets (CSS, JavaScript, images, etc.).
- **css/** - Stylesheets with pre-defined CSS variables for theming
- **js/** - JavaScript files for frontend functionality

### routes/
Contains Flask blueprints organized by feature/functionality. Each route file should define a blueprint and be registered in `__init__.py`.

### services/
Business logic, database queries, and reusable functions live here. Services are called by routes to keep the separation of concerns clean.

### db/
Database initialization, SQLAlchemy configuration, and model definitions. The `BaseModel` provides common fields (id, created_at, updated_at).

## Quick Start

1. Install FlaskMeridian:
   ```bash
   pip install git+https://github.com/Zesuperaker/flaskmeridian.git
   ```

2. Create a new project:
   ```bash
   flaskmeridian create my_project
   ```

3. Navigate to your project:
   ```bash
   cd my_project
   ```

4. Install dependencies:
   ```bash
   pip install flask flask-sqlalchemy
   ```

5. Update `app.py` with your configuration

6. Define your models in `db/models.py`

7. Create route blueprints in `routes/`

8. Add styles to `static/css/style.css`

9. Add scripts to `static/js/script.js`

10. Run your app:
    ```bash
    python app.py
    ```

## License

MIT

## Repository

https://github.com/Zesuperaker/flaskmeridian