# PHASE 2: PROJECT STRUCTURE ANALYSIS
**TechAdvisor Expert System - Detailed Module & Folder Analysis**

---

## OVERVIEW

TechAdvisor follows a **layered architecture** with clear separation of concerns:

```
┌──────────────────────────────────────────────────────────┐
│                  FLASK APPLICATION LAYER                 │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ PRESENTATION LAYER (Routes + Templates)           │  │
│  │ ├── user.py (Public recommendations)              │  │
│  │ ├── admin.py (Admin dashboard)                    │  │
│  │ ├── auth.py (Login/Register)                      │  │
│  │ └── api.py (REST API endpoints)                   │  │
│  └────────────────────────────────────────────────────┘  │
│                           ↓                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │ BUSINESS LOGIC LAYER (Services)                   │  │
│  │ ├── inference_engine.py (Expert system)           │  │
│  │ ├── recommendation_service.py (Orchestration)     │  │
│  │ └── comparison_service.py (Pros/Cons analysis)    │  │
│  └────────────────────────────────────────────────────┘  │
│                           ↓                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │ FORM & VALIDATION LAYER (Forms)                   │  │
│  │ ├── recommendation_forms.py (Questionnaire)       │  │
│  │ ├── product_forms.py (Product CRUD)               │  │
│  │ ├── rule_forms.py (Rule builder)                  │  │
│  │ ├── user_forms.py (User management)               │  │
│  │ └── role_forms.py (Role definition)               │  │
│  └────────────────────────────────────────────────────┘  │
│                           ↓                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │ DATA ACCESS LAYER (Models + ORM)                  │  │
│  │ ├── product.py (Products, Brands, Categories)     │  │
│  │ ├── rule.py (Rules & Conditions)                  │  │
│  │ ├── user.py (Users & Audit Logs)                  │  │
│  │ └── role.py (RBAC - Roles & Permissions)          │  │
│  └────────────────────────────────────────────────────┘  │
│                           ↓                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │ DATABASE LAYER (MySQL)                            │  │
│  │ ├── 10+ normalized tables                         │  │
│  │ └── Foreign keys & indexes                        │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## DIRECTORY STRUCTURE ANALYSIS

```
TechAdvisor/
│
├── 📄 config.py              ← Flask configuration (Database, Security)
├── 📄 run.py                 ← Application entry point
├── 📄 requirements.txt        ← Python dependencies
├── 📄 pytest.ini              ← Test configuration
├── 📄 setup.cfg               ← Setup configuration
│
├── 📁 app/                    ← MAIN APPLICATION PACKAGE
│   │
│   ├── 📄 __init__.py         ← Application factory (create_app)
│   │                          └─ Initializes Flask, DB, extensions
│   │
│   ├── 📁 models/             ← DATA MODELS (ORM Layer)
│   │   ├── __init__.py
│   │   ├── product.py         ← Product, Brand, Category, Specification
│   │   ├── rule.py            ← Rule, RuleCondition
│   │   ├── user.py            ← User, AuditLog
│   │   └── role.py            ← Role, Permission, RBAC
│   │
│   ├── 📁 routes/             ← BLUEPRINTS (URL Handlers)
│   │   ├── __init__.py
│   │   ├── user.py            ← Public routes (/recommend, /compare)
│   │   ├── admin.py           ← Admin dashboard & management
│   │   ├── auth.py            ← Authentication (/login, /logout)
│   │   └── api.py             ← REST API endpoints (/api/products)
│   │
│   ├── 📁 services/           ← BUSINESS LOGIC
│   │   ├── __init__.py
│   │   ├── inference_engine.py     ← CORE: Forward chaining logic
│   │   ├── recommendation_service.py ← Orchestrates recommendations
│   │   └── comparison_service.py     ← Pros/Cons analysis
│   │
│   ├── 📁 forms/              ← FORM VALIDATION & BUILDING
│   │   ├── __init__.py
│   │   ├── auth_forms.py       ← LoginForm, RegisterForm
│   │   ├── recommendation_forms.py ← RecommendationForm (questionnaire)
│   │   ├── product_forms.py    ← ProductForm, BrandForm
│   │   ├── rule_forms.py       ← RuleForm (condition builder)
│   │   ├── user_forms.py       ← UserForm (account management)
│   │   ├── brand_forms.py      ← BrandForm
│   │   └── role_forms.py       ← RoleForm (role assignment)
│   │
│   ├── 📁 utils/              ← UTILITY FUNCTIONS
│   │   ├── __init__.py
│   │   └── decorators.py       ← @permission_required, @admin_required
│   │
│   ├── 📁 static/             ← STATIC ASSETS (CSS, Images, JS)
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   └── uploads/           ← User-uploaded files
│   │
│   └── 📁 templates/          ← HTML JINJA2 TEMPLATES
│       ├── base.html           ← Base layout (navigation, inheritance)
│       ├── 📁 user/            ← User-facing pages
│       │   ├── home.html       ← Landing page
│       │   ├── questionnaire.html ← Preference form
│       │   ├── results.html    ← Recommendation results display
│       │   ├── compare.html    ← Side-by-side comparison
│       │   ├── comparison_analysis.html ← Pros/Cons analysis
│       │   └── product_detail.html ← Single product page
│       ├── 📁 admin/           ← Admin dashboard pages
│       │   ├── dashboard.html  ← Admin home
│       │   ├── products.html   ← Product list/manage
│       │   ├── product_form.html ← Create/edit product
│       │   ├── brands.html     ← Brand management
│       │   ├── brand_form.html ← Create/edit brand
│       │   ├── rules.html      ← Rule management
│       │   ├── rule_form.html  ← Rule builder UI
│       │   ├── users.html      ← User management
│       │   ├── user_form.html  ← Create/edit user
│       │   ├── roles.html      ← Role management
│       │   ├── role_form.html  ← Role/permission assignment
│       │   └── audit_log.html  ← System activity log
│       ├── 📁 auth/            ← Authentication pages
│       │   ├── login.html      ← Login form
│       │   └── register.html   ← Registration form
│       └── 📁 components/      ← Reusable components
│           └── loading.html    ← Loading indicator
│
├── 📁 tests/                  ← UNIT & INTEGRATION TESTS
│   ├── __init__.py
│   ├── conftest.py            ← Pytest fixtures & configuration
│   ├── test_models.py          ← Model tests
│   ├── test_routes.py          ← Route/endpoint tests
│   ├── test_inference_engine.py ← Expert system tests
│   ├── test_recommendation_service.py ← Recommendation logic tests
│   └── test_comparison_service.py ← Comparison tests
│
├── 📁 migrations/             ← DATABASE MIGRATIONS
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/              ← Version-controlled schema changes
│       └── 1bbcdce30bff_initial_migration.py
│
├── 📁 docs/                   ← PROJECT DOCUMENTATION
│   ├── database_schema.sql    ← SQL schema definition
│   └── technical/
│
└── 📁 ANALYSIS_DOCS/          ← THIS ANALYSIS
    ├── 01_PHASE1_PROJECT_UNDERSTANDING.md
    └── 02_PHASE2_PROJECT_STRUCTURE.md (THIS FILE)
```

---

## 1. ROOT LEVEL FILES

### `config.py` - Configuration Management
**Purpose**: Centralize configuration across environments

**Contents**:
```python
class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    
    # Database connection
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://...'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

**Key Features**:
- Environment-based configuration (dev, test, production)
- Dot-env file support
- Security headers enabled
- CSRF protection enabled
- File upload restrictions
- Session configuration

---

### `run.py` - Application Entry Point
**Purpose**: Start the Flask development server

**Contents**:
```python
from app import create_app, db
import os

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5001,          # Changed from 5000 (Windows restriction)
        debug=app.config['DEBUG']
    )
```

**How to Run**:
```bash
python run.py              # Start development server (http://localhost:5001)
```

---

### `pytest.ini` - Test Configuration
**Purpose**: Configure pytest behavior

**Contains**:
- Test discovery patterns
- Markers for categorizing tests
- Coverage reporting thresholds

---

### `requirements.txt` - Python Dependencies
**Key Dependencies**:
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
Flask-Login==0.6.3
Flask-WTF==1.2.1
WTForms==3.0.1
python-dotenv==1.0.0
PyMySQL==1.1.0
cryptography==41.0.4
pytest==7.4.2
```

---

## 2. APP/ PACKAGE STRUCTURE

### `app/__init__.py` - Application Factory
**Purpose**: Initialize Flask application and extensions

**Key Components**:
```python
# Extensions initialization
db = SQLAlchemy()           # Database ORM
migrate = Migrate()         # Database migrations
login_manager = LoginManager()  # Session management
csrf = CSRFProtect()        # CSRF token protection

def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    
    # Security headers
    @app.after_request
    def set_security_headers(response):
        # Add security headers to all responses
        ...
    
    return app
```

**Why Factory Pattern?**
- ✅ Easy testing (create test instances)
- ✅ Configuration-based initialization
- ✅ Multiple app instances possible
- ✅ Blueprints registration centralized

---

## 3. MODELS/ PACKAGE - Data Persistence Layer

### `models/product.py` - Product Catalog

**Classes**:

#### **Brand Model**
```python
class Brand:
    id INT (PK)
    name VARCHAR(100) UNIQUE
    logo_url VARCHAR(255)
    created_at DATETIME
    
    Relationships:
    - products: One Brand → Many Products
```

**Purpose**: Store manufacturer information (Apple, Samsung, Dell, etc.)

#### **Category Model**
```python
class Category:
    id INT (PK)
    name VARCHAR(50) UNIQUE           # 'Smartphone', 'Laptop'
    description TEXT
    created_at DATETIME
    
    Relationships:
    - products: One Category → Many Products
    - rules: One Category → Many Rules
```

**Purpose**: Categorize products (Smartphone, Laptop, etc.)

#### **Product Model**
```python
class Product:
    id INT (PK)
    name VARCHAR(255)
    brand_id INT (FK)
    category_id INT (FK)
    price DECIMAL(10,2)
    image_url VARCHAR(500)
    description TEXT
    is_active BOOLEAN (default: TRUE)
    created_at, updated_at DATETIME
    
    Relationships:
    - brand: Many Products → One Brand
    - category: Many Products → One Category
    - specifications: One Product → Many Specifications
    
    Methods:
    - to_dict(): Convert to JSON-serializable dict
```

**Purpose**: Store individual products (iPhone 15, Dell XPS 13, etc.)

**Indexes**: 
- idx_name (for searching products)
- idx_brand (for filtering by brand)
- idx_category (for filtering by category)
- idx_price (for price-based sorting)
- idx_active (to quickly find active products)

#### **Specification Model**
```python
class Specification:
    id INT (PK)
    product_id INT (FK)
    spec_key VARCHAR(100)              # 'RAM', 'Processor', 'Battery'
    spec_value TEXT                    # '12GB', 'Intel i7', '5000mAh'
    
    Relationships:
    - product: Many Specs → One Product
```

**Purpose**: Store technical details for products

**Usage Example**:
```python
# Accessing product with specifications
product = Product.query.get(1)
for spec in product.specifications:
    print(f"{spec.spec_key}: {spec.spec_value}")
    # Output: "RAM: 12GB"
```

---

### `models/rule.py` - Expert System Rules

#### **Rule Model**
```python
class Rule:
    id INT (PK)
    name VARCHAR(255)                  # 'Gaming Laptop for Professionals'
    description TEXT
    category_id INT (FK)               # Which category this rule applies to
    priority INT (default: 0)          # Higher = matched first
    is_active BOOLEAN (default: TRUE)
    created_at DATETIME
    
    Relationships:
    - category: Many Rules → One Category
    - conditions: One Rule → Many RuleConditions
    
    Methods:
    - to_dict(): Serialize with conditions
```

**Purpose**: Store inference rules used by expert system

**Example Rule Data**:
```
Name: "Gaming Laptop Under $1000"
Description: "For gamers with strict budget constraints"
Category: Laptop
Priority: 85
Active: TRUE
Conditions:
  - budget >= 500
  - usage_type = 'gaming'
  - category = 'laptop'
```

#### **RuleCondition Model**
```python
class RuleCondition:
    id INT (PK)
    rule_id INT (FK)
    condition_type VARCHAR(50)         # 'budget', 'usage', 'brand'
    condition_key VARCHAR(100)         # 'budget', 'usage_type'
    operator VARCHAR(20)               # '>=', '==', 'in', 'contains'
    condition_value VARCHAR(255)       # '1000', 'gaming', 'ASUS,MSI'
    
    Relationships:
    - rule: Many Conditions → One Rule
    
    Methods:
    - to_dict(): Serialize condition
```

**Purpose**: Store individual condition criteria for rules

**Supported Operators**:
- `==` (equals): String exact match
- `!=` (not equals): String inverse match
- `<` (less than): Numeric comparison
- `>` (greater than): Numeric comparison
- `<=` (less equal): Numeric comparison
- `>=` (greater equal): Numeric comparison
- `in`: Check if value in comma-separated list
- `contains`: Substring search

---

### `models/user.py` - Authentication & Audit

#### **User Model**
```python
class User(UserMixin):
    id INT (PK)
    username VARCHAR(50) UNIQUE
    email VARCHAR(100) UNIQUE
    password_hash VARCHAR(255)         # Scrypt hashed
    role ENUM('admin', 'staff')        # Legacy
    role_id INT (FK)                   # New RBAC
    is_active BOOLEAN (default: TRUE)
    created_at, updated_at DATETIME
    
    Relationships:
    - audit_logs: One User → Many AuditLogs
    - role_obj: Many Users → One Role (RBAC)
    
    Methods:
    - set_password(pwd): Hash and store password
    - check_password(pwd): Verify password
    - has_role(role_name): Check user role
    - has_permission(perm_slug): Check specific permission
```

**Purpose**: Store user accounts for administrators and staff

**Security Features**:
- Passwords hashed with scrypt (not plaintext!)
- Active/inactive flag to disable accounts
- Flexible RBAC system with role & permission checking

#### **AuditLog Model**
```python
class AuditLog:
    id INT (PK)
    user_id INT (FK)                   # Who did it
    action VARCHAR(100)                # 'CREATE', 'UPDATE', 'DELETE'
    table_name VARCHAR(50)             # 'products', 'rules', 'users'
    record_id INT                      # Which record was affected
    details TEXT                       # What changed (serialized)
    ip_address VARCHAR(45)             # Source IP
    created_at DATETIME                # When
    
    Relationships:
    - user: Many Logs → One User
```

**Purpose**: Track all system changes for compliance and debugging

**Indexes**:
- idx_user (to find all actions by a user)
- idx_action (to find all actions of a type)
- idx_created (to find recent actions)

---

### `models/role.py` - RBAC System

#### **Permission Model**
```python
class Permission:
    id INT (PK)
    name VARCHAR(50) UNIQUE            # 'Create Products'
    slug VARCHAR(50) UNIQUE            # 'product.create'
    description VARCHAR(255)
```

**Purpose**: Define granular permissions

**Example Permissions**:
- `product.create` → Create new products
- `product.edit` → Modify products
- `product.delete` → Delete products
- `rule.create` → Create rules
- `rule.edit` → Modify rules
- `user.create` → Create user accounts
- `user.edit` → Modify user accounts

#### **Role Model**
```python
class Role:
    id INT (PK)
    name VARCHAR(50) UNIQUE            # 'Admin', 'Staff'
    description VARCHAR(255)
    is_system BOOLEAN (default: FALSE) # System roles can't be deleted
    created_at, updated_at DATETIME
    
    Relationships:
    - permissions: Many Roles ↔ Many Permissions
    - users: One Role ← Many Users
    
    Methods:
    - has_permission(slug): Check if role has permission
```

**Purpose**: Group permissions into roles

**Example Role Structure**:
```
ADMIN ROLE:
├── product.create
├── product.edit
├── product.delete
├── rule.create
├── rule.edit
├── user.create
└── (all permissions)

STAFF ROLE:
├── product.view
├── product.edit
└── rule.view
```

#### **role_permissions Table (Association)**
```python
role_permissions = db.Table(
    'role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), PK),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), PK)
)
```

**Purpose**: Many-to-many relationship between roles and permissions

---

## 4. ROUTES/ PACKAGE - URL Handlers (Blueprints)

### Architecture Pattern: **Flask Blueprints**
Blueprints organize routes into logical modules, each with their own namespace and templates.

---

### `routes/user.py` - Public User Routes
**URL Prefix**: `/` (no prefix)
**Authentication**: Optional (not required)

**Key Routes**:

| Route | Method | Purpose | Returns |
|-------|--------|---------|---------|
| `/` | GET | Home page | user/home.html |
| `/recommend` | GET | Show questionnaire form | user/questionnaire.html |
| `/recommend` | POST | Process form, show results | user/results.html |
| `/compare` | GET | Side-by-side comparison | user/compare.html |
| `/compare-analysis` | GET | Pros & Cons analysis (2 products) | user/comparison_analysis.html |

**Logic Flow**:

```python
@user_bp.route('/recommend', methods=['GET', 'POST'])
def recommend():
    form = RecommendationForm()
    
    if form.validate_on_submit():
        # Extract form data
        user_inputs = {
            'category_id': form.category.data,
            'budget': form.budget.data,
            'usage_type': form.usage_type.data,
            'preferred_brand': form.preferred_brand.data
        }
        
        # Get recommendations from service
        rec_service = RecommendationService()
        recommendations = rec_service.get_recommendations(user_inputs)
        
        # Return results
        return render_template('user/results.html',
                             products=recommendations['products'],
                             message=recommendations['message'])
    
    # GET: Show form
    return render_template('user/questionnaire.html', form=form)
```

---

### `routes/admin.py` - Admin Dashboard Routes
**URL Prefix**: `/admin`
**Authentication**: **Required** (`@login_required`)
**Authorization**: Staff or Admin role (`@staff_required`)

**Key Routes**:

| Route | Purpose | Authorization |
|-------|---------|---|
| `/admin/dashboard` | Admin home with statistics | Staff+ |
| `/admin/products` | List/search products | Staff+ |
| `/admin/products/new` | Create product | Admin |
| `/admin/products/<id>/edit` | Edit product | Admin |
| `/admin/products/<id>/delete` | Delete product | Admin |
| `/admin/brands` | List brands | Staff+ |
| `/admin/brands/new` | Create brand | Admin |
| `/admin/rules` | List/search rules | Staff+ |
| `/admin/rules/new` | Create rule with conditions | Admin |
| `/admin/rules/<id>/edit` | Edit rule | Admin |
| `/admin/users` | List users | Admin |
| `/admin/users/new` | Create user | Admin |
| `/admin/roles` | Manage roles & permissions | Admin |
| `/admin/audit-log` | View system audit trail | Admin |

**Protected Decorator**:
```python
@admin_bp.route('/dashboard')
@login_required          # User must be logged in
@staff_required         # User must be Admin or Staff
def dashboard():
    # Get statistics
    total_products = Product.query.count()
    total_rules = Rule.query.count()
    # ... render dashboard
```

---

### `routes/auth.py` - Authentication Routes
**URL Prefix**: `/auth`
**Authentication**: Variable

| Route | Method | Purpose | Required | Returns |
|-------|--------|---------|----------|---------|
| `/auth/login` | GET | Show login form | No | auth/login.html |
| `/auth/login` | POST | Process login | No | Redirect to dashboard or home |
| `/auth/logout` | GET | Logout user | Yes | Redirect to home |
| `/auth/register` | GET | Show registration form | Yes (Admin only) | auth/register.html |
| `/auth/register` | POST | Create new user | Yes (Admin only) | Redirect to users list |

**Login Logic**:
```python
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        # Find user by username
        user = User.query.filter_by(username=form.username.data).first()
        
        # Check password
        if user and user.check_password(form.password.data):
            # Create session
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('auth/login.html', form=form)
```

---

### `routes/api.py` - REST API Endpoints
**URL Prefix**: `/api`
**Authentication**: Not required (public API)
**Returns**: JSON

| Route | Method | Purpose | Query Params |
|-------|--------|---------|---|
| `/api/products` | GET | List all products | category, brand |
| `/api/products/<id>` | GET | Get single product | - |
| `/api/brands` | GET | List all brands | - |
| `/api/categories` | GET | List all categories | - |

**Example API Response**:
```json
GET /api/products?category=Laptop&brand=ASUS

{
    "id": 1,
    "name": "ASUS TUF Gaming Laptop",
    "brand": "ASUS",
    "category": "Laptop",
    "price": 749.99,
    "image_url": "/static/images/asus-tuf.jpg",
    "description": "Gaming laptop with RTX graphics",
    "specifications": {
        "processor": "Intel i7",
        "ram": "16GB",
        "storage": "512GB SSD"
    }
}
```

---

## 5. SERVICES/ PACKAGE - Business Logic

### `services/inference_engine.py` - Expert System Core

**Class**: `InferenceEngine`

**Responsibility**: Implement forward-chaining inference algorithm

**Key Methods**:

```python
class InferenceEngine:
    
    def __init__(self):
        self.working_memory = {}      # Stores facts
        self.matched_rules = []        # Stores matched rules
    
    def add_fact(self, key, value):
        """Add user input to working memory"""
        self.working_memory[key] = value
    
    def evaluate_condition(self, condition, facts) -> bool:
        """Evaluate single condition: 
        - Extract key from facts
        - Apply operator (==, !=, <, >, <=, >=, in, contains)
        - Compare with expected value
        """
        operator = condition.operator
        actual = facts.get(condition.condition_key)
        expected = condition.condition_value
        
        # Implement logic for each operator...
        if operator == '>=':
            return float(actual) >= float(expected)
        # ... etc
    
    def match_rules(self, rules, facts) -> List[Rule]:
        """Match all rules against current facts
        FOR EACH rule:
          FOR EACH condition in rule:
            IF condition not satisfied:
              SKIP rule
          IF all conditions satisfied:
            ADD rule to matched
        SORT by priority
        """
        matched = []
        
        for rule in rules:
            all_met = True
            for condition in rule.conditions:
                if not self.evaluate_condition(condition, facts):
                    all_met = False
                    break
            if all_met and rule.is_active:
                matched.append(rule)
        
        return sorted(matched, key=lambda r: r.priority, reverse=True)
    
    def infer(self, user_inputs) -> List[Rule]:
        """Run complete inference:
        1. Load facts
        2. Load rules
        3. Match rules
        4. Return matched rules sorted by priority
        """
        # Add user inputs to working memory
        for key, value in user_inputs.items():
            self.add_fact(key, value)
        
        # Get active rules from database
        rules = Rule.query.filter_by(is_active=True).all()
        
        # Match rules
        self.matched_rules = self.match_rules(rules, self.working_memory)
        
        return self.matched_rules
```

**Algorithm Complexity**:
- Time: O(R × C) where R = rules, C = conditions per rule
- Space: O(R) for matched_rules list

**Why Forward Chaining?**
- ✅ Data-driven (matches our questionnaire → products flow)
- ✅ All conclusions found in one pass
- ✅ Efficient for recommendation systems
- ℹ️ Alternative: Backward chaining (goal-driven) - less suitable here

---

### `services/recommendation_service.py` - Orchestration

**Class**: `RecommendationService`

**Responsibility**: Orchestrate complete recommendation workflow

**Key Methods**:

```python
class RecommendationService:
    
    def __init__(self):
        self.engine = InferenceEngine()
    
    def get_recommendations(self, user_input: Dict, limit: int = 10) -> Dict:
        """Main entry point
        Returns: {
            'products': [list of dicts with reasoning],
            'total_matches': 3,
            'fired_rules': 5,
            'message': 'Found 3 products...'
        }
        """
        # 1. Run inference engine
        matched_rules = self.engine.infer(user_input)
        
        # 2. Fetch products matching rules
        products = self._fetch_products(matched_rules, user_input, limit)
        
        # 3. Add reasoning explanations
        products_with_reasoning = self._add_reasoning(products, matched_rules)
        
        return {
            'products': products_with_reasoning,
            'total_matches': len(products),
            'fired_rules': len(matched_rules)
        }
    
    def _fetch_products(self, matched_rules, user_input, limit) -> List[Product]:
        """Filter products based on:
        1. Budget (price <= budget)
        2. Category (must match category_id from rules)
        3. Brand preference (optional filter)
        4. Active status (only active=TRUE)
        """
        query = Product.query.filter_by(is_active=True)
        
        # Budget filter
        if 'budget' in user_input:
            budget = float(user_input['budget'])
            query = query.filter(Product.price <= budget)
        
        # Category filter
        if 'category_id' in user_input and user_input['category_id']:
            query = query.filter(Product.category_id == user_input['category_id'])
        
        # Brand filter
        if 'preferred_brand' in user_input and user_input['preferred_brand']:
            brand = Brand.query.filter(
                db.func.lower(Brand.name) == user_input['preferred_brand'].lower()
            ).first()
            if brand:
                query = query.filter(Product.brand_id == brand.id)
        
        return query.order_by(Product.price.asc()).limit(limit).all()
    
    def _add_reasoning(self, products, matched_rules) -> List[Dict]:
        """Add confidence, reasoning, and matched rule to each product"""
        results = []
        
        for product in products:
            # Find matching rule for this product's category
            matching_rule = None
            for rule in matched_rules:
                if rule.category_id == product.category_id:
                    matching_rule = rule
                    break
            
            # Calculate confidence (50 base + rule priority)
            confidence = min(100, 50 + (matching_rule.priority if matching_rule else 50))
            
            # Generate reasoning text
            reasoning = self._generate_reasoning(product)
            
            results.append({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'confidence': confidence,
                'reasoning': reasoning,
                'matched_rule': matching_rule.name if matching_rule else None,
                'specifications': [...]
            })
        
        # Sort by confidence descending
        return sorted(results, key=lambda x: x['confidence'], reverse=True)
```

---

### `services/comparison_service.py` - Intelligent Comparison

**Class**: `ComparisonService`

**Responsibility**: Compare 2 products with pros/cons analysis

**Key Method**:

```python
class ComparisonService:
    
    def __init__(self):
        # Define benchmarks for evaluation
        self.benchmarks = {
            'smartphone': {
                'ram': {'excellent': 12, 'good': 8, 'minimum': 6},
                'storage': {'excellent': 256, 'good': 128, 'minimum': 64},
                'battery': {'excellent': 5000, 'good': 4000, 'minimum': 3000}
            },
            'laptop': {
                'ram': {'excellent': 16, 'good': 8, 'minimum': 4},
                'storage': {'excellent': 512, 'good': 256, 'minimum': 128}
            }
        }
    
    def compare_two_products(
        self,
        product1: Product,
        product2: Product,
        user_preferences: Dict = None
    ) -> Dict:
        """Compare two products
        Returns: {
            'product1': {
                'pros': ['Fast processor', 'Good battery'],
                'cons': ['Expensive', 'Limited storage']
            },
            'product2': {...},
            'advantages': {
                'product1': ['Better price'],
                'product2': ['Better specs']
            },
            'winner': 1,  # 1=product1, 2=product2, 0=tie
            'winner_reason': 'Product 1 offers better value...'
        }
        """
        # Extract pros for each product
        product1_pros = self.extract_pros(product1, user_preferences)
        product1_cons = self.extract_cons(product1, user_preferences)
        # ... similar for product2
        
        # Calculate scores
        score1 = self.calculate_overall_score(product1, user_preferences)
        score2 = self.calculate_overall_score(product2, user_preferences)
        
        # Determine winner
        winner = 1 if score1 > score2 else (2 if score2 > score1 else 0)
        
        return {
            'product1': {...},
            'product2': {...},
            'winner': winner,
            'winner_reason': '...'
        }
    
    def extract_pros(self, product, user_prefs) -> List[str]:
        """Extract strong points relative to benchmarks"""
        pros = []
        for spec in product.specifications:
            # Compare against benchmark
            if spec.spec_value exceeds benchmark:
                pros.append(f"Strong {spec.spec_key}")
        return pros
    
    def extract_cons(self, product, user_prefs) -> List[str]:
        """Extract weak points relative to benchmarks"""
        cons = []
        for spec in product.specifications:
            if spec.spec_value below benchmark:
                cons.append(f"Weak {spec.spec_key}")
        return cons
```

---

## 6. FORMS/ PACKAGE - Input Validation

**Technology**: WTForms + Flask-WTF

**File Structure**:
```
forms/
├── auth_forms.py         → LoginForm, RegisterForm
├── recommendation_forms.py → RecommendationForm (questionnaire)
├── product_forms.py      → ProductForm
├── rule_forms.py         → RuleForm (dynamic condition builder)
├── user_forms.py         → UserForm
├── brand_forms.py        → BrandForm
└── role_forms.py         → RoleForm
```

### `recommendation_forms.py` - Questionnaire Form

```python
class RecommendationForm(FlaskForm):
    """User questionnaire for product recommendations"""
    
    category = SelectField(
        'What are you looking for?',
        choices=[('smartphone', 'Smartphone'), ('laptop', 'Laptop')],
        validators=[DataRequired()]
    )
    
    budget = IntegerField(
        'Your budget (USD)',
        validators=[
            DataRequired(),
            NumberRange(min=100, max=10000)
        ]
    )
    
    usage_type = SelectField(
        'Primary Usage',
        choices=[
            ('gaming', 'Gaming'),
            ('work', 'Business'),
            ('study', 'Education'),
            ('general', 'General'),
            ('creative', 'Content Creation')
        ],
        validators=[DataRequired()]
    )
    
    preferred_brand = StringField(
        'Preferred Brand (optional)',
        validators=[Optional(), Length(max=50)]
    )
    
    submit = SubmitField('Get Recommendations')
```

**Validation Features**:
- ✅ CSRF token protection (FlaskForm)
- ✅ Server-side validation
- ✅ Type checking (Integer, String)
- ✅ Range validation (100-10000 for budget)
- ✅ Required vs optional fields

---

## 7. UTILS/ PACKAGE - Decorators & Helpers

### `decorators.py` - Route Protection

```python
def permission_required(permission_slug):
    """Check for specific permission"""
    # Protects route by checking current_user.has_permission(slug)
    # Returns 403 if denied
    pass

def admin_required(f):
    """Check if user is admin"""
    # Legacy decorator
    pass

def staff_required(f):
    """Check if user is admin OR staff"""
    # Protects most admin routes
    pass
```

**Usage**:
```python
@admin_bp.route('/sensitive')
@login_required
@admin_required
def sensitive_operation():
    # Only admins reach here
    pass

@admin_bp.route('/create-product')
@permission_required('product.create')
def create_product():
    # Only users with 'product.create' permission
    pass
```

---

## 8. TEMPLATES/ PACKAGE - Frontend

**Structure**:
```
templates/
├── base.html                    ← Master layout
├── user/                        ← Public-facing templates
│   ├── home.html               ← Landing page
│   ├── questionnaire.html      ← Preference questionnaire
│   ├── results.html            ← Recommendation results
│   ├── compare.html            ← Side-by-side comparison
│   ├── comparison_analysis.html ← Pros & Cons
│   └── product_detail.html     ← Single product page
├── admin/                       ← Admin dashboard templates
│   ├── dashboard.html
│   ├── products.html
│   ├── product_form.html
│   ├── rules.html
│   ├── rule_form.html
│   ├── users.html
│   ├── user_form.html
│   ├── roles.html
│   ├── role_form.html
│   └── audit_log.html
├── auth/                        ← Authentication templates
│   ├── login.html
│   └── register.html
└── components/                  ← Reusable components
    └── loading.html
```

### Template Inheritance Pattern
```html
<!-- base.html -->
<html>
  <head>{% block head %}...{% endblock %}</head>
  <body>
    <nav>Navigation</nav>
    <main>{% block content %}{% endblock %}</main>
    <footer>Footer</footer>
  </body>
</html>

<!-- home.html -->
{% extends "base.html" %}

{% block content %}
<h1>Welcome to TechAdvisor</h1>
<a href="{{ url_for('user.recommend') }}">Get Recommendations</a>
{% endblock %}
```

---

## 9. TESTS/ PACKAGE - Quality Assurance

```
tests/
├── conftest.py                    ← Pytest fixtures
├── test_models.py                 ← Database model tests
├── test_routes.py                 ← Endpoint tests
├── test_inference_engine.py       ← Expert system tests
├── test_recommendation_service.py ← Service tests
└── test_comparison_service.py     ← Comparison tests
```

### `conftest.py` - Test Configuration

```python
# Fixtures for testing
@pytest.fixture
def app():
    """Create test Flask app"""
    app = create_app('testing')
    # Create tables, seed data
    return app

@pytest.fixture
def client(app):
    """Test client for making requests"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI runner for testing commands"""
    return app.test_cli_runner()
```

### Running Tests
```bash
pytest                           # Run all tests
pytest tests/test_models.py     # Run specific file
pytest -v                       # Verbose output
pytest --cov                    # Coverage report
pytest -k "test_inference"      # Run matching tests
```

---

## 10. MIGRATIONS/ - Database Version Control

**Purpose**: Track schema changes over time

**File Structure**:
```
migrations/
├── alembic.ini                 ← Alembic configuration
├── env.py                      ← Migration environment
├── script.py.mako              ← Migration template
└── versions/                   ← Migration scripts
    └── 1bbcdce30bff_initial_migration.py
```

### How Migrations Work
```bash
# Generate new migration
flask db migrate -m "Add new table"

# Apply migration
flask db upgrade

# Rollback
flask db downgrade

# View migration history
flask db history
```

**Benefits**:
- ✅ Version control for database schema
- ✅ Repeatable deployments
- ✅ Easy rollback
- ✅ Team collaboration

---

## 11. STATIC/ - Frontend Assets

```
static/
├── css/                    ← Stylesheets (Tailwind)
├── js/                     ← JavaScript files
├── images/                 ← Logo, favicon, etc.
└── uploads/                ← User-uploaded files (brand logos, product images)
```

---

## 12. DEPENDENCY GRAPH

```
run.py
  └── app/__init__.py (create_app)
      ├── config.py
      ├── models/
      │   ├── product.py (Brand, Category, Product, Specification)
      │   ├── rule.py (Rule, RuleCondition)
      │   ├── user.py (User, AuditLog)
      │   └── role.py (Role, Permission)
      ├── routes/
      │   ├── user.py → services/recommendation_service.py
      │   │           → services/comparison_service.py
      │   ├── admin.py → models/* (CRUD operations)
      │   ├── auth.py → models/user.py
      │   └── api.py → models/* (JSON responses)
      ├── services/
      │   ├── recommendation_service.py
      │   │   └── services/inference_engine.py
      │   └── comparison_service.py → models/product.py
      ├── forms/
      │   ├── recommendation_forms.py ← recommendation_forms.py
      │   ├── rule_forms.py ← RuleForm
      │   └── product_forms.py ← ProductForm
      └── utils/
          └── decorators.py (used by routes)

DATABASE (MySQL)
  ├── users
  ├── audit_logs
  ├── roles
  ├── permissions
  ├── role_permissions
  ├── brands
  ├── categories
  ├── products
  ├── specifications
  ├── rules
  └── rule_conditions
```

---

## SUMMARY: MODULE PURPOSES AT A GLANCE

| Module | Layer | Purpose |
|--------|-------|---------|
| **config.py** | Config | Environment-based settings |
| **app/__init__.py** | Init | Application factory & extension setup |
| **models/product.py** | Data | Product catalog (Brand, Category, Product, Spec) |
| **models/rule.py** | Data | Expert system rules & conditions |
| **models/user.py** | Data | Authentication & audit logging |
| **models/role.py** | Data | RBAC (Role, Permission, Association) |
| **routes/user.py** | Presentation | Public questionnaire & comparison |
| **routes/admin.py** | Presentation | Admin dashboard & CRUD |
| **routes/auth.py** | Presentation | Login/logout/register |
| **routes/api.py** | Presentation | REST API endpoints |
| **inference_engine.py** | Logic | 🔴 CORE: Forward chaining expert system |
| **recommendation_service.py** | Logic | Orchestrate recommendations |
| **comparison_service.py** | Logic | Intelligent product comparison |
| **forms/** | Validation | Input validation & CSRF protection |
| **utils/decorators.py** | Security | Route protection & RBAC enforcement |
| **templates/** | Presentation | Jinja2 HTML templates |
| **tests/** | QA | Unit & integration tests |
| **migrations/** | DevOps | Database version control |

---

## KEY ARCHITECTURAL INSIGHTS

### 1. **Layered Architecture**
```
Presentation (Routes)
     ↓
Business Logic (Services)
     ↓
Data Access (Models/ORM)
     ↓
Database
```

### 2. **Separation of Concerns**
- Routes handle HTTP
- Services handle business logic
- Models handle data
- Forms handle validation

### 3. **Expert System Integration**
- InferenceEngine sits in Services layer
- Rules stored in Models/Database
- Accessed through RecommendationService

### 4. **Security & RBAC**
- Decorators enforce permissions
- Models check permissions
- Audit logs track changes
- CSRF tokens on all forms

### 5. **Testability**
- Dependency injection (services take models)
- Fixtures for databases
- Mock objects for testing
- Separate test database (SQLite in-memory)

---

**Next Phase**: PHASE 3 — FEATURE-BY-FEATURE ANALYSIS (coming next)
