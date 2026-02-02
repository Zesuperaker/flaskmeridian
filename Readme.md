# FlaskMeridian

A fast and efficient CLI tool for setting up Flask applications with optional authentication.

## Installation

```bash
pip install git+https://github.com/Zesuperaker/flaskmeridian.git
```

Or with pipx:

```bash
pipx install git+https://github.com/Zesuperaker/flaskmeridian.git
```

## Usage

### Quick Start - Initialize in Current Directory (Recommended)

```bash
# Create and enter your project directory
mkdir my_app
cd my_app

# Initialize FlaskMeridian project
flaskmeridian init

# Install dependencies
pip install -r requirements.txt

# Run your app
python app.py
```

### With Authentication

```bash
mkdir my_app
cd my_app

# Initialize with Flask-Security-Too authentication
flaskmeridian init --with-auth

# Install dependencies
pip install -r requirements.txt

# Update app.py secrets:
# - Change SECRET_KEY
# - Change SECURITY_PASSWORD_SALT

# Run your app
python app.py
```

### Alternative - Create with Subdirectory

```bash
flaskmeridian create my_project
cd my_project
pip install -r requirements.txt
python app.py
```

Or with authentication:

```bash
flaskmeridian create my_project
cd my_project
flaskmeridian auth
pip install -r requirements.txt
python app.py
```

## Project Structure

```
my_app/
├── templates/
│   ├── base.html
│   ├── index.html
│   └── auth/                (if --with-auth used)
│       ├── login.html
│       ├── signup.html
│       └── profile.html
├── static/
│   ├── css/style.css
│   └── js/script.js
├── routes/
│   ├── __init__.py
│   ├── main.py
│   └── auth.py             (if --with-auth used)
├── services/
│   ├── __init__.py
│   └── auth_service.py     (if --with-auth used)
├── db/
│   ├── __init__.py
│   ├── database.py
│   └── models/
│       ├── __init__.py
│       ├── base.py
│       ├── user.py         (if --with-auth used)
│       └── role.py         (if --with-auth used)
├── app.py
└── requirements.txt
```

## Using Auth

Protect routes:

```python
from flask_security import auth_required

@app.route('/dashboard')
@auth_required()
def dashboard():
    return 'Protected page'
```

Check roles:

```python
if current_user.has_role('admin'):
    # admin only code
```

Access user info:

```python
from flask_security import current_user

@app.route('/profile')
@auth_required()
def profile():
    return f'Hello {current_user.email}'
```

## Commands

### `flaskmeridian init [OPTIONS]`

Initialize a Flask project in the current directory.

**Options:**
- `--with-auth`: Include Flask-Security-Too authentication system

**Usage:**
```bash
flaskmeridian init                 # Basic project
flaskmeridian init --with-auth     # With authentication
```

### `flaskmeridian create PROJECT_NAME`

Create a Flask project in a new subdirectory (legacy command).

**Usage:**
```bash
flaskmeridian create my_project
cd my_project
```

### `flaskmeridian auth`

Add Flask-Security-Too authentication to an existing project created with `create`.

**Options:**
- `--db-type`: Database type - `sqlite` (default) or `postgres`

**Usage:**
```bash
flaskmeridian auth                        # SQLite
flaskmeridian auth --db-type=postgres     # PostgreSQL
```

## License

MIT

## Repository

https://github.com/Zesuperaker/flaskmeridian