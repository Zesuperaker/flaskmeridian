# FlaskMeridian - Streamlined Version

A fast and elegant CLI tool for setting up Flask applications with optional authentication.

## Installation

```bash
pip install git+https://github.com/Zesuperaker/flaskmeridian.git
```

Or with pipx:

```bash
pipx install git+https://github.com/Zesuperaker/flaskmeridian.git
```

Uninstall with

```bash
pip uninstall flaskmeridian
```


## Quick Start

Simply run the interactive builder:

```bash
flaskmeridian build
```

Then answer two simple questions:

1. **Where to create the project?**
   - In current directory
   - In a new subdirectory

2. **Include authentication?**
   - No (basic Flask)
   - Yes (Flask-Security-Too)

Everything else is automatic!

## Example Usage

### Option 1: Create in Current Directory (No Auth)

```bash
mkdir my_app
cd my_app
flaskmeridian build

# Select: 1) Current directory
#         1) No auth

pip install -r requirements.txt
python app.py
# Visit http://localhost:5000
```

### Option 2: Create in Subdirectory (With Auth)

```bash
flaskmeridian build

# Select: 2) New subdirectory
#         Enter: my_secure_app
#         2) Yes auth

cd my_secure_app
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000/register
```

## Project Structure

```
my_app/
├── templates/
│   ├── base.html
│   ├── index.html
│   └── security/                (if auth enabled)
│       ├── login_user.html
│       └── register_user.html
├── static/
│   ├── css/style.css
│   └── js/script.js
├── routes/
│   ├── __init__.py
│   └── main.py
├── services/
│   ├── __init__.py
│   └── auth_service.py         (if auth enabled)
├── db/
│   ├── __init__.py
│   ├── database.py
│   └── models/
│       ├── __init__.py
│       ├── base.py
│       ├── user.py             (if auth enabled)
│       └── role.py             (if auth enabled)
├── app.py
├── requirements.txt
├── .env                        (secrets - protected by .gitignore)
├── .env.example                (documentation template)
└── .gitignore
```

## Features

### Without Authentication

- Clean Flask project structure
- Database setup (SQLAlchemy)
- Static files (CSS/JS)
- HTML templating
- Route organization

### With Authentication (Flask-Security-Too)

All of the above, plus:

- **User Registration & Login**
- **Role-Based Access Control (RBAC)**
- **Argon2 Password Hashing** (modern, secure)
- **Login Tracking**
- **Account Activation/Deactivation**
- **Password Reset**
- **CSRF Protection**
- **Session Management**

### Built-in Auth Routes (Flask-Security-Too)

When you enable authentication, these routes are automatically available:

```
GET/POST /login              - Login page & handler
GET/POST /register           - Registration page & handler
GET      /logout             - Logout handler
GET/POST /forgot-password    - Password reset request
GET/POST /reset-password/<token> - Password reset form
```

## Environment Variables

All secrets are managed via `.env` file (protected by `.gitignore`):

```bash
SECRET_KEY=generated-secure-key
SECURITY_PASSWORD_SALT=generated-secure-salt
DATABASE_URL=sqlite:///app.db
FLASK_ENV=development
FLASK_DEBUG=True
```

**Important**: Never commit `.env` to version control! Share `.env.example` with your team instead.

## Using Authentication

### Protect Routes

```python
from flask_security import auth_required

@app.route('/dashboard')
@auth_required()
def dashboard():
    return 'Protected page'
```

### Check Roles

```python
from flask_security import current_user

@app.route('/admin')
@auth_required()
def admin_panel():
    if current_user.has_role('admin'):
        return 'Admin panel'
    return 'Access denied', 403
```

### Access User Info

```python
from flask_security import current_user

@app.route('/profile')
@auth_required()
def profile():
    return f'Hello {current_user.email}!'
```

## Security

✅ **Secrets Management**
- Secrets stored in `.env` (not in code)
- `.env` is in `.gitignore` (never committed)
- Share `.env.example` for documentation

✅ **Password Security**
- Argon2 hashing (modern standard)
- Verified by Flask-Security-Too
- Password salt configured in `.env`

✅ **Session Security**
- CSRF protection (automatic)
- Secure session management
- Remember-me functionality
- Login tracking

## Development Workflow

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Flask shell to create users**
   ```bash
   flask shell
   >>> from db import db
   >>> from db.models import User, Role
   >>> from flask_security import hash_password
   >>> 
   >>> # Create admin role
   >>> admin_role = Role(name='admin', description='Admin')
   >>> db.session.add(admin_role)
   >>> 
   >>> # Create admin user
   >>> admin = User(
   ...     email='admin@example.com',
   ...     username='admin',
   ...     password=hash_password('secure_password'),
   ...     active=True
   ... )
   >>> admin.roles.append(admin_role)
   >>> db.session.add(admin)
   >>> db.session.commit()
   ```

3. **Run development server**
   ```bash
   python app.py
   ```

4. **Test authentication**
   ```
   Register:  http://localhost:5000/register
   Login:     http://localhost:5000/login
   Profile:   http://localhost:5000/profile
   ```

## Customization

### Add Custom Models

Create files in `db/models/`:

```python
# db/models/product.py
from .base import BaseModel
from db.database import db

class Product(BaseModel):
    __tablename__ = 'product'
    
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
```

### Add Routes

Create blueprints in `routes/`:

```python
# routes/api.py
from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/products')
def get_products():
    return jsonify([])
```

Register in `app.py`:

```python
from routes.api import api_bp
app.register_blueprint(api_bp)
```

### Add Business Logic

Create services in `services/`:

```python
# services/product_service.py
from db import db
from db.models import Product

class ProductService:
    @staticmethod
    def create_product(name, price, description):
        product = Product(name=name, price=price, description=description)
        db.session.add(product)
        db.session.commit()
        return product
```

## License

MIT - See LICENSE file

## Repository

https://github.com/Zesuperaker/flaskmeridian
