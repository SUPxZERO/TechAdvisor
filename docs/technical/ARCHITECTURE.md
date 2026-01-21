# TechAdvisor Expert System - Comprehensive Technical Analysis

A complete technical analysis of the TechAdvisor full-stack web application, covering architecture, workflows, and component interactions from database to frontend.

---

## 1. System Overview

**Project Type**: Rule-Based Expert System for Product Recommendations  
**Domain**: Consumer Electronics (Smartphones & Laptops)  
**Architecture Pattern**: Monolithic MVC with Flask Application Factory

```mermaid
flowchart TB
    subgraph Frontend["Frontend Layer"]
        UI[Jinja2 Templates + Tailwind CSS]
        JS[Vanilla JavaScript]
    end
    
    subgraph Backend["Backend Layer (Flask)"]
        subgraph Blueprints["Route Blueprints"]
            auth[auth_bp<br>/auth/*]
            user[user_bp<br>/*]
            admin[admin_bp<br>/admin/*]
            api[api_bp<br>/api/*]
        end
        
        subgraph Services["Business Logic Services"]
            IE[InferenceEngine<br>Forward Chaining]
            RS[RecommendationService]
            CS[ComparisonService]
        end
        
        subgraph Security["Security & Auth"]
            LoginMgr[Flask-Login]
            CSRF[CSRFProtect]
            RBAC[Role-Based Access Control]
        end
    end
    
    subgraph Database["Database Layer (MySQL 8.0)"]
        Products[(Products<br>Brands<br>Categories<br>Specifications)]
        Rules[(Rules<br>RuleConditions)]
        Users[(Users<br>Roles<br>Permissions<br>AuditLogs)]
    end
    
    UI --> Blueprints
    JS --> api
    Blueprints --> Services
    Services --> Products
    Services --> Rules
    admin --> Users
    auth --> LoginMgr
    LoginMgr --> RBAC
```

---

## 2. Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Jinja2 + Tailwind CSS | Server-side templating with utility-first CSS |
| **JavaScript** | Vanilla JS | Client-side interactivity |
| **Backend** | Flask 2.3.3, Python 3.12 | Web framework |
| **ORM** | SQLAlchemy + Flask-Migrate | Database abstraction and migrations |
| **Database** | MySQL 8.0 (PyMySQL driver) | Persistent storage |
| **Forms** | WTForms + Flask-WTF | Form validation and CSRF protection |
| **Auth** | Flask-Login | Session management |
| **RBAC** | Custom Role/Permission models | Granular access control |
| **Testing** | Pytest | Unit and integration tests |

---

## 3. Database Layer

### 3.1 Schema Design (Relational)

```mermaid
erDiagram
    users ||--o{ audit_logs : creates
    users }o--|| roles : has
    roles }o--o{ permissions : contains
    
    products }o--|| brands : belongs_to
    products }o--|| categories : belongs_to
    products ||--o{ specifications : has
    
    rules }o--o| categories : applies_to
    rules ||--o{ rule_conditions : contains

    users {
        int id PK
        string username UK
        string email UK
        string password_hash
        enum role "admin,staff"
        int role_id FK
        bool is_active
        datetime created_at
        datetime updated_at
    }
    
    roles {
        int id PK
        string name UK
        string description
        bool is_system
        datetime created_at
        datetime updated_at
    }
    
    permissions {
        int id PK
        string name UK
        string slug UK
        string description
    }
    
    brands {
        int id PK
        string name UK
        string logo_url
        datetime created_at
    }
    
    categories {
        int id PK
        string name UK
        text description
        datetime created_at
    }
    
    products {
        int id PK
        string name
        int brand_id FK
        int category_id FK
        decimal price
        string image_url
        text description
        bool is_active
        datetime created_at
        datetime updated_at
    }
    
    specifications {
        int id PK
        int product_id FK
        string spec_key
        text spec_value
    }
    
    rules {
        int id PK
        string name
        text description
        int category_id FK
        int priority
        bool is_active
        datetime created_at
    }
    
    rule_conditions {
        int id PK
        int rule_id FK
        string condition_type
        string condition_key
        string operator
        string condition_value
    }
    
    audit_logs {
        int id PK
        int user_id FK
        string action
        string table_name
        int record_id
        text details
        string ip_address
        datetime created_at
    }
```

### 3.2 Indexing Strategy

| Table | Index Name | Columns | Purpose |
|-------|------------|---------|---------|
| `users` | `idx_username` | `username` | Fast authentication lookup |
| `users` | `idx_email` | `email` | Unique constraint enforcement |
| `products` | `idx_name` | `name` | Product search |
| `products` | `idx_brand` | `brand_id` | Filter by brand |
| `products` | `idx_category` | `category_id` | Category-based queries |
| `products` | `idx_price` | `price` | Budget filtering |
| `products` | `idx_active` | `is_active` | Active product filtering |
| `specifications` | `idx_product_spec` | `product_id, spec_key` | Fast spec lookups |
| `rules` | `idx_priority` | `priority` | Rule ordering |
| `rule_conditions` | `idx_rule` | `rule_id` | Condition retrieval |

### 3.3 Seed Data Strategy

The project uses **multiple seeding scripts** executed in order:

1. **[init_rbac.py](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/init_rbac.py)** - Initializes RBAC roles and permissions
2. **[seed_database.py](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/seed_database.py)** - Core data (users, categories, brands, products)
3. **[seed_products.py](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/seed_products.py)** - Extended product catalog
4. **[seed_rules.py](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/seed_rules.py)** - Basic recommendation rules
5. **[seed_comprehensive_rules.py](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/seed_comprehensive_rules.py)** - Full rule set

> [!TIP]
> Seeders use upsert patterns (`ON DUPLICATE KEY UPDATE`, `check-before-insert`) for idempotent execution.

---

## 4. Backend/API Layer

### 4.1 Application Factory Pattern

The Flask app is created using the [factory pattern](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/__init__.py):

```python
def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    
    return app
```

### 4.2 Blueprint Architecture

| Blueprint | Prefix | Purpose | Auth Required |
|-----------|--------|---------|---------------|
| `auth_bp` | `/auth` | Login, logout, registration | Mixed |
| `user_bp` | `/` | Home, questionnaire, results, compare | No |
| `admin_bp` | `/admin` | Dashboard, CRUD operations | Yes (Admin/Staff) |
| `api_bp` | `/api` | RESTful JSON endpoints | No |

### 4.3 Route Structure

````carousel
**User Routes** ([user.py](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/routes/user.py))
| Route | Method | Handler |
|-------|--------|---------|
| `/` | GET | `home()` |
| `/recommend` | GET, POST | `recommend()` |
| `/compare` | GET | `compare()` |
| `/compare-analysis` | GET | `compare_analysis()` |
| `/product/<id>` | GET | `product_detail()` |
<!-- slide -->
**Auth Routes** ([auth.py](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/routes/auth.py))
| Route | Method | Handler |
|-------|--------|---------|
| `/auth/login` | GET, POST | `login()` |
| `/auth/logout` | GET | `logout()` |
| `/auth/register` | GET, POST | `register()` |
<!-- slide -->
**Admin Routes** ([admin.py](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/routes/admin.py))
- `/admin/dashboard` - Dashboard with statistics
- `/admin/products` - Product CRUD
- `/admin/brands` - Brand management
- `/admin/rules` - Rule engine management
- `/admin/users` - User management (admin only)
- `/admin/roles` - Role/permission management
<!-- slide -->
**API Routes** ([api.py](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/routes/api.py))
| Endpoint | Method | Returns |
|----------|--------|---------|
| `/api/products` | GET | All active products (JSON) |
| `/api/products/<id>` | GET | Single product details |
| `/api/brands` | GET | All brands |
| `/api/categories` | GET | All categories |
````

### 4.4 Expert System Services Architecture

```mermaid
flowchart LR
    subgraph Services["Business Logic Layer"]
        direction TB
        
        subgraph IE["InferenceEngine"]
            WM[Working Memory]
            RM[Rule Matching]
            EC[Evaluate Conditions]
        end
        
        subgraph RS["RecommendationService"]
            GR[get_recommendations]
            FP[_fetch_products]
            AR[_add_reasoning]
        end
        
        subgraph CS["ComparisonService"]
            C2P[compare_two_products]
            EP[extract_pros]
            EC2[extract_cons]
            CA[get_comparative_advantages]
            COS[calculate_overall_score]
        end
    end
    
    UserInput --> RS
    RS --> IE
    IE --> RM
    RM --> EC
    EC --> Products[(Products)]
    RS --> FP
    FP --> Products
    
    ProductIDs --> CS
    CS --> C2P
    C2P --> EP
    C2P --> EC2
    C2P --> CA
```

#### InferenceEngine - Forward Chaining Logic

The [InferenceEngine](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/services/inference_engine.py) implements forward-chaining inference:

1. **Add Facts**: User inputs are added to working memory
2. **Match Rules**: All active rules are evaluated against facts
3. **Evaluate Conditions**: Each rule condition is tested using operators (`==`, `!=`, `<`, `>`, `in`, `contains`)
4. **Return Matched Rules**: Rules sorted by priority (highest first)

```python
# Supported operators
operators = ['equals', 'not_equals', 'less_than', 'greater_than', 
             'less_equal', 'greater_equal', 'in', 'contains']
```

### 4.5 Authentication & Authorization Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Flask App
    participant LM as Flask-Login
    participant DB as Database
    participant RBAC as Role/Permission
    
    U->>F: POST /auth/login (credentials)
    F->>DB: Query User by username
    DB-->>F: User object
    F->>F: check_password(hash)
    alt Valid credentials
        F->>LM: login_user(user)
        LM->>LM: Set session cookie
        F-->>U: Redirect to /admin/dashboard
    else Invalid
        F-->>U: Flash "Invalid username or password"
    end
    
    Note over U,RBAC: Protected Route Access
    U->>F: GET /admin/products
    F->>LM: @login_required check
    LM->>F: current_user loaded
    F->>RBAC: has_permission('product.view')
    alt Has permission
        RBAC-->>F: True
        F-->>U: Render products page
    else No permission
        RBAC-->>F: False
        F-->>U: Flash error, redirect
    end
```

### 4.6 Error Handling & Validation

- **Form Validation**: WTForms validators (DataRequired, Email, Length, etc.)
- **CSRF Protection**: Flask-WTF CSRFProtect on all forms
- **Database Errors**: Try-catch with user-friendly flash messages
- **404 Handling**: `get_or_404()` for missing resources
- **Security Headers**: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection

---

## 5. Frontend Layer

### 5.1 Template Hierarchy

```
templates/
├── base.html              # Master layout with nav, footer, flash messages
├── auth/
│   ├── login.html         # Login form
│   └── register.html      # Registration form (admin-only)
├── user/
│   ├── home.html          # Landing page
│   ├── questionnaire.html # Recommendation form
│   ├── results.html       # Product recommendations
│   ├── compare.html       # Side-by-side specs (2-4 products)
│   ├── comparison_analysis.html  # Pros/cons (2 products)
│   └── product_detail.html       # Single product view
├── admin/
│   ├── dashboard.html     # Statistics overview
│   ├── products.html      # Product list
│   ├── product_form.html  # Add/edit product
│   ├── brands.html        # Brand management
│   ├── rules.html         # Rule list
│   ├── rule_form.html     # Add/edit rule
│   ├── users.html         # User management
│   └── roles.html         # Role management
└── components/
    └── (reusable partials)
```

### 5.2 Styling Architecture

- **Framework**: Tailwind CSS (utility-first)
- **Responsive**: Mobile-first breakpoints
- **Static Files**: Located in `app/static/css/`, `app/static/js/`

### 5.3 State Management

| Type | Mechanism | Usage |
|------|-----------|-------|
| Server Session | `session` object | User preferences, last questionnaire inputs |
| Form State | WTForms | CSRF tokens, validation state |
| URL State | Query parameters | Compare product IDs (`?ids=1,2,3`) |

---

## 6. Core User Workflows

### 6.1 Product Recommendation Flow

```mermaid
sequenceDiagram
    participant U as User
    participant QF as Questionnaire Form
    participant RS as RecommendationService
    participant IE as InferenceEngine
    participant DB as Database
    
    U->>QF: Fill questionnaire
    Note right of QF: category, budget,<br/>usage_type, brand
    QF->>RS: get_recommendations(user_inputs)
    RS->>IE: infer(user_inputs)
    IE->>DB: Query active rules<br/>(filtered by category)
    DB-->>IE: Rule list
    
    loop For each rule
        IE->>IE: evaluate_condition(condition, facts)
    end
    
    IE-->>RS: matched_rules (sorted by priority)
    RS->>DB: Query products<br/>(budget, category, brand filters)
    DB-->>RS: Product list
    RS->>RS: _add_reasoning(products, rules)
    RS-->>U: Render results.html<br/>(products with confidence scores)
```

**Request/Response Pattern**:
```
POST /recommend
├── Form Data: category, budget, usage_type, preferred_brand
└── Response: HTML (results.html) with:
    ├── products: [{id, name, brand, price, confidence, reasoning, ...}]
    ├── total_matches: int
    ├── fired_rules: int
    └── message: string
```

---

### 6.2 Product Comparison Flow (Pros & Cons)

```mermaid
sequenceDiagram
    participant U as User
    participant CP as Compare Page
    participant CS as ComparisonService
    participant DB as Database
    
    U->>CP: GET /compare-analysis?ids=1,2
    CP->>DB: Fetch products by IDs
    DB-->>CP: Product objects
    CP->>CS: compare_two_products(p1, p2, prefs)
    
    par Parallel Analysis
        CS->>CS: extract_pros(p1)
        CS->>CS: extract_pros(p2)
        CS->>CS: extract_cons(p1)
        CS->>CS: extract_cons(p2)
    end
    
    CS->>CS: get_comparative_advantages(p1, p2)
    CS->>CS: calculate_overall_score(p1)
    CS->>CS: calculate_overall_score(p2)
    CS->>CS: Determine winner & reason
    
    CS-->>CP: Comparison data
    CP-->>U: Render comparison_analysis.html
```

**Scoring Weights**:
| Factor | Weight | Description |
|--------|--------|-------------|
| Budget Alignment | 25% | Optimal at 80% of budget |
| Specification Quality | 40% | RAM, storage, premium features |
| Brand Preference | 10% | Match to user's preferred brand |
| Usage Type Alignment | 15% | Gaming, business optimization |

---

### 6.3 Admin Product Management Flow

```mermaid
sequenceDiagram
    participant A as Admin
    participant AF as Admin Form
    participant AR as Admin Routes
    participant DB as Database
    participant AL as AuditLog
    
    A->>AR: GET /admin/products/new
    AR->>A: Render product_form.html
    A->>AF: Fill product details + specs
    AF->>AR: POST /admin/products/new
    
    AR->>AR: Validate form (WTForms)
    alt Valid
        AR->>DB: Create Product
        AR->>DB: Create Specifications
        AR->>AL: Log "product.create"
        AR-->>A: Flash success, redirect
    else Invalid
        AR-->>A: Re-render form with errors
    end
```

---

## 7. Configuration Management

### 7.1 Environment Setup

Three configuration classes in [config.py](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/config.py):

| Config | DEBUG | Database | CSRF | Session Secure |
|--------|-------|----------|------|----------------|
| `DevelopmentConfig` | True | MySQL (from .env) | Enabled | False |
| `TestingConfig` | False | SQLite :memory: | Disabled | False |
| `ProductionConfig` | False | MySQL (from .env) | Enabled | True |

### 7.2 Key Environment Variables

```env
# Flask
SECRET_KEY=your-secret-key
FLASK_ENV=development

# Database
DB_HOST=localhost
DB_PORT=3307
DB_NAME=techadvisor
DB_USER=root
DB_PASSWORD=ROOT
DATABASE_URL=mysql+pymysql://root:ROOT@localhost:3307/techadvisor

# Security
SESSION_COOKIE_SECURE=False  # True in production
SESSION_COOKIE_HTTPONLY=True

# File Upload
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=app/static/uploads
```

---

## 8. Testing Architecture

### 8.1 Test Structure

```
tests/
├── conftest.py                # Fixtures: app, db, client, test data
├── test_models.py             # Model unit tests
├── test_routes.py             # Route integration tests
├── test_inference_engine.py   # Inference logic tests
├── test_recommendation_service.py  # Recommendation logic
└── test_comparison_service.py      # Comparison logic
```

### 8.2 Test Configuration

From [pytest.ini](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/pytest.ini):
- Uses in-memory SQLite for isolation
- Coverage reporting for `app/` package
- Markers: `unit`, `integration`, `slow`

### 8.3 Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_inference_engine.py

# By marker
pytest -m unit
```

---

## 9. Key Technical Decisions & Rationale

| Decision | Rationale |
|----------|-----------|
| **Flask over Django** | Lighter weight for expert system focus; more flexibility |
| **Forward-chaining inference** | Suitable for recommendation systems where goal is unknown |
| **Specification as key-value pairs** | Flexible schema for varying product attributes |
| **RBAC over simple role enum** | Future-proof for complex permission requirements |
| **Server-side rendering** | SEO-friendly, simpler state management |
| **MySQL over PostgreSQL** | Common WAMP/XAMPP stack compatibility |
| **Tailwind CSS** | Rapid UI development with utility classes |

---

## 10. Potential Bottlenecks & Improvement Areas

### 10.1 Performance Considerations

| Area | Current State | Recommendation |
|------|---------------|----------------|
| Rule Matching | Loads all rules, then filters | Add database-level category filtering |
| Product Specs | N+1 queries on list views | Use `joinedload()` for eager loading |
| Session Storage | Filesystem-based | Consider Redis for production |
| Static Assets | Served by Flask | Use CDN/Nginx in production |

### 10.2 Scalability Path

```mermaid
flowchart LR
    subgraph Current["Current (Monolith)"]
        Flask[Flask App]
    end
    
    subgraph Phase1["Phase 1: Optimization"]
        Flask2[Flask App]
        Redis[(Redis Cache)]
        Nginx[Nginx Static]
    end
    
    subgraph Phase2["Phase 2: Separation"]
        API[API Backend]
        FE[SPA Frontend]
        ES[Inference Service]
    end
    
    Current --> Phase1
    Phase1 --> Phase2
```

### 10.3 Feature Enhancement Opportunities

1. **Machine Learning Integration**: Replace/augment rule-based system with ML recommendations
2. **Real-time Updates**: WebSocket for live price/availability updates
3. **User Accounts**: Allow users to save comparisons and preferences
4. **Analytics Dashboard**: Track recommendation success rates
5. **API Authentication**: JWT tokens for third-party integrations

---

## 11. Dependency Overview

```mermaid
flowchart TD
    subgraph External["External Dependencies"]
        Flask[Flask 2.3.3]
        SQLAlchemy[Flask-SQLAlchemy]
        Migrate[Flask-Migrate]
        Login[Flask-Login]
        WTF[Flask-WTF]
        PyMySQL[PyMySQL]
        Pytest[Pytest]
    end
    
    subgraph Internal["Layer Dependencies"]
        Routes[Routes/Blueprints]
        Services[Services Layer]
        Models[Models/ORM]
        Forms[Forms Layer]
        Utils[Utilities]
    end
    
    Routes --> Services
    Routes --> Forms
    Routes --> Models
    Services --> Models
    Models --> SQLAlchemy
    SQLAlchemy --> PyMySQL
    Forms --> WTF
    Routes --> Login
```

---

## 12. Quick Reference

### Start Development Server
```bash
python run.py
# Runs on http://127.0.0.1:5001
```

### Default Credentials
| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Staff | `staff` | `staff123` |

### Key Files for Modification
| Area | File(s) |
|------|---------|
| Add new route | `app/routes/<blueprint>.py` |
| Add new model | `app/models/<model>.py` |
| Modify inference logic | `app/services/inference_engine.py` |
| Add comparison logic | `app/services/comparison_service.py` |
| Add form validation | `app/forms/<form>.py` |
| Add permission checks | `app/utils/decorators.py` |

---

*Document generated: January 20, 2026*
