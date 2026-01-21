# Development Setup Guide

Step-by-step guide for setting up the TechAdvisor development environment.

---

## Prerequisites

| Software | Version | Download |
|----------|---------|----------|
| Python | 3.12+ | [python.org](https://www.python.org/downloads/) |
| MySQL | 8.0+ | [mysql.com](https://dev.mysql.com/downloads/mysql/) |
| Git | Latest | [git-scm.com](https://git-scm.com/) |

---

## Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd TechAdvisor

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env with your database credentials

# 6. Create database
mysql -u root -p -e "CREATE DATABASE techadvisor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 7. Initialize RBAC
python init_rbac.py

# 8. Seed database
python seed_database.py

# 9. Run application
python run.py
```

Application runs at: **http://127.0.0.1:5001**

---

## Environment Configuration

Create `.env` file from template:

```env
# Flask
SECRET_KEY=your-secret-key-change-in-production-12345
FLASK_APP=run.py
FLASK_ENV=development
DEBUG=True

# Database
DB_HOST=localhost
DB_PORT=3307
DB_NAME=techadvisor
DB_USER=root
DB_PASSWORD=YOUR_PASSWORD
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3307/techadvisor

# Security
WTF_CSRF_ENABLED=True
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# File Upload
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=app/static/uploads
ITEMS_PER_PAGE=20

# Admin
ADMIN_EMAIL=admin@techadvisor.local
```

### Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Database Setup

### Option 1: Using Schema File

```bash
mysql -u root -p techadvisor < docs/database_schema.sql
```

### Option 2: Using Flask-Migrate

```bash
flask db upgrade
```

### Seeding Data

Run seeders in order:

```bash
# 1. Initialize roles and permissions
python init_rbac.py

# 2. Core data (users, categories, brands, sample products)
python seed_database.py

# 3. Extended product catalog (optional)
python seed_products.py

# 4. Recommendation rules
python seed_rules.py
python seed_comprehensive_rules.py
```

---

## Project Structure

```
TechAdvisor/
├── app/                    # Main application
│   ├── __init__.py         # App factory
│   ├── models/             # SQLAlchemy models
│   ├── routes/             # Flask blueprints
│   ├── services/           # Business logic
│   ├── forms/              # WTForms
│   ├── templates/          # Jinja2 templates
│   ├── static/             # CSS, JS, images
│   └── utils/              # Helpers
├── docs/                   # Documentation
│   ├── database_schema.sql
│   └── technical/          # Technical docs
├── migrations/             # Alembic migrations
├── tests/                  # Pytest test suite
├── config.py               # Configuration classes
├── run.py                  # Entry point
├── requirements.txt        # Dependencies
└── *.py                    # Seeding scripts
```

---

## Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_models.py

# With verbose output
pytest -v

# With coverage report
pytest --cov=app --cov-report=html

# By marker
pytest -m unit
pytest -m integration
```

Coverage report: `htmlcov/index.html`

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Edit code
- Add tests
- Update documentation

### 3. Run Tests

```bash
pytest
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: description of changes"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

---

## Common Tasks

### Add New Model

1. Create model in `app/models/`
2. Import in `app/models/__init__.py`
3. Create migration: `flask db migrate -m "Add new model"`
4. Apply: `flask db upgrade`

### Add New Route

1. Create/edit blueprint in `app/routes/`
2. Register blueprint in `app/__init__.py` (if new)
3. Add template in `app/templates/`
4. Add form in `app/forms/` (if needed)

### Add New Permission

1. Add to `init_rbac.py` permissions list
2. Re-run: `python init_rbac.py`
3. Use decorator: `@permission_required('new.permission')`

---

## Debugging

### Enable SQL Logging

In `config.py`:
```python
SQLALCHEMY_ECHO = True
```

### Flask Debug Mode

In `.env`:
```env
DEBUG=True
FLASK_ENV=development
```

### Interactive Shell

```bash
flask shell
>>> from app.models.product import Product
>>> Product.query.all()
```

---

## IDE Setup

### VS Code

Recommended extensions:
- Python
- Pylance
- Flask Snippets
- Jinja2 Snippet Kit

### PyCharm

1. Set Python interpreter to `venv/`
2. Enable Flask server configuration
3. Configure pytest as test runner

---

## Troubleshooting

### Port Already in Use

Edit `run.py` to change port:
```python
app.run(host='0.0.0.0', port=5002)
```

Or kill the process:
```bash
# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :5001
kill -9 <PID>
```

### Database Connection Failed

1. Check MySQL is running
2. Verify credentials in `.env`
3. Ensure database exists
4. Check port number (3306 default, 3307 for XAMPP)

### Module Not Found

```bash
# Ensure venv is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### CSRF Token Missing

Ensure forms include:
```html
{{ form.csrf_token }}
```

---

## Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Staff | staff | staff123 |

> ⚠️ Change these in production!
