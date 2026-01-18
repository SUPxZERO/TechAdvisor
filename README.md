# TechAdvisor Expert System

A web-based rule-based expert system that helps users find the perfect smartphone or laptop based on their needs, budget, and preferences. Using forward-chaining inference engine and Flask web framework, TechAdvisor provides intelligent product recommendations through an interactive questionnaire interface.

## Table of Contents
- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Database Setup](#database-setup)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Available Routes](#available-routes)

## Project Overview

**Duration**: 12 Weeks (6 Sprints × 2 Weeks)  
**Team Size**: 3 Members  
**Methodology**: Agile (Iterative Model)

TechAdvisor is an expert system designed to provide intelligent product recommendations using rule-based inference. Users can answer a simple questionnaire to receive personalized recommendations for smartphones or laptops, while administrators can manage products, brands, and recommendation rules through an intuitive dashboard.

## Technology Stack

- **Frontend**: HTML5, Jinja2, Tailwind CSS, Vanilla JavaScript
- **Backend**: Python 3.12, Flask 2.3.3, SQLAlchemy ORM, WTForms
- **Database**: MySQL 8.0+ (with PyMySQL driver)
- **Authentication**: Flask-Login with RBAC (Role-Based Access Control)
- **Testing**: Pytest with coverage reporting
- **Security**: CSRF Protection, Security Headers, Password Hashing
- **Version Control**: Git

## Features

### For End Users
- **Smart Questionnaire**: Answer simple questions about preferences and needs
- **Intelligent Recommendations**: Get top 3 personalized product suggestions with explanations
- **Product Comparison**: 
  - Compare 2 products side-by-side with pros and cons analysis
  - Compare up to 4 products for specifications
- **No Registration Required**: Instant access without login
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### For Admins & Staff
- **Product Management**: Full CRUD operations
  - Add/edit/delete products, brands, and categories
  - Manage product specifications and details
- **Rule Engine Management**: Create and modify recommendation rules without coding
  - Define rules with conditions and actions
  - Test rules before deployment
- **Admin Dashboard**: 
  - View system statistics and analytics
  - Monitor user activity
  - Manage user accounts
- **Role-Based Access Control**: Granular permissions for Admin and Staff roles
- **Audit Trails**: Track all system changes and modifications

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.12** or higher ([Download](https://www.python.org/downloads/))
- **MySQL 8.0** or higher ([Download](https://dev.mysql.com/downloads/mysql/))
- **Git** ([Download](https://git-scm.com/))
- **pip** (included with Python)

### System Requirements
- **RAM**: 2 GB minimum
- **Disk Space**: 500 MB
- **OS**: Windows, macOS, or Linux

## Installation & Setup

### Step 1: Clone or Download the Repository

```bash
# Clone using Git
git clone <repository-url>
cd TechAdvisor

# OR download and extract the ZIP file manually
```

### Step 2: Create Virtual Environment

A virtual environment isolates project dependencies from your system Python.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal after activation.

### Step 3: Download & Install Requirements

All project dependencies are listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

**What gets installed:**
- Flask & Flask extensions (SQLAlchemy, Migrate, Login, WTF, CSRF)
- Database driver (PyMySQL)
- Security libraries (cryptography, email-validator)
- Testing framework (Pytest)
- Environment variable loader (python-dotenv)

## Configuration

### Step 1: Create .env File

The project uses environment variables for configuration:

```bash
# Copy the example configuration file
cp .env.example .env
```

### Step 2: Edit .env with Your Settings

Open `.env` in your text editor and configure the following:

#### Flask Configuration
```env
SECRET_KEY=your-secret-key-change-in-production-12345
FLASK_APP=run.py
FLASK_ENV=development
DEBUG=True
```

**Note**: For production, use a strong random secret key (e.g., from `secrets` module).

#### Database Configuration
```env
DB_HOST=localhost          # Your MySQL server host
DB_PORT=3307              # Default MySQL port (3306 is standard, 3307 if MySQL uses custom port)
DB_NAME=techadvisor       # Database name (will be created)
DB_USER=root              # MySQL username
DB_PASSWORD=ROOT          # MySQL password
DATABASE_URL=mysql+pymysql://root:ROOT@localhost:3307/techadvisor
```

#### Security Settings (Development vs Production)
```env
# Development (as shown)
WTF_CSRF_ENABLED=True
SESSION_COOKIE_SECURE=False      # Set to True only in production with HTTPS
SESSION_COOKIE_HTTPONLY=True     # Prevents JavaScript access to cookies
SESSION_COOKIE_SAMESITE=Lax      # Prevents CSRF attacks

# Production (commented out - only enable with HTTPS)
# SESSION_COOKIE_SECURE=True
```

#### File Upload Settings
```env
MAX_CONTENT_LENGTH=16777216      # 16 MB max file size
UPLOAD_FOLDER=app/static/uploads
ITEMS_PER_PAGE=20                # Pagination size
```

#### Admin Contact
```env
ADMIN_EMAIL=admin@techadvisor.local
```

### Complete .env Example
See `.env.example` in the project root for all available configuration options.

## Database Setup

### Step 1: Create MySQL Database

1. Open MySQL command line or MySQL Workbench:

```bash
mysql -u root -p
```

2. Create the database:

```sql
CREATE DATABASE techadvisor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

**Why `utf8mb4`?**
- Supports emojis and special characters in product names
- Future-proof for international characters

### Step 2: Initialize Database Schema

Apply the database schema to your MySQL database:

```bash
# Using database schema file (if available)
mysql -u root -p techadvisor < docs/database_schema.sql
```

**OR** using Flask migrations:

```bash
# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

### Step 3: Seed Initial Data

Populate the database with initial data (roles, users, products, rules):

```bash
python seed_database.py
```

This script will create:
- **Roles**: Admin, Staff (RBAC framework)
- **Default Users**: 
  - Username: `admin` | Password: `admin123`
  - Username: `staff` | Password: `staff123`
- **Categories**: Smartphone, Laptop
- **Brands**: Apple, Samsung, Dell, HP, Lenovo, ASUS, etc.
- **Sample Products**: Various phones and laptops
- **Recommendation Rules**: Initial rule set for the inference engine

### Additional Seeding Scripts

```bash
# Initialize RBAC (Role-Based Access Control)
python init_rbac.py

# Seed comprehensive rules
python seed_comprehensive_rules.py

# Seed products
python seed_products.py

# Seed specific rules
python seed_rules.py
```

## Running the Application

### Method 1: Direct Python Execution (Recommended for Development)

```bash
python run.py
```

The application will start on: **http://127.0.0.1:5001**

**Output should show:**
```
 * Running on http://127.0.0.1:5001
 * Debug mode: on
```

### Method 2: Using Flask CLI

```bash
flask run
```

**Note**: Ensure `FLASK_ENV=development` is set in `.env`

### Accessing the Application

- **Home Page**: http://127.0.0.1:5001/
- **User Questionnaire**: http://127.0.0.1:5001/questionnaire
- **Admin Login**: http://127.0.0.1:5001/auth/login
- **Admin Dashboard**: http://127.0.0.1:5001/admin/dashboard (after login)

### Default Admin Credentials

```
Username: admin
Password: admin123
```

⚠️ **Change these credentials in production!**

## Project Structure

```
TechAdvisor/
├── app/                          # Main Flask application
│   ├── __init__.py              # App factory and initialization
│   ├── models/                  # Database models
│   │   ├── user.py             # User model with authentication
│   │   ├── product.py          # Product, Brand, Category models
│   │   ├── role.py             # Role model for RBAC
│   │   └── rule.py             # Rule and RuleCondition models
│   ├── routes/                  # Flask route blueprints
│   │   ├── auth.py             # Authentication routes (login, register, logout)
│   │   ├── user.py             # User-facing routes (questionnaire, recommendations)
│   │   ├── admin.py            # Admin dashboard and management routes
│   │   └── api.py              # REST API endpoints
│   ├── services/                # Business logic layer
│   │   ├── inference_engine.py # Forward-chaining inference engine
│   │   ├── recommendation_service.py  # Recommendation logic
│   │   └── comparison_service.py      # Product comparison logic
│   ├── forms/                   # WTForms for validation
│   │   ├── auth_forms.py       # Login and registration forms
│   │   ├── product_forms.py    # Product management forms
│   │   ├── rule_forms.py       # Rule creation and editing forms
│   │   ├── brand_forms.py      # Brand management forms
│   │   └── recommendation_forms.py  # Questionnaire forms
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── base.html           # Base template with navigation
│   │   ├── auth/               # Authentication templates
│   │   ├── user/               # User-facing templates
│   │   ├── admin/              # Admin dashboard templates
│   │   └── components/         # Reusable components
│   ├── static/                  # Static files
│   │   ├── css/                # Tailwind CSS stylesheets
│   │   ├── js/                 # JavaScript functionality
│   │   ├── images/             # Images and icons
│   │   └── uploads/            # User-uploaded files
│   └── utils/                   # Utility functions
│       └── decorators.py       # Custom decorators (role_required, etc.)
├── tests/                       # Test suite
│   ├── conftest.py             # Pytest configuration and fixtures
│   ├── test_models.py          # Model tests
│   ├── test_routes.py          # Route/view tests
│   ├── test_inference_engine.py # Inference engine tests
│   ├── test_recommendation_service.py  # Recommendation logic tests
│   └── test_comparison_service.py      # Comparison logic tests
├── migrations/                  # Database migration files (auto-generated)
├── docs/                        # Documentation
│   └── database_schema.sql     # Database schema definition
├── config.py                    # Configuration classes (Dev, Test, Prod)
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore patterns
├── README.md                    # This file
└── QUICKSTART.md               # Quick reference guide
```

## Testing

The project uses **Pytest** for unit and integration testing with code coverage reporting.

### Running All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_models.py
```

### Run Specific Test

```bash
pytest tests/test_models.py::TestUserModel::test_password_hashing
```

### Run Tests with Coverage Report

```bash
pytest --cov=app --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`

### Test Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

### Test Configuration

Test settings are in `pytest.ini`:
- Test discovery in `tests/` directory
- Code coverage for `app/` package
- HTML coverage report generation
- Branch coverage enabled

## Troubleshooting

### Issue 1: Port Already in Use

**Error**: `socket in a way forbidden by its access permissions` or port 5001 already in use

**Solution**:
1. Edit `run.py` and change the port:
   ```python
   app.run(host='0.0.0.0', port=5002)  # Change from 5001
   ```
2. Kill the process using the port (Windows):
   ```bash
   netstat -ano | findstr :5001
   taskkill /PID <PID> /F
   ```

### Issue 2: Database Connection Error

**Error**: `Can't connect to MySQL server at 'localhost:3307'`

**Solutions**:
1. Verify MySQL is running:
   ```bash
   mysql -u root -p
   ```
2. Check `.env` has correct credentials:
   ```env
   DB_HOST=localhost
   DB_PORT=3307
   DB_USER=root
   DB_PASSWORD=ROOT
   ```
3. Verify database exists:
   ```sql
   SHOW DATABASES;
   ```

### Issue 3: Module Not Found Errors

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
1. Ensure virtual environment is activated:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Issue 4: "TemplateNotFound" Errors

**Error**: `TemplateNotFound: base.html` or similar

**Cause**: Template files haven't been created yet (normal in early development)

**Solution**: Check that template files exist in `app/templates/` directory

### Issue 5: Secret Key Not Set

**Error**: `ValueError: SECRET_KEY must be set in production`

**Solution**: Add `SECRET_KEY` to your `.env` file:
```env
SECRET_KEY=your-very-secret-key-12345
```

Generate a secure key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Issue 6: CSRF Token Missing

**Error**: `The CSRF token is missing` when submitting forms

**Solution**: Ensure forms include CSRF token:
```html
<form method="POST">
    {{ form.csrf_token }}
    <!-- form fields -->
</form>
```

## Available Routes

### Public Routes (No Login Required)

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/questionnaire` | GET, POST | Product recommendation questionnaire |
| `/results` | GET | Display recommendation results |
| `/product/<id>` | GET | Product detail page |
| `/compare` | GET, POST | Product comparison interface |
| `/auth/login` | GET, POST | Login page |
| `/auth/register` | GET, POST | User registration |

### Admin Routes (Login Required)

| Route | Method | Description |
|-------|--------|-------------|
| `/admin/dashboard` | GET | Admin dashboard |
| `/admin/products` | GET | Product list |
| `/admin/products/new` | GET, POST | Create product |
| `/admin/products/<id>` | GET, POST, DELETE | Edit/delete product |
| `/admin/brands` | GET | Brand list |
| `/admin/brands/new` | GET, POST | Create brand |
| `/admin/rules` | GET | Rule list |
| `/admin/rules/new` | GET, POST | Create rule |
| `/admin/users` | GET | User management |

### API Routes (REST Endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/products` | GET | Get all products (JSON) |
| `/api/products/<id>` | GET | Get product details (JSON) |
| `/api/recommendations` | POST | Get recommendations (JSON) |
| `/api/comparison` | POST | Compare products (JSON) |

### Authentication Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/auth/login` | POST | Login user |
| `/auth/logout` | GET | Logout user |
| `/auth/register` | POST | Register new user |

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | Required in production | Flask session encryption key |
| `FLASK_ENV` | development | Environment mode (development/testing/production) |
| `DEBUG` | True | Enable debug mode and auto-reload |
| `DB_HOST` | localhost | MySQL server address |
| `DB_PORT` | 3307 | MySQL server port |
| `DB_NAME` | techadvisor | Database name |
| `DB_USER` | root | MySQL username |
| `DB_PASSWORD` | ROOT | MySQL password |
| `DATABASE_URL` | mysql+pymysql://... | Full database connection URL |
| `SESSION_COOKIE_SECURE` | False | HTTPS only cookies (True in production) |
| `MAX_CONTENT_LENGTH` | 16777216 | Max upload file size (bytes) |
| `UPLOAD_FOLDER` | app/static/uploads | File upload directory |
| `ITEMS_PER_PAGE` | 20 | Pagination size |
| `ADMIN_EMAIL` | admin@techadvisor.local | Admin contact email |

## Quick Reference Commands

```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python run.py

# Run tests
pytest

# Create database
mysql -u root -p < docs/database_schema.sql

# Seed database
python seed_database.py

# Check Python version
python --version

# Freeze current dependencies
pip freeze > requirements.txt
```

## Development Workflow

1. **Create a feature branch**: `git checkout -b feature/your-feature-name`
2. **Make changes** and test locally
3. **Run tests**: `pytest`
4. **Check coverage**: `pytest --cov=app`
5. **Commit changes**: `git commit -am "Description of changes"`
6. **Push to repository**: `git push origin feature/your-feature-name`
7. **Create Pull Request** on GitHub

## Performance Optimization

### Database Indexing
The models include indexes on frequently queried columns for better performance.

### Query Optimization
- Use SQLAlchemy relationship lazy loading efficiently
- Implement pagination for large result sets
- Use database-level aggregation when possible

### Caching Strategies
- Cache product catalog (changes infrequently)
- Cache rule evaluation results during sessions
- Implement HTTP caching headers for static assets

## Security Considerations

1. **Change default credentials** before deployment
2. **Use strong SECRET_KEY** (generate with `secrets` module)
3. **Enable HTTPS** in production (set `SESSION_COOKIE_SECURE=True`)
4. **Keep dependencies updated**: `pip list --outdated`
5. **Use environment variables** for sensitive data (never commit `.env`)
6. **Implement rate limiting** for login attempts
7. **Regular security audits** of dependencies

## Performance Tips

- Use database indexes for frequently queried columns
- Implement caching for recommendations
- Enable gzip compression in production
- Use CDN for static assets
- Monitor query performance with `SQLALCHEMY_ECHO`

## Support & Documentation

- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **Database Schema**: See [docs/database_schema.sql](docs/database_schema.sql)
- **Issues**: Create an issue in the repository
- **Documentation**: Check the `docs/` folder

## License

This project is developed for educational purposes as part of the Expert Systems course.

## Version History

- **v1.0.0** (Current) - Initial release with core features
- Features: Questionnaire, recommendations, comparison, admin dashboard

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the application**
   - User Interface: http://localhost:5000
   - Admin Login: http://localhost:5000/auth/login

## Default Admin Account

- **Username**: admin
- **Password**: admin123
- **Note**: Change password after first login

## Development

### Running Tests
```bash
pytest
pytest --cov=app  # With coverage report
```

### Database Migrations
```bash
# Create new migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback
flask db downgrade
```

## Team Members

- **Seng Sokang** - Project Manager / QA
- **Lim Rattana** - Backend Developer
- **Chey Chansomny** - Frontend Developer

## Sprint Progress

- [x] Sprint 0: Project Setup & Planning (Week 1-2)
- [ ] Sprint 1: Backend Foundation (Week 3-4)
- [ ] Sprint 2: Data & Rules Management (Week 5-6)
- [ ] Sprint 3: Expert System Logic (Week 7-8)
- [ ] Sprint 4: Frontend Development (Week 9-10)
- [ ] Sprint 5: Integration & Testing (Week 11)
- [ ] Sprint 6: Documentation & Deployment (Week 12)

## Documentation

- [Sprint Plan](docs/sprint_plan.md)
- [SRS Document](docs/SRS.md)
- [ERD Diagram](docs/ERD.md)
- [API Documentation](docs/API_Documentation.md)
- [User Manual](docs/USER_MANUAL.md)
- [Admin Manual](docs/ADMIN_MANUAL.md)

## License

This project is developed for educational purposes as part of a university assignment.

## Acknowledgments

- Course Instructor
- IT Experts for rule validation
- Test users for feedback
"# TechAdvisor" 
