"""Gitignore generator - creates .gitignore with security best practices and Docker ignores"""
import click


def create(project_path):
    """Create .gitignore file with standard Python, Flask, and Docker ignores"""

    gitignore_content = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache
.flask_env

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.env.local
.env.*.local
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Project-specific
test_app/
*.db
app.db
instance/

# Docker
.docker/
docker-compose.local.yml
docker-compose.prod.yml
.env.docker
'''

    gitignore_file = project_path / '.gitignore'
    with open(gitignore_file, 'w', encoding='utf-8') as f:
        f.write(gitignore_content)

    click.echo("✅ Created .gitignore with .env and sensitive files protected")
    click.echo("   ✓ Secrets (.env) protected")
    click.echo("   ✓ Virtual environments ignored")
    click.echo("   ✓ IDE files ignored")
    click.echo("   ✓ Docker build artifacts ignored")