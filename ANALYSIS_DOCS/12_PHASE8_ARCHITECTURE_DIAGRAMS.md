# PHASE 8 - ARCHITECTURE DIAGRAMS
**System Design, Layered Components, and Interactions**

---

## 1. SYSTEM ARCHITECTURE OVERVIEW

### 1.1 Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         PRESENTATION TIER (User Interface)              │   │
│  │                                                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │   │
│  │  │ Browser  │  │ Mobile   │  │ Admin    │             │   │
│  │  │ (HTML,   │  │ App      │  │ Panel    │             │   │
│  │  │ CSS, JS) │  │ (Future) │  │ (Flask   │             │   │
│  │  └─────┬────┘  └────┬─────┘  │ Routes)  │             │   │
│  │        │             │        └─────┬────┘             │   │
│  │        └─────────────┼──────────────┘                  │   │
│  │                      │ HTTP/HTTPS                      │   │
│  └──────────────────────┼──────────────────────────────────┘   │
│                         │                                       │
│                         │                                       │
│  ┌──────────────────────┼──────────────────────────────────┐   │
│  │  APPLICATION TIER (Business Logic)                      │   │
│  │                                                         │   │
│  │  ┌────────────────────────────────────────────────┐    │   │
│  │  │ Flask Application (app/)                       │    │   │
│  │  │                                                │    │   │
│  │  │  ┌──────────────────────────────────────────┐  │    │   │
│  │  │  │ Routes (Flask Blueprints)                │  │    │   │
│  │  │  │ ├─ /auth.py (login, register)           │  │    │   │
│  │  │  │ ├─ /user.py (questionnaire, results)    │  │    │   │
│  │  │  │ ├─ /admin.py (manage rules, products)   │  │    │   │
│  │  │  │ └─ /api.py (REST endpoints)             │  │    │   │
│  │  │  └──────────────────────────────────────────┘  │    │   │
│  │  │                    │                            │    │   │
│  │  │  ┌────────────────┴──────────────────────┐     │    │   │
│  │  │  │ Services (Python Classes)             │     │    │   │
│  │  │  │ ├─ inference_engine.py               │     │    │   │
│  │  │  │ │  └─ Forward-chaining execution     │     │    │   │
│  │  │  │ ├─ recommendation_service.py         │     │    │   │
│  │  │  │ │  └─ Product filtering & ranking    │     │    │   │
│  │  │  │ └─ comparison_service.py             │     │    │   │
│  │  │  │    └─ Product comparison logic       │     │    │   │
│  │  │  └────────────────┬─────────────────────┘     │    │   │
│  │  │                   │                            │    │   │
│  │  │  ┌────────────────┴──────────────────────┐     │    │   │
│  │  │  │ Forms & Validation (WTForms)         │     │    │   │
│  │  │  │ ├─ auth_forms.py                     │     │    │   │
│  │  │  │ ├─ recommendation_forms.py            │     │    │   │
│  │  │  │ └─ rule_forms.py                     │     │    │   │
│  │  │  └────────────────┬─────────────────────┘     │    │   │
│  │  │                   │                            │    │   │
│  │  │  ┌────────────────┴──────────────────────┐     │    │   │
│  │  │  │ Utils & Helpers                       │     │    │   │
│  │  │  │ ├─ decorators.py (auth checks)       │     │    │   │
│  │  │  │ └─ common utility functions          │     │    │   │
│  │  │  └────────────────┬─────────────────────┘     │    │   │
│  │  │                   │                            │    │   │
│  │  └───────────────────┼────────────────────────────┘    │   │
│  │                      │ SQLAlchemy ORM                  │   │
│  └──────────────────────┼──────────────────────────────────┘   │
│                         │                                       │
│                         │                                       │
│  ┌──────────────────────┼──────────────────────────────────┐   │
│  │  PERSISTENCE TIER (Data Storage)                        │   │
│  │                                                         │   │
│  │  ┌────────────────────────────────────────────────┐    │   │
│  │  │ Database (MySQL 8.0+)                         │    │   │
│  │  │                                                │    │   │
│  │  │  ┌──────────────────────────────────────────┐  │    │   │
│  │  │  │ Core Data Tables                         │  │    │   │
│  │  │  │                                          │  │    │   │
│  │  │  │  users              (user accounts)      │  │    │   │
│  │  │  │  products           (device catalog)     │  │    │   │
│  │  │  │  categories         (device types)       │  │    │   │
│  │  │  │  brands             (manufacturers)      │  │    │   │
│  │  │  │  specifications     (product features)   │  │    │   │
│  │  │  │                                          │  │    │   │
│  │  │  │  rules              (expert system)      │  │    │   │
│  │  │  │  rule_conditions    (rule logic)         │  │    │   │
│  │  │  │                                          │  │    │   │
│  │  │  │  roles              (authentication)     │  │    │   │
│  │  │  │  permissions        (authorization)      │  │    │   │
│  │  │  │  role_permissions   (RBAC mapping)       │  │    │   │
│  │  │  │                                          │  │    │   │
│  │  │  │  audit_logs         (compliance)         │  │    │   │
│  │  │  └──────────────────────────────────────────┘  │    │   │
│  │  │                                                │    │   │
│  │  └────────────────────────────────────────────────┘    │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ EXTERNAL SERVICES (Optional)                             │  │
│  │                                                          │  │
│  │  ├─ Redis (Caching layer)                              │  │
│  │  ├─ Datadog/New Relic (Monitoring)                     │  │
│  │  └─ AWS/Azure (Deployment)                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Architecture Benefits

```
THREE-TIER SEPARATION PROVIDES:

Presentation Tier:
  ✓ Decoupled from business logic
  ✓ Can update UI without touching backend
  ✓ Support multiple clients (web, mobile, API)
  ✓ Template-based rendering with Jinja2

Business Logic Tier:
  ✓ Centralized inference and recommendation
  ✓ Reusable services across routes
  ✓ Form validation before DB operations
  ✓ Authentication & authorization enforcement
  ✓ Error handling and logging

Persistence Tier:
  ✓ Single source of truth for all data
  ✓ Transaction support (ACID guarantees)
  ✓ Indexing for performance
  ✓ Audit logging for compliance
  ✓ Schema versioning with migrations
```

---

## 2. APPLICATION TIER - DETAILED COMPONENT BREAKDOWN

### 2.1 Routes (Flask Blueprints)

```
Flask Blueprint Architecture
════════════════════════════════════════════════════════════════

app/
├── __init__.py
│   └── create_app() → Flask app with blueprints registered
│
└── routes/
    ├── __init__.py
    │
    ├── auth.py (Blueprint: 'auth')
    │   ├── /register (GET/POST) → Registration form
    │   ├── /login (GET/POST) → Authentication
    │   ├── /logout → Invalidate session
    │   └── /forgot-password (optional) → Recovery
    │
    ├── user.py (Blueprint: 'user')
    │   ├── /home → User dashboard
    │   ├── /recommend (GET/POST) → Questionnaire form
    │   ├── /results → Display recommendations
    │   ├── /compare → Product comparison
    │   └── /product/<id> → Product detail page
    │
    ├── admin.py (Blueprint: 'admin')
    │   ├── /dashboard → Admin overview
    │   ├── /rules → Manage rules (list, create, edit, delete)
    │   ├── /products → Manage products
    │   ├── /users → Manage user accounts
    │   ├── /audit-log → View audit trail
    │   └── /categories → Manage categories
    │
    └── api.py (Blueprint: 'api')
        ├── /api/v1/products → REST GET
        ├── /api/v1/recommendations → REST POST
        ├── /api/v1/compare → REST comparison
        └── /api/v1/rules → REST admin operations


REQUEST FLOW EXAMPLE:
═════════════════════

User Questionnaire Submission:
  
  Browser: POST /recommend
    ↓
  Flask routing matches POST → routes/user.py
    ↓
  Function: recommend_post()
    ├─ Extract form data from request
    ├─ Validate CSRF token (security.decorators)
    ├─ Call: WTForms validation (forms/recommendation_forms.py)
    ├─ Call: validation_service.validate_budget_range()
    ├─ Call: InferenceEngine.infer(working_memory)
    │   └─ Database queries for rules, conditions
    ├─ Call: RecommendationService.rank_products()
    │   └─ Database queries for products, specifications
    ├─ Render template: results.html with context
    │   └─ Pass products, explanations, matched_rules
    └─ Return HTTP 200 with HTML
    
  Browser: Display results page
```

### 2.2 Services - Core Business Logic

```
Services Layer Architecture
════════════════════════════════════════════════════════════════

app/services/
│
├── __init__.py
│
├── inference_engine.py
│   │
│   └── InferenceEngine class
│       │
│       ├── __init__()
│       │   └─ Initialize rule cache (optional)
│       │
│       ├── infer(working_memory: dict) → List[Rule]
│       │   │
│       │   ├─ Query database for active rules
│       │   │   └─ SELECT * FROM rules WHERE is_active = TRUE
│       │   │
│       │   ├─ Load rule conditions (eager-load)
│       │   │   └─ joinedload('conditions')
│       │   │
│       │   ├─ For each rule:
│       │   │   └─ Evaluate all conditions
│       │   │       ├─ Condition: budget <= value?
│       │   │       ├─ Condition: usage_type in [...]?
│       │   │       ├─ Condition: brand matches?
│       │   │       └─ If ALL conditions match → add to matched_rules
│       │   │
│       │   └─ Return matched_rules sorted by priority
│       │
│       ├── evaluate_condition(condition, working_memory) → bool
│       │   │
│       │   ├─ Get condition: key, operator, value
│       │   ├─ Get fact: working_memory[key]
│       │   ├─ Apply operator:
│       │   │   ├─ == (equality)
│       │   │   ├─ != (not equal)
│       │   │   ├─ < (less than)
│       │   │   ├─ > (greater than)
│       │   │   ├─ <= (less than or equal)
│       │   │   ├─ >= (greater than or equal)
│       │   │   ├─ in (set membership)
│       │   │   └─ contains (substring)
│       │   │
│       │   └─ Return boolean result
│       │
│       └── [Cache methods - optional]
│           ├─ cache_rules()
│           └─ invalidate_cache()
│
├── recommendation_service.py
│   │
│   └── RecommendationService class
│       │
│       ├── get_recommendations(user_input: dict) → List[Product]
│       │   │
│       │   ├─ Call: InferenceEngine.infer()
│       │   │   └─ Output: matched_rules
│       │   │
│       │   ├─ Extract primary category from matched rules
│       │   │   └─ Find most common category_id
│       │   │
│       │   ├─ Query products by:
│       │   │   ├─ category_id (from rules)
│       │   │   ├─ budget <= max_price
│       │   │   ├─ is_active = TRUE
│       │   │   └─ ORDER BY price ASC LIMIT 20
│       │   │
│       │   ├─ Eager-load specifications for all products
│       │   │   └─ joinedload('specifications')
│       │   │
│       │   ├─ Calculate confidence for each product
│       │   │   └─ confidence = min(100, 50 + matched_rule.priority)
│       │   │
│       │   ├─ Sort products by (confidence DESC, price ASC)
│       │   │
│       │   └─ Return ranked products with confidence scores
│       │
│       ├── filter_by_budget(products, max_price) → List[Product]
│       │   └─ In-memory filter (already DB filtered)
│       │
│       ├── sort_by_value(products) → List[Product]
│       │   └─ Price+specs scoring
│       │
│       └─ generate_explanation(product, rules) → str
│           ├─ Check which rules matched for this category
│           ├─ Build explanation text
│           │   ├─ "Matched X recommendation rules"
│           │   ├─ "Confidence: Y%"
│           │   └─ "Key factors: Z"
│           └─ Return formatted explanation
│
└── comparison_service.py
    │
    └── ComparisonService class
        │
        ├── compare_two_products(product_a, product_b) → dict
        │   │
        │   ├─ Load full specs for both products
        │   │   └─ SELECT * FROM specifications WHERE product_id IN (a, b)
        │   │
        │   ├─ Extract specifications into dicts
        │   │   ├─ product_a_specs = {attr: value, ...}
        │   │   └─ product_b_specs = {attr: value, ...}
        │   │
        │   ├─ Call: extract_pros(product_a, product_b, specs)
        │   │   └─ Output: List[str] of advantages
        │   │
        │   ├─ Call: extract_cons(product_a, product_b, specs)
        │   │   └─ Output: List[str] of disadvantages
        │   │
        │   ├─ Call: score_products(product_a, product_b, specs)
        │   │   │
        │   │   ├─ Score dimensions:
        │   │   │   ├─ Budget (25%): price value
        │   │   │   ├─ Performance (40%): CPU, GPU, RAM
        │   │   │   ├─ Build (10%): materials, design
        │   │   │   ├─ Use case (15%): intended purpose
        │   │   │   └─ Value (10%): overall value
        │   │   │
        │   │   ├─ Calculate weighted score for each
        │   │   │   └─ total = sum(dimension_score × weight)
        │   │   │
        │   │   └─ Return scores (0-100 range)
        │   │
        │   └─ Return comparison dict with:
        │       ├─ product_a_score
        │       ├─ product_b_score
        │       ├─ winner (higher score)
        │       ├─ pros_a, cons_a
        │       ├─ pros_b, cons_b
        │       └─ explanation
        │
        ├── extract_pros(prod_a, prod_b, specs) → List[str]
        │   └─ Find advantages of prod_a vs prod_b
        │
        ├── extract_cons(prod_a, prod_b, specs) → List[str]
        │   └─ Find disadvantages of prod_a vs prod_b
        │
        └─ score_products(prod_a, prod_b, specs) → (float, float)
            └─ Weighted multi-criteria scoring
```

### 2.3 Forms - Input Validation

```
Forms Layer (WTForms)
════════════════════════════════════════════════════════════════

app/forms/
│
├── __init__.py
│
├── auth_forms.py
│   ├── LoginForm
│   │   ├─ username: StringField(validators=[DataRequired()])
│   │   ├─ password: PasswordField(validators=[DataRequired()])
│   │   └─ remember_me: BooleanField()
│   │
│   └── RegisterForm
│       ├─ username: StringField(validators=[...])
│       ├─ email: EmailField(validators=[...])
│       ├─ password: PasswordField(validators=[Length(8,)...])
│       └─ confirm_password: PasswordField(validators=[EqualTo('password')])
│
├── recommendation_forms.py
│   │
│   └── QuestionnaireForm
│       ├─ budget: IntegerField(
│       │     validators=[
│       │       DataRequired(),
│       │       NumberRange(min=0, max=10000)
│       │     ]
│       │  )
│       │ 
│       ├─ usage_type: SelectField(
│       │     choices=[
│       │       ('gaming', 'Gaming'),
│       │       ('business', 'Business'),
│       │       ('general', 'General'),
│       │       ('creative', 'Creative')
│       │     ]
│       │  )
│       │
│       ├─ preferred_brand: SelectField(
│       │     choices=[loaded from Brand table]
│       │  )
│       │
│       └─ category: SelectField(
│             choices=[loaded from Category table]
│          )
│
│
├── rule_forms.py
│   │
│   └── RuleForm
│       ├─ name: StringField(validators=[DataRequired()])
│       ├─ description: TextAreaField()
│       ├─ category_id: SelectField(choices=[loaded from DB])
│       ├─ priority: IntegerField(validators=[NumberRange(1, 100)])
│       ├─ conditions: FieldList(FormField(ConditionForm))
│       │   └─ ConditionForm:
│       │       ├─ key: SelectField(choices=[budget, usage_type, brand...])
│       │       ├─ operator: SelectField(choices=[==, !=, <, >, <=, >=, in])
│       │       └─ value: StringField()
│       └─ is_active: BooleanField()
│
│
├── product_forms.py
│   └── ProductForm
│       ├─ name: StringField()
│       ├─ category_id: SelectField()
│       ├─ brand_id: SelectField()
│       ├─ price: FloatField()
│       └─ is_active: BooleanField()
│
└── user_forms.py
    └── UserForm
        ├─ username: StringField()
        ├─ email: EmailField()
        └─ role_id: SelectField()


VALIDATION FLOW:
═════════════════

Form Submission (POST /recommend):
  
  1. Browser sends form data
  2. Flask receives request
  3. Create form object: form = QuestionnaireForm(request.form)
  4. Call: form.validate()
     │
     ├─ CSRF protection: Verify token
     ├─ For each field:
     │   ├─ Run validators in order
     │   ├─ budget: 
     │   │   ├─ DataRequired()? ✓
     │   │   └─ NumberRange(0, 10000)? ✓
     │   ├─ usage_type:
     │   │   └─ In valid choices? ✓
     │   └─ ... (repeat for all fields)
     │
     └─ If any validation fails:
         └─ Return form with error messages
  
  5. If validation passes (form.validate() == True):
     └─ Proceed to business logic
```

### 2.4 Models - Data Structure

```
Models (SQLAlchemy ORM)
════════════════════════════════════════════════════════════════

app/models/
│
├── __init__.py
│   └─ db = SQLAlchemy(app)
│
├── user.py
│   │
│   └── User model
│       ├─ id: Integer (primary key)
│       ├─ username: String (unique)
│       ├─ email: String (unique)
│       ├─ password_hash: String (bcrypt hashed)
│       ├─ created_at: DateTime (default: now)
│       ├─ updated_at: DateTime (default: now)
│       │
│       ├─ Relationships:
│       │   ├─ role_id → Role (foreign key)
│       │   └─ cascade options
│       │
│       └─ Methods:
│           ├─ set_password(password: str)
│           │   └─ Hash password with bcrypt
│           ├─ verify_password(password: str) → bool
│           │   └─ Compare hash
│           └─ has_permission(action: str) → bool
│               └─ Check RBAC permissions
│
├── product.py
│   │
│   └── Product model
│       ├─ id: Integer (primary key)
│       ├─ name: String
│       ├─ category_id: Integer (foreign key → Category)
│       ├─ brand_id: Integer (foreign key → Brand)
│       ├─ price: Float
│       ├─ description: Text
│       ├─ image_url: String
│       ├─ is_active: Boolean (default: True)
│       ├─ created_at: DateTime
│       │
│       ├─ Relationships:
│       │   ├─ category → Category (one-to-many reverse)
│       │   ├─ brand → Brand (one-to-many reverse)
│       │   └─ specifications → Specification (one-to-many)
│       │       └─ Back-populates: product
│       │
│       └─ Properties:
│           └─ specs_dict: Dict[str, str]
│               └─ Convert specifications to dict
│
├── rule.py
│   │
│   └── Rule model
│       ├─ id: Integer (primary key)
│       ├─ name: String
│       ├─ description: Text
│       ├─ category_id: Integer (foreign key)
│       ├─ priority: Integer (1-100)
│       ├─ is_active: Boolean
│       ├─ created_at: DateTime
│       ├─ created_by: Integer (foreign key → User)
│       │
│       ├─ Relationships:
│       │   └─ conditions → RuleCondition (one-to-many)
│       │       ├─ cascade delete
│       │       └─ back-populates: rule
│       │
│       └─ Methods:
│           ├─ add_condition(key, operator, value)
│           │   └─ Create RuleCondition and add to list
│           └─ toggle_active()
│               └─ Flip is_active and save
│
├── role.py
│   │
│   └── Role model
│       ├─ id: Integer
│       ├─ name: String (unique)
│       ├─ description: String
│       │
│       └─ Relationships:
│           ├─ users → User (one-to-many)
│           └─ permissions → Permission (many-to-many)
│               └─ Through: role_permissions
│
│
└── audit_log.py
    │
    └── AuditLog model
        ├─ id: Integer (primary key)
        ├─ user_id: Integer (foreign key → User)
        ├─ action: String (create, read, update, delete)
        ├─ table_name: String (which table modified)
        ├─ record_id: Integer (which record in table)
        ├─ details: JSON (before/after values)
        └─ timestamp: DateTime (when change occurred)
```

---

## 3. DATA FLOW & COMPONENT INTERACTIONS

### 3.1 Questionnaire to Recommendation Flow

```
COMPONENT INTERACTION DIAGRAM
════════════════════════════════════════════════════════════════

User Browser          Routes           Services           Database
    │                   │                 │                  │
    │ POST /recommend   │                 │                  │
    ├──────────────────→│                 │                  │
    │  (form data)      │                 │                  │
    │                   │ validate() ✓    │                  │
    │                   │                 │                  │
    │                   invokes:          │                  │
    │                   ├─InferenceEngine │                  │
    │                   │ .infer()        │                  │
    │                   │                 │ Query: rules,    │
    │                   │                 ├─────────────────→│
    │                   │                 │ conditions       │
    │                   │                 │←─────────────────┤
    │                   │                 │ (rules + conds)  │
    │                   │                 │                  │
    │                   │                 │ Evaluate all     │
    │                   │                 │ conditions       │
    │                   │                 │ (in-memory)      │
    │                   │                 │                  │
    │                   │                 │ Return matched   │
    │                   ├─────────────────┤ rules            │
    │                   │                 │                  │
    │                   invokes:          │                  │
    │                   ├─RecommendationSe│                  │
    │                   │ rvice.rank()    │                  │
    │                   │                 │ Query: products  │
    │                   │                 ├─────────────────→│
    │                   │                 │ (by category,    │
    │                   │                 │  price, active)  │
    │                   │                 │←─────────────────┤
    │                   │                 │ (product list)   │
    │                   │                 │                  │
    │                   │                 │ Query: specs     │
    │                   │                 ├─────────────────→│
    │                   │                 │ (batch load)     │
    │                   │                 │←─────────────────┤
    │                   │                 │ (ALL specs)      │
    │                   │                 │                  │
    │                   │                 │ Calculate scores │
    │                   │                 │ (in-memory)      │
    │                   │                 │                  │
    │                   │ Results returned│                  │
    │                   │ (products +     │                  │
    │                   ├─ scores)        │                  │
    │                   │                 │                  │
    │                   render_template() │                  │
    │                   (results.html)    │                  │
    │                   │                 │                  │
    │ ←──────────────── HTTP 200 ────────┤                  │
    │   (HTML page)     │                 │                  │
    │                   │                 │                  │
    Display results     │                 │                  │
    │                   │                 │                  │


TIMING BREAKDOWN:
  Database queries:       45 ms
  Inference:              7 ms
  Ranking & scoring:      8 ms
  Template rendering:     50 ms
  Network transmission:   100 ms
  Browser rendering:      200 ms
  ────────────────────────────
  TOTAL PERCEIVED TIME:   410 ms
```

### 3.2 Admin Rule Creation Flow

```
ADMIN COMPONENT INTERACTION
════════════════════════════════════════════════════════════════

Admin Browser        Routes           Services/Forms       Database
    │                  │                   │                  │
    │ POST /rules/add  │                   │                  │
    ├─────────────────→│                   │                  │
    │ (form data)      │                   │                  │
    │                  │ WTForms.validate()│                  │
    │                  │                   │                  │
    │                  invoke RuleForm     │                  │
    │                  │                   │                  │
    │                  ├──────────────────→│ Validate all     │
    │                  │                   │ fields:          │
    │                  │                   │ - name (required)│
    │                  │                   │ - priority (1-100│
    │                  │                   │ - conditions     │
    │                  │                   │   (valid ops?)   │
    │                  │                   │←──────────────────
    │                  │                   │ form.errors = {} │
    │                  │                   │ (valid)          │
    │                  │                   │                  │
    │                  START TRANSACTION   │                  │
    │                  │                   │                  │
    │                  INSERT rule         │                  │
    │                  │                   ├─────────────────→│
    │                  │                   │ INSERT INTO rules│
    │                  │                   │ (name, priority..│
    │                  │                   │←─────────────────┤
    │                  │                   │ rule_id = 15     │
    │                  │                   │                  │
    │                  FOR each condition: │                  │
    │                  INSERT condition    │                  │
    │                  │                   ├─────────────────→│
    │                  │                   │ INSERT INTO cond │
    │                  │                   │ (rule_id, key..  │
    │                  │                   │←─────────────────┤
    │                  │                   │ cond_id = 127    │
    │                  │                   │                  │
    │                  INSERT audit log    │                  │
    │                  │                   ├─────────────────→│
    │                  │                   │ INSERT audit_logs│
    │                  │                   │ (user, action..  │
    │                  │                   │←─────────────────┤
    │                  │                   │ OK               │
    │                  COMMIT TRANSACTION  │                  │
    │                  │                   │                  │
    │ ←────────────────── HTTP 302 ─────────                 │
    │   REDIRECT /rules │                   │                  │
    │                  │                   │                  │
    Display success    │                   │                  │
    notification       │                   │                  │


TRANSACTION GUARANTEES:
  All or nothing: Either all inserts succeed or all rollback
  If error mid-transaction: Database reverts to pre-INSERT state
  Audit log: Always inserted (even if rule creation fails info tracked)
  Consistency: rule_id FK references always valid
```

---

## 4. DEPLOYMENT ARCHITECTURE

### 4.1 Development Environment

```
DEVELOPMENT SETUP
════════════════════════════════════════════════════════════════

Developer Machine:
  ├─ Python 3.11
  ├─ Virtual environment (.venv/)
  ├─ Flask development server (localhost:5000)
  │   └─ Auto-reload on file changes
  ├─ SQLite database (dev.db)
  │   └─ Fast, file-based, no server needed
  ├─ Redis (optional, for testing cache)
  └─ Git repository

run.py:
  ├─ Load environment variables from .env
  ├─ Create Flask app with create_app()
  ├─ Set debug=True
  └─ Run on localhost:5000

Typical workflow:
  1. source .venv/Scripts/activate
  2. python run.py
  3. Open browser: http://localhost:5000
  4. Test features locally
  5. Commit changes to git
```

### 4.2 Production Environment

```
PRODUCTION DEPLOYMENT ARCHITECTURE
════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────┐
│                  LOAD BALANCER (Optional)                │
│              (AWS ELB, Nginx, or similar)                │
│                                                          │
│  Routes traffic across multiple app servers             │
│  Enables zero-downtime deployments                      │
│  Distributes load for scale                             │
└──────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼

┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ APP SERVER 1     │ │ APP SERVER 2     │ │ APP SERVER N     │
│                  │ │                  │ │                  │
│ Gunicorn/WSGI    │ │ Gunicorn/WSGI    │ │ Gunicorn/WSGI    │
│  Flask app       │ │  Flask app       │ │  Flask app       │
│  (Python 3.11)   │ │  (Python 3.11)   │ │  (Python 3.11)   │
│                  │ │                  │ │                  │
│  Handles:        │ │  Handles:        │ │  Handles:        │
│  - Routes        │ │  - Routes        │ │  - Routes        │
│  - Inference     │ │  - Inference     │ │  - Inference     │
│  - Forms         │ │  - Forms         │ │  - Forms         │
│  - RBAC checks   │ │  - RBAC checks   │ │  - RBAC checks   │
│                  │ │                  │ │                  │
└────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────┐
         │  MySQL Database (Primary)          │
         │                                    │
         │  Replication (optional):           │
         │  - Master-Slave setup              │
         │  - Read replicas for queries       │
         │  - Write to master only            │
         │                                    │
         │  Connection Pool:                  │
         │  - 10 connections per app          │
         │  - Max 50+ concurrent              │
         │  - Retry logic for exhaustion      │
         │                                    │
         │  Backup:                           │
         │  - Daily snapshots                 │
         │  - Point-in-time recovery          │
         └────────────────────────────────────┘
                              │
         ┌────────────────────┴────────────────────┐
         │                                         │
         ▼                                         ▼
         
┌─────────────────────┐                 ┌──────────────────────┐
│ Redis Cache (opt)   │                 │ Monitoring/Logging   │
│                     │                 │                      │
│ Stores:             │                 │ Datadog/New Relic    │
│ - Rule cache        │                 │ - Metrics            │
│ - Product cache     │                 │ - Logs               │
│ - Session data      │                 │ - Alerts             │
│ - Query results     │                 │ - Dashboards         │
│                     │                 │                      │
│ TTL: Based on data  │                 │ CloudWatch (AWS)     │
│ Invalidation:       │                 │ - Application logs   │
│ - On rule change    │                 │ - Error tracking     │
│ - On product update │                 │ - Performance trace  │
└─────────────────────┘                 └──────────────────────┘


DEPLOYMENT OPTIONS:

Option 1: Docker + Kubernetes
  ├─ Containerize Flask app
  ├─ Push to registry (Docker Hub, ECR)
  ├─ Deploy to K8s cluster
  ├─ Auto-scaling by CPU/memory
  └─ Blue-green deployments

Option 2: AWS EC2 + RDS
  ├─ EC2 instances for Flask app
  ├─ RDS for managed MySQL database
  ├─ ElastiCache for Redis
  ├─ ALB for load balancing
  └─ Auto Scaling Group

Option 3: Heroku (simple)
  ├─ Git push to deploy
  ├─ Managed PostgreSQL (or MySQL addon)
  ├─ Built-in load balancing
  └─ Scaling with dynos

Option 4: Traditional VM
  ├─ On-premises or cloud VM
  ├─ Manual deployment
  ├─ Nginx reverse proxy
  ├─ Systemd service management
  └─ Manual scaling
```

### 4.3 Scaling Strategy

```
HORIZONTAL SCALING
════════════════════════════════════════════════════════════════

Problem: Single server hitting capacity
Solution: Add more servers behind load balancer

Load Distribution:
  Request 1 → Server A (inference + query)
  Request 2 → Server B (inference + query)
  Request 3 → Server C (inference + query)
  Request 4 → Server A (round-robin)
  
  All servers share:
  - Same database (MySQL)
  - Same cache (Redis) - optional
  - Same code base

Scaling triggers:
  ├─ CPU > 70% → Add 1 server
  ├─ Memory > 80% → Increase instance size
  ├─ Database connections > 80% → Add read replicas
  └─ Response time > 1000ms → Optimize or scale

Benefits:
  ✓ Increased throughput
  ✓ Better reliability (if one fails, others handle load)
  ✓ Zero-downtime deployments (stop one, update, restart)
  ✓ A/B testing (canary deployments)

Challenges:
  ✗ Session management (use Redis or DB for sessions)
  ✗ Database becomes bottleneck
  ✗ Increased cost
  ✗ Debugging distributed systems harder


VERTICAL SCALING
════════════════════════════════════════════════════════════════

Solution: Make single server more powerful

Upgrades:
  ├─ Add CPU cores (better inference)
  ├─ Add RAM (more processes, bigger cache)
  ├─ SSD storage (faster database access)
  └─ Faster network (better database connectivity)

Downside:
  ✗ More expensive per resource
  ✗ Single point of failure
  ✗ Eventually hits limits (physical constraints)

When to use:
  - Application not multi-threaded
  - Database is most expensive resource
  - Easier to manage than horizontal scaling
```

---

## 5. INTERACTION PATTERNS

### 5.1 User Authentication Flow

```
AUTHENTICATION ARCHITECTURE
════════════════════════════════════════════════════════════════

Flask-Login Integration:

User Registration:
  1. Browser: GET /register
  2. Flask: render register.html (form)
  3. User: Fills username, email, password
  4. Browser: POST /register with credentials
  5. Flask:
     ├─ Validate form data
     ├─ Hash password with bcrypt
     ├─ INSERT user into database
     ├─ CREATE session
     └─ Redirect to /home

User Login:
  1. Browser: GET /login
  2. Flask: render login.html (form)
  3. User: Enters credentials
  4. Browser: POST /login
  5. Flask:
     ├─ Validate CSRF token
     ├─ Query user by username
     ├─ Verify password hash
     ├─ CREATE session (set flask-login current_user)
     ├─ Store session in cookie or Redis
     └─ Redirect to referrer or /home

Session Management:
  ├─ Session cookie sent with every request
  ├─ Flask-Login checks: @login_required decorator
  ├─ If logged in: current_user available
  ├─ If not logged in: Redirect to /login
  └─ Session timeout: After X minutes (configurable)

Logout:
  1. User: Click [Logout]
  2. Browser: GET /logout
  3. Flask:
     ├─ Clear session
     ├─ Remove login cookie
     └─ Redirect to /login

Security Features:
  ├─ Password hashing: bcrypt (salt + hash)
  ├─ CSRF protection: Flask-WTF token on forms
  ├─ Session tokens: Secure, HTTP-only cookies
  ├─ Rate limiting: (optional) Brute-force protection
  └─ HTTPS: Encrypt in-flight data


RBAC (Role-Based Access Control)
════════════════════════════════════════════════════════════════

Architecture:

  User → Role(s) → Permission(s)
  
  Examples:
  - User 'lisa' → Role 'marketing_staff' → Perms [rule.create, rule.edit]
  - User 'john' → Role 'admin' → Perms [*.create, *.edit, *.delete]
  - User 'sarah' → Role 'user' → Perms [view_results, save_results]

Implementation:

Role table:
  id, name (admin, user, marketing_staff, analyst)
  
Permission table:
  id, action (rule.create, rule.edit, rule.delete, product.view, ...)
  
RolePermission table:
  role_id, permission_id (join table)

Check permission:
  if not current_user.has_permission('rule.create'):
    abort(403)  # Forbidden

Decorator usage in routes:
  @app.route('/admin/rules/add', methods=['POST'])
  @login_required
  @require_permission('rule.create')
  def add_rule():
    # Only users with 'rule.create' permission can reach here
    ...
```

### 5.2 Error Handling Architecture

```
ERROR HANDLING STRATEGY
════════════════════════════════════════════════════════════════

Layers:

1. INPUT VALIDATION (Forms)
   └─ Catch errors before business logic
      ├─ Empty fields
      ├─ Invalid types
      ├─ Out-of-range values
      ├─ If validation fails: Return form with error messages
      └─ Example: Budget must be 0-10000

2. BUSINESS LOGIC ERRORS (Services)
   └─ Catch errors during processing
      ├─ DATABASE ERRORS:
      │  ├─ Connection timeout → Use cached data, return 503
      │  ├─ Query slow → Log, monitor, may implement retry
      │  └─ FK constraint violated → Should not happen (validation)
      │
      ├─ INFERENCE ERRORS:
      │  ├─ No rules matched → Return generic products
      │  ├─ Conflicting conditions → Skip rule, log warning
      │  └─ Invalid condition operator → Log, skip condition
      │
      └─ COMPARISON ERRORS:
          ├─ Product not found → Return 404
          ├─ Missing specifications → Use defaults, warn
          └─ Scoring error → Use fallback score

3. CONTROLLER ERRORS (Routes)
   └─ Catch errors from services
      ├─ 404 Not Found (product doesn't exist)
      ├─ 403 Forbidden (permission denied)
      ├─ 400 Bad Request (invalid input)
      ├─ 500 Internal Server Error (unexpected error)
      └─ 503 Service Unavailable (database down)

4. GLOBAL ERROR HANDLERS
   └─ Catch all unhandled errors
      ├─ Log error with context
      ├─ Return user-friendly error page
      └─ Notify admin via alert


ERROR RECOVERY PATTERNS
════════════════════════════════════════════════════════════════

Try/Except blocks:

  try:
    recommendations = inference_engine.infer(user_input)
  except DatabaseTimeoutError as e:
    logger.error(f"Database timeout: {e}")
    cached_rules = cache.get('rules:all')
    if cached_rules:
      # Use cache as fallback
      recommendations = cached_rules
    else:
      # No cache, return error page
      return render_template('error.html', 
        message="System busy, please try again...")
  except Exception as e:
    logger.critical(f"Unexpected error: {e}", exc_info=True)
    sentry.capture_exception(e)  # Alert admin
    return render_template('error.html', message="Internal error")


Graceful Degradation:

  Level 1 (Best): Fresh database data
  Level 2 (Good): Cached database data
  Level 3 (Acceptable): Generic recommendations
  Level 4 (Worst case): Error page


Monitoring & Alerting:

  ├─ Error logging (file, console, centralized)
  ├─ Error tracking (Sentry, Datadog)
  ├─ Alerts on critical errors
  │  ├─ Threshold: > 10 errors/min
  │  ├─ Action: Page admin, auto-scale
  │  └─ Escalation: If continues > 5 min
  └─ Error dashboards
     └─ Trend analysis, root cause identification
```

---

## 6. TECHNOLOGY STACK DIAGRAM

```
COMPLETE TECHNOLOGY STACK
════════════════════════════════════════════════════════════════

FRONTEND
  ├─ HTML5 (Semantic markup)
  ├─ CSS3 (Tailwind, custom styling)
  ├─ JavaScript (Vanilla, no framework for simplicity)
  │   ├─ Form validation on client
  │   ├─ Interactive slider/dropdown
  │   ├─ AJAX calls (optional for dynamic loading)
  │   └─ Event listeners (click, change, submit)
  │
  └─ Jinja2 Templates (Server-side rendering)
      ├─ Form rendering
      ├─ Loop over products
      ├─ Conditional display
      └─ Inheritance (base.html)

BACKEND

Framework:
  └─ Flask 2.3.3
      ├─ Routing (@app.route)
      ├─ Blueprints (modular routes)
      ├─ Session management (Flask-Login)
      ├─ CSRF protection (Flask-WTF)
      └─ Template rendering (Jinja2)

Database ORM:
  └─ SQLAlchemy 2.0
      ├─ Declarative models
      ├─ Relationships (one-to-many, many-to-many)
      ├─ Query API (filter, order_by, limit)
      ├─ Connection pooling
      ├─ Eager loading (joinedload)
      └─ Lazy loading (on-demand)

Forms:
  └─ WTForms 3.0
      ├─ Field types (StringField, IntegerField, SelectField)
      ├─ Validators (DataRequired, Length, NumberRange)
      ├─ CSRF protection (CSRF token)
      └─ Error messages

Data Validation:
  └─ Marshmallow (optional, for APIs)
      ├─ Serialization (object → JSON)
      ├─ Deserialization (JSON → object)
      └─ Validation rules per field

Authentication:
  └─ Flask-Login 0.6
      ├─ Login manager
      ├─ UserMixin (default user impl)
      ├─ @login_required decorator
      └─ current_user context

PERSISTENCE

Database:
  └─ MySQL 8.0+
      ├─ InnoDB engine (ACID transactions)
      ├─ 11 tables (users, products, rules, etc)
      ├─ 20+ indexes (optimized queries)
      ├─ Foreign keys (referential integrity)
      └─ Cascading deletes

Migrations:
  └─ Alembic (database version control)
      ├─ Manage schema changes
      ├─ Generate migration scripts
      ├─ Backward compatibility
      └─ Timestamp tracking

Caching (Optional):
  └─ Redis
      ├─ Cache rules (TTL: 1 hour)
      ├─ Cache products (TTL: 2 hours)
      ├─ Store sessions (optional)
      └─ Invalidate on data changes

TESTING

Unit Testing:
  └─ Pytest
      ├─ Test models
      ├─ Test services
      ├─ Test forms
      ├─ Fixtures for setup/teardown
      └─ Mocking external dependencies

Integration Testing:
  └─ Pytest with Flask test client
      ├─ Test routes (GET, POST)
      ├─ Test form submission
      ├─ Test database operations
      └─ Test error handling

DEPLOYMENT

Container:
  └─ Docker (optional)
      ├─ Dockerfile
      ├─ requirements.txt
      ├─ docker-compose.yml (with MySQL)
      └─ Image registry (Docker Hub, ECR)

WSGI Server:
  └─ Gunicorn (production)
      ├─ Multiple workers (e.g., 4 workers)
      ├─ Listen on port 8000
      ├─ Graceful shutdown
      └─ Hot reload (development only)

Reverse Proxy:
  └─ Nginx
      ├─ Listens on port 80/443
      ├─ Routes to Gunicorn
      ├─ Static file serving
      ├─ SSL/TLS termination
      └─ Load balancing

Process Manager:
  └─ Systemd (Linux) or Supervisor
      ├─ Start/stop/restart Gunicorn
      ├─ Auto-restart on crash
      ├─ Log rotation
      └─ Health checks

MONITORING

Metrics & Logging:
  ├─ Datadog / New Relic
  │  ├─ Response time
  │  ├─ Error rate
  │  ├─ Database latency
  │  ├─ Cache hit rate
  │  └─ Custom metrics
  │
  ├─ CloudWatch (AWS)
  │  ├─ Application logs
  │  ├─ Database logs
  │  └─ Alarm triggers
  │
  └─ Sentry (error tracking)
      ├─ Exception aggregation
      ├─ Stack trace
      ├─ Context (user, browser)
      └─ Alerts

VERSION CONTROL:
  └─ Git
      ├─ GitHub / GitLab / Bitbucket
      ├─ Branches (main, develop, feature)
      ├─ Pull requests (code review)
      └─ CI/CD integration

DEVELOPMENT TOOLS:
  ├─ Python 3.11
  ├─ Virtual environment (venv)
  ├─ Package manager (pip)
  ├─ Linter (pylint, flake8)
  ├─ Formatter (black, autopep8)
  ├─ IDE (VS Code, PyCharm)
  ├─ Browser DevTools (F12)
  └─ SQL IDE (DataGrip, MySQL Workbench)


DEPLOYMENT PIPELINE:
═════════════════════

  Git commit → GitHub → CI/CD Pipeline
      │
      ├─ Lint code
      ├─ Run tests
      ├─ Build Docker image
      ├─ Push to registry
      ├─ Deploy to staging
      ├─ Run smoke tests
      ├─ If successful: Deploy to production
      └─ Monitor for errors
```

---

## 7. PERFORMANCE OPTIMIZATION ARCHITECTURE

```
OPTIMIZATION LAYERS
════════════════════════════════════════════════════════════════

LAYER 1: Database Level

Indexing:
  CREATE INDEX idx_rules_priority 
    ON rules(is_active, priority DESC);
  
  CREATE INDEX idx_products_category_price 
    ON products(category_id, price, is_active);
  
  CREATE INDEX idx_specs_product_id 
    ON specifications(product_id);

Benefits:
  ├─ Rules query: 7ms (vs 500ms without index)
  ├─ Products query: 8ms (vs 200ms without)
  └─ Specs query: 5ms (vs 150ms without)

Query Optimization:
  ├─ Eager loading (joinedload) to avoid N+1
  ├─ Batch queries (WHERE IN clause)
  ├─ Limit results (LIMIT 20 instead of LIMIT 1000)
  └─ Select only needed columns

Connection Pool:
  ├─ Reuse connections (don't create new for each query)
  ├─ Max pool size: 10-20 per app server
  ├─ Retry logic if exhausted
  └─ Monitor pool health


LAYER 2: Application Level

Caching:
  ├─ Cache rules (change rarely, loaded frequently)
  │  └─ TTL 1 hour, invalidate on rule change
  │
  ├─ Cache products (change occasionally)
  │  └─ TTL 2 hours, invalidate on product change
  │
  ├─ Cache specifications (change rarely)
  │  └─ TTL 24 hours
  │
  └─ Session cache (user login state)
     └─ TTL per session timeout

In-Memory Caching:
  ├─ Working memory (during single request)
  ├─ Inference results (don't re-infer same input)
  └─ Template compilation (cached for reuse)

Lazy Loading Strategy:
  ├─ Load rules: Only when needed (on POST /recommend)
  ├─ Load products: Only after inference (not on page load)
  ├─ Load specs: Batch load with products
  └─ Load user roles: Cache after login


LAYER 3: Network Level

Compression:
  ├─ Gzip HTML response (85KB → 20KB)
  ├─ Minify CSS (50KB → 15KB)
  ├─ Minify JavaScript (30KB → 10KB)
  └─ Compress images (JPEG with quality 85)

CDN for Static Assets:
  ├─ Serve CSS from CloudFront/Cloudflare
  ├─ Serve JS from CDN
  ├─ Serve images from CDN
  └─ Benefits: Geographic redundancy, faster load

HTTP Caching Headers:
  ├─ Cache-Control: max-age=3600 (for static assets)
  ├─ ETag: For cache validation
  ├─ Last-Modified: For conditional requests
  └─ 304 Not Modified: No re-download if unchanged

Connection Reuse:
  ├─ Keep-Alive HTTP (HTTP/1.1)
  ├─ HTTP/2 multiplexing (parallel requests)
  ├─ Browser connection pool
  └─ Reduce handshake overhead


LAYER 4: Client (Browser) Level

Render Optimization:
  ├─ Critical CSS (above-the-fold inline)
  ├─ Defer JavaScript (load after page render)
  ├─ Lazy load images (load on scroll)
  └─ Virtual scrolling (for long product lists)

Caching:
  ├─ LocalStorage for form state
  ├─ SessionStorage for temp data
  ├─ Service Workers (offline fallback)
  └─ Application cache

Reduce Paint Operations:
  ├─ Batch DOM updates
  ├─ Avoid layout thrashing
  ├─ Use CSS transforms (GPU acceleration)
  └─ Efficient event listeners (event delegation)


MONITORING PERFORMANCE
════════════════════════════════════════════════════════════════

Key Metrics:

Response Time (P50, P95, P99):
  ├─ Target P50: 300-400ms
  ├─ Target P95: 600-800ms
  ├─ Target P99: 1000-1500ms
  
Database Latency:
  ├─ Target P50: 40ms
  ├─ Alert P95: > 200ms
  ├─ Problem P99: > 500ms
  
Error Rate:
  ├─ Target: < 0.1%
  ├─ Alert: > 1%
  ├─ Critical: > 5%
  
Throughput:
  ├─ Requests per second (RPS)
  ├─ Target: 100 RPS per server
  ├─ Scale at: 80% capacity
  
Cache Hit Rate:
  ├─ Target: > 80%
  ├─ Monitor: Redis hit/miss ratio
  ├─ Improve: Increase TTL or add more caching

Tools:
  ├─ Datadog APM (application monitoring)
  ├─ New Relic (detailed performance breakdown)
  ├─ CloudWatch (AWS metrics)
  ├─ Lighthouse (frontend performance)
  └─ WebPageTest (synthetic monitoring)
```

---

## 8. SECURITY ARCHITECTURE

```
SECURITY LAYERS
════════════════════════════════════════════════════════════════

1. NETWORK SECURITY

HTTPS/TLS:
  ├─ All traffic encrypted (except development)
  ├─ Certificate from Let's Encrypt (free, auto-renew)
  ├─ TLS 1.2+ only (disable older versions)
  ├─ Forward secrecy (ephemeral key exchange)
  └─ HSTS header (force HTTPS)

Firewall Rules:
  ├─ Allow public: Port 80 (HTTP redirect), 443 (HTTPS)
  ├─ Allow admin: SSH port 22 (restricted IP)
  ├─ Deny: Direct database access from internet
  ├─ Database firewall: Only app servers
  └─ Cache firewall: Only app servers

DDoS Protection:
  ├─ CloudFlare / AWS Shield
  ├─ Rate limiting (API endpoints)
  ├─ IP blocking for abuses
  └─ Geographic filtering (optional)


2. APPLICATION SECURITY

Authentication:
  ├─ Passwords hashed with bcrypt (salt + iterations)
  ├─ Session tokens (secure, random, HTTP-only cookies)
  ├─ Multi-factor authentication (optional, future)
  └─ Password requirements (min 8 chars, complex)

Authorization (RBAC):
  ├─ Every protected route checks: @login_required
  ├─ Permission checks: @require_permission('action')
  ├─ Database-backed roles (can change without code)
  └─ Audit log of all actions

CSRF Protection:
  ├─ CSRF tokens on all forms (Flask-WTF)
  ├─ Token validation on form submission
  ├─ SameSite cookie (prevent cross-site requests)
  └─ Regenerate token per session

Form Validation:
  ├─ Server-side validation (not just client)
  ├─ Type checking (int, string, enum)
  ├─ Range checks (0-10000 for budget)
  ├─ Whitelist operator values (==, !=, <, >, <=, >=, in)
  └─ Prevent SQL injection with parameterized queries

SQL Injection Prevention:
  ├─ SQLAlchemy ORM (automatic parameterization)
  ├─ Prepared statements (no string concatenation)
  ├─ Input validation (whitelist operators)
  ├─ Never use raw SQL with user input
  └─ Regular security audits


3. DATA SECURITY

Database:
  ├─ Encryption at rest (AWS RDS encryption)
  ├─ Backups encrypted
  ├─ Access control (restricted to app servers)
  ├─ Audit logging (WHO accessed WHAT WHEN)
  └─ Masking sensitive data in logs

Session Data:
  ├─ Session cookie: Secure, HttpOnly, SameSite
  ├─ Session storage: Redis (encrypted) or DB
  ├─ Session timeout: 30 minutes inactivity
  ├─ Clear session on logout
  └─ Prevent session fixation attacks

Sensitive Data:
  ├─ Never log passwords (even hashed)
  ├─ Never log credit card numbers
  ├─ Mask PII in error messages
  ├─ Encrypt PII if stored
  └─ Comply with GDPR/CCPA (right to be forgotten)


4. MONITORING & INCIDENT RESPONSE

Logging:
  ├─ Application logs (info, warning, error, critical)
  ├─ Access logs (who accessed what)
  ├─ Audit logs (all data modifications)
  ├─ Security logs (failed logins, permission denies)
  └─ Centralized logging (ELK stack, CloudTrail)

Intrusion Detection:
  ├─ Monitor for brute-force login attempts
  ├─ Alert on unusual database queries
  ├─ Detect SQL injection patterns
  ├─ Identify privilege escalation attempts
  └─ Geo-blocking suspicious IPs

Incident Response:
  ├─ Defined playbook (what to do if hacked)
  ├─ Backup recovery procedures
  ├─ Data breach notification plan
  ├─ Post-mortem analysis
  └─ Continuous improvement


5. COMPLIANCE

Standards:
  ├─ OWASP Top 10 (web security best practices)
  ├─ GDPR (if European users)
  ├─ CCPA (if California users)
  ├─ PCI DSS (if handling payment cards)
  └─ SOC 2 (if enterprise customers)

Privacy:
  ├─ Privacy policy (clear, updated)
  ├─ Terms of service
  ├─ Data retention policy
  ├─ User consent (for tracking)
  └─ Right to data export/deletion

Documentation:
  ├─ Security policies
  ├─ Incident response procedures
  ├─ Backup/restore procedures
  ├─ Access control matrix
  └─ Regular training for developers
```

---

## 9. ARCHITECTURE SUMMARY

```
LAYERED SYSTEM OVERVIEW
════════════════════════════════════════════════════════════════

                    USER BROWSER
                        │
                        │ HTTP/HTTPS
                        ▼
            ┌─────────────────────────┐
            │   WEB TIER              │
            │  (Presentation Layer)   │
            ├─────────────────────────┤
            │ Jinja2 Templates        │
            │ HTML/CSS/JavaScript     │
            │ Form Rendering          │
            └────────┬────────────────┘
                     │
                     │ Flask Routing
                     ▼
            ┌─────────────────────────┐
            │  APP TIER               │
            │ (Business Logic Layer)  │
            ├─────────────────────────┤
            │ Flask Routes            │
            │ WTForms Validation      │
            │ Business Services:      │
            │ -InferenceEngine        │
            │ -RecommendationService  │
            │ -ComparisonService      │
            │ RBAC & Auth Decorators  │
            └────────┬────────────────┘
                     │
        ┌────────────┼────────────────┐
        │            │                │
        ▼            ▼                ▼
    ┌────────┐ ┌─────────┐   ┌──────────┐
    │ MySQL  │ │ Redis   │   │ Datadog  │
    │        │ │ Cache   │   │ Logging  │
    └────────┘ └─────────┘   └──────────┘
        │
        │ SQLAlchemy ORM
        ▼
    ┌──────────────────────────────┐
    │  DATA TIER                   │
    │  (Persistence Layer)         │
    ├──────────────────────────────┤
    │  MySQL Database              │
    │  11 Tables                   │
    │  20+ Indexes                 │
    │  Foreign Keys (Referential)  │
    │  ACID Transactions           │
    └──────────────────────────────┘


Key Design Principles:

✓ Separation of Concerns
  - Presentation (templates) ≠ Business Logic (services) ≠ Data (ORM)
  - Each layer has single responsibility
  - Easy to test, maintain, change

✓ Scalability
  - Horizontal scaling (load balancer + multiple servers)
  - Vertical scaling (bigger server)
  - Caching layer to reduce database load
  - Database replication for read scaling

✓ Reliability
  - ACID transactions (data consistency)
  - Error handling & graceful degradation
  - Audit logging (track all changes)
  - Health checks & monitoring

✓ Security
  - HTTPS/TLS encryption
  - Authentication (login, sessions)
  - Authorization (RBAC)
  - CSRF protection, SQL injection prevention

✓ Maintainability
  - Modular code (Blueprints, Services)
  - Clear naming conventions
  - Documentation & comments
  - Version control (Git)
```

---

## Document Metadata
- **Created**: PHASE 8 - Architecture Diagrams
- **Scope**: Complete system architecture, components, interactions
- **Diagrams**: 25+ ASCII & detailed flow diagrams
- **Technology Stack**: Documented with justification
- **Deployment**: Development through production
- **Security**: All major layers covered
- **Performance**: Optimization strategies for 5 layers
- **Sections**: 9 major sections covering all aspects
- **Length**: 40+ KB comprehensive architecture documentation
