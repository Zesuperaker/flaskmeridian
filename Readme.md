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

### Create a new Flask project

```bash
flaskmeridian create my_project
cd my_project
```

This creates a project with directory structure and boilerplate code.

### Add authentication (optional)

```bash
flaskmeridian auth
```

Or for PostgreSQL:

```bash
flaskmeridian auth --db-type=postgres
```

This adds:
- User registration and login pages
- Password hashing with passlib
- User profile management
- Role-based access control
- Login tracking

## Quick Start

```bash
# 1. Create project
flaskmeridian create my_app
cd my_app

# 2. Add auth (optional)
flaskmeridian auth

# 3. Install dependencies
pip install -r requirements.txt

# 4. Update secrets in app.py
# Change SECRET_KEY and SECURITY_PASSWORD_SALT

# 5. Run
python app.py

# 6. Visit http://localhost:5000
```

## Project Structure

```
my_project/
├── templates/
│   ├── base.html
│   └── auth/           (if auth added)
│       ├── login.html
│       ├── signup.html
│       └── profile.html
├── static/
│   ├── css/style.css
│   └── js/script.js
├── routes/
│   ├── main.py
│   └── auth.py         (if auth added)
├── services/
│   └── auth_service.py (if auth added)
├── db/
│   ├── models.py
│   ├── database.py
│   └── __init__.py
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

## License

MIT

## Repository

https://github.com/Zesuperaker/flaskmeridian