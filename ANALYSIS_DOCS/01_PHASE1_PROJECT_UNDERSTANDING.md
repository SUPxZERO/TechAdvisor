# PHASE 1: PROJECT UNDERSTANDING
**TechAdvisor Expert System - Comprehensive Analysis**

---

## 1. PROJECT IDENTITY

### Project Name
**TechAdvisor Expert System**

### Problem Statement
Users struggle with choosing between hundreds of smartphone and laptop models because of:
- Overwhelming specification details
- Conflicting reviews and opinions  
- Unclear value-for-money
- Not knowing which features matter for their specific use case

**Solution**: TechAdvisor automatically recommends best-fit products using intelligent rule-based inference.

### Project Domain
- 🎯 **E-commerce Decision Support System**
- 🤖 **Expert Systems & Artificial Intelligence**
- 💡 **Rule-Based Inference**
- 📊 **Product Recommendation Engine**

---

## 2. PROJECT GOALS & OBJECTIVES

### Primary Goals
1. **Intelligent Recommendations**: Use rule-based expert system to suggest top 3 products matching user preferences
2. **User Empowerment**: Provide personalized advice without manual human intervention
3. **Admin Control**: Allow non-technical staff to create/modify recommendation rules via UI
4. **Transparency**: Explain *why* each product is recommended (reasoning explanation)

### Key Outcomes
- ✅ Reduce decision time for customers from 2+ hours to 5 minutes
- ✅ Enable administrators to update rules without code changes
- ✅ Provide comprehensive audit trail for all system actions
- ✅ Support product comparison with pros/cons analysis
- ✅ Fine-grained permission control with RBAC

---

## 3. USER PERSONAS & STAKEHOLDERS

### End Users (No Login)
**Persona**: Tech consumers (students, professionals, budget-conscious buyers)
- **Scenario**: "I have $800 budget and need a laptop for gaming. What's best?"
- **Actions**: 
  1. Answer questionnaire (4 simple questions)
  2. Get top 3 product recommendations
  3. Compare products side-by-side
  4. View pro/con analysis
- **Need**: Quick, trustworthy product suggestions in < 5 minutes

### Admin Users (Login Required)
**Persona**: Tech specialists, marketing managers, business analysts

**Admin Role**:
- Full system access
- Manage products, brands, categories
- Create/modify inference rules without coding
- Manage user accounts and permissions
- View audit trails and system statistics
- Need: Easy UI to define recommendation logic

**Staff Role**:
- Limited product management
- Cannot create/modify rules
- Cannot manage users
- Read-only access to some features
- Need: Simplified interface for daily tasks

### System Architect (Academic)
- Need: Complete understanding of logic flow and expert system reasoning

---

## 4. TECHNOLOGY STACK

### Frontend
- **HTML5**: Semantic markup
- **Jinja2**: Server-side templating
- **Tailwind CSS**: Responsive styling  
- **Vanilla JavaScript**: Client-side interactivity

### Backend
- **Python 3.12**: Core language
- **Flask 2.3.3**: Web framework
- **SQLAlchemy ORM**: Database abstraction
- **Flask-Migrate**: Database versioning
- **Flask-Login**: Session management
- **WTForms**: Form handling & validation
- **Flask-WTF**: CSRF protection

### Database
- **MySQL 8.0+**: Relational DBMS
- **PyMySQL**: Python MySQL driver
- **Alembic**: Database migration tool

### Security
- **Werkzeug**: Password hashing (scrypt algorithm)
- **CSRF Tokens**: Form protection
- **RBAC**: Fine-grained permission control
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection

### Testing & Development
- **Pytest**: Unit testing framework
- **pytest-cov**: Coverage reporting
- **python-dotenv**: Environment variable management

---

## 5. DATABASE SCHEMA

### 8 Core Tables

```
┌─────────────────────────────────────────────────────────┐
│                   DATABASE STRUCTURE                    │
├─────────────────────────────────────────────────────────┤
│
│ AUTHENTICATION & AUTHORIZATION
│ ├── users (Admin/Staff accounts)
│ ├── roles (Role definitions)
│ ├── permissions (Permission definitions)
│ └── role_permissions (Many-to-Many)
│
│ PRODUCT CATALOG
│ ├── brands (Manufacturers: Apple, Samsung, etc.)
│ ├── categories (Types: Smartphone, Laptop)
│ ├── products (Individual phones/laptops)
│ └── specifications (Technical details: RAM, CPU, etc.)
│
│ EXPERT SYSTEM
│ ├── rules (Recommendation rules)
│ └── rule_conditions (Rule matching criteria)
│
│ AUDIT & LOGGING
│ └── audit_logs (All system changes tracked)
│
└─────────────────────────────────────────────────────────┘
```

### Table Details

| Table | Purpose | Rows | Relationships |
|-------|---------|------|---|
| **users** | Admin/Staff accounts | Few (< 20) | Has AuditLogs, Has Role |
| **brands** | Product manufacturers (Apple, Samsung, Dell) | 20-50 | Has many Products |
| **categories** | Product types (Smartphone, Laptop) | 2-5 | Has many Products, Has Rules |
| **products** | Individual phones/laptops for sale | 100-500 | Has Brand, Has Category, Has Specifications |
| **specifications** | Technical details (RAM, CPU, Battery, etc.) | 500-2000 | Belongs to Product |
| **rules** | Expert system inference rules | 50-200 | Has many Conditions, Has Category |
| **rule_conditions** | Individual rule matching criteria | 200-1000 | Belongs to Rule |
| **permissions** | Permission definitions (product.create, rule.edit) | 20-50 | Used by Roles |
| **roles** | Role groupings (Admin, Staff, Customer) | 2-10 | Has many Permission, Has many Users |
| **role_permissions** | Role-Permission many-to-many mapping | 50-200 | Links Roles & Permissions |
| **audit_logs** | System activity tracking | Grows continuously | Belongs to User |

---

## 6. EXPERT SYSTEM CORE ARCHITECTURE

### 6.1 System Components

```
┌─────────────────────────────────────┐
│       USER QUESTIONNAIRE            │
│  (4 simple preference questions)    │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│    RECOMMENDATION SERVICE           │
│  (High-level orchestration)         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│    INFERENCE ENGINE                 │
│  (Forward Chaining Logic)           │
│ - Working Memory (facts)            │
│ - Rule Matching                     │
│ - Condition Evaluation              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   DATABASE RULE BASE                │
│   (Rules + Conditions)              │
└──────────────────────────────────────┘
```

### 6.2 Inference Method: Forward Chaining (Data-Driven)

**Definition**: Start with known facts → Apply all applicable rules → Derive new conclusions

**Process**:
1. User provides facts (budget, usage_type, category, brand)
2. System loads ALL active rules from database
3. For EACH rule, evaluate ALL conditions against user facts
4. IF all conditions are satisfied, THEN rule is "fired" (matched)
5. Collect all matched rules
6. Sort matched rules by PRIORITY (highest first)
7. Fetch products based on matched rules
8. Return products with confidence scores and reasoning

### Example Rule Structure

```sql
RULE: "Gaming Laptop for Professionals"
  Conditions:
    - budget >= 1000
    - usage_type = 'gaming'
    - preferred_brand IN ('ASUS', 'MSI', 'Razer')
  Actions:
    - Priority: 90
    - Category: Laptop
    - Return products matching above
```

---

## 7. SYSTEM FEATURES AT HIGH LEVEL

### Feature 1: Smart Questionnaire (User)
**User answers 4 simple questions:**
1. **Product Type**: Smartphone or Laptop?
2. **Budget**: How much willing to spend? ($100-$10,000)
3. **Usage**: What's the primary use?
   - Gaming
   - Business/Work
   - Education/Study
   - General Entertainment
   - Content Creation
4. **Brand Preference**: Preferred manufacturer (optional)

### Feature 2: Intelligent Recommendation (Expert System)
**System returns:**
- Top 3 products matching user inputs
- Confidence score for each (0-100%)
- Detailed reasoning explanation
- All product specifications
- Price comparison

### Feature 3: Product Comparison (User)
**Two types of comparison:**
1. **Side-by-side**: Compare 2-4 products on all specifications
2. **Pros & Cons Analysis**: Get AI-generated pros, cons, and winner for exactly 2 products

### Feature 4: Rule Management (Admin Only)
**Create rules with visual UI:**
- Condition builder (no SQL required)
- Multiple operators: ==, !=, <, >, <=, >=, in, contains
- Priority selection
- Test rules before activation
- Activate/deactivate without code changes

### Feature 5: Admin Dashboard (Admin/Staff)
**Statistics & Management:**
- System statistics (products, brands, rules, users count)
- Product management: Add/edit/delete products with specs
- Brand management: Add/edit brands
- Category management: Create product categories
- User management: Create accounts, assign roles
- Audit trail: View all system changes with timestamps
- Role management: Create roles with fine-grained permissions

---

## 8. DATA FLOW — USER JOURNEY

```
STEP 1: USER VISITS SYSTEM
    ↓
STEP 2: USER COMPLETES QUESTIONNAIRE
    Inputs:
    - Category: "Laptop"
    - Budget: $800
    - Usage Type: "Gaming"
    - Brand: "ASUS"
    ↓
STEP 3: RECOMMENDATION SERVICE RECEIVES INPUTS
    ↓
STEP 4: INFERENCE ENGINE RUNS (FORWARD CHAINING)
    ├─ Load all ACTIVE rules from database
    ├─ For each rule, evaluate conditions:
    │   ├─ IF budget >= 800: TRUE ✓
    │   ├─ IF usage_type = 'gaming': TRUE ✓
    │   ├─ IF brand IN ['ASUS', 'MSI']: TRUE ✓
    │   └─ ALL CONDITIONS MET → Rule matched!
    ├─ Matched rules sorted by priority
    └─ Return matched rules
    ↓
STEP 5: FETCH PRODUCTS FROM CATALOG
    ├─ Filter: category_id = Laptop (from rule)
    ├─ Filter: price <= 800 (budget constraint)
    ├─ Filter: brand_id = ASUS (preference)
    ├─ Sort by price ascending
    └─ Return top 3 products
    ↓
STEP 6: ADD REASONING & CONFIDENCE SCORES
    ├─ Calculate confidence = 50 + (rule_priority)
    ├─ Link products to matched rules
    ├─ Extract key features
    ├─ Generate explanation text
    └─ Add specification details
    ↓
STEP 7: RETURN RESULTS TO USER
    ├─ Product names, prices, images
    ├─ Specifications with key feature highlights
    ├─ Confidence score (e.g., 92%)
    ├─ Matched rule name
    ├─ Full reasoning explanation
    └─ Options to compare or view details
```

---

## 9. CRITICAL SYSTEM COMPONENTS

### Component 1: InferenceEngine
**Location**: `app/services/inference_engine.py`
**Purpose**: Core expert system logic

**Interface**:
```python
engine = InferenceEngine()
engine.add_fact(key, value)        # Add user input
engine.infer(user_inputs) -> List[Rule]  # Run inference
```

**Process**:
1. Create empty working memory (dict)
2. Add user facts to working memory
3. Load all active rules from database
4. For each rule:
   - Check all conditions using evaluate_condition()
   - If ANY condition fails, skip rule
   - If ALL conditions pass, add rule to matched_rules
5. Sort matched_rules by priority (descending)
6. Return matched_rules

### Component 2: RecommendationService
**Location**: `app/services/recommendation_service.py`
**Purpose**: High-level orchestration of recommendations

**Interface**:
```python
service = RecommendationService()
result = service.get_recommendations(user_input, limit=3)
```

**Returns**:
```python
{
    'products': [
        {
            'id': 1,
            'name': 'ASUS TUF Gaming Laptop',
            'price': 749.99,
            'confidence': 92,
            'reasoning': 'Optimized for gaming within your budget',
            'specifications': [...],
            'matched_rule': 'Gaming Laptop Rule'
        },
        ...
    ],
    'total_matches': 3,
    'fired_rules': 5,
    'message': 'Found 3 products matching your preferences'
}
```

### Component 3: ComparisonService
**Location**: `app/services/comparison_service.py`
**Purpose**: Intelligent product comparison with pros/cons analysis

**Features**:
- Category-specific benchmarks (RAM, Storage, Battery, Camera specs)
- Extract pros based on high specs relative to benchmarks
- Extract cons for weak specifications
- Comparative advantages (which product is better in each aspect)
- Overall score calculation
- Winner recommendation with reasoning

### Component 4-6: Models (Product, Rule, User)
**Location**: `app/models/`

**Product Model**:
- Stores product information (name, brand, category, price, image, description)
- Has many specifications
- Can be active/inactive

**Rule Model**:
- Stores inference rules
- Has many conditions (stored in RuleCondition table)
- Priority for sorting
- Can be active/inactive

**User Model**:
- Authentication (password hashing)
- RBAC (role-based access control)
- Permission checking
- Audit logging

---

## 10. SECURITY & RBAC ARCHITECTURE

### 10.1 Authentication
- **Method**: Flask-Login + Session Management
- **Password Storage**: Werkzeug scrypt hashing
- **Session Timeout**: 1 hour (configurable)
- **Remember Me**: Optional persistent sessions

### 10.2 Authorization (RBAC)
```
ROLE-PERMISSION MODEL:
└── Role (has many Permissions)
    ├── Admin
    │   ├── product.create
    │   ├── product.edit
    │   ├── product.delete
    │   ├── rule.create
    │   ├── rule.edit
    │   ├── rule.delete
    │   ├── user.create
    │   ├── user.edit
    │   └── ...all permissions
    │
    └── Staff
        ├── product.view
        ├── product.edit (own)
        ├── rule.view
        └── (limited permissions)
```

### 10.3 Route Protection
```python
@admin_required           # Only admin users
@staff_required          # Admin OR Staff users  
@permission_required('permission.slug')   # Fine-grained permission
@login_required          # Any authenticated user
```

### 10.4 Audit Logging
- **What**: Every action (create, edit, delete) logged
- **Who**: User ID tracked
- **When**: Timestamp recorded
- **Where**: IP address captured
- **Why**: Details stored (old value → new value)

**Tracked Actions**:
- User management
- Product management
- Brand management
- Rule management
- Category management
- User account changes

---

## 11. KEY ALGORITHMS

### Algorithm 1: Forward Chaining Inference
```
FUNCTION infer(user_inputs) -> List[MatchedRules]
  working_memory = {}
  matched_rules = []
  
  FOR EACH key, value IN user_inputs:
    working_memory[key] = value
  
  rules = Database.fetch_active_rules()
  
  FOR EACH rule IN rules:
    all_conditions_met = TRUE
    
    FOR EACH condition IN rule.conditions:
      IF evaluate_condition(condition, working_memory) == FALSE:
        all_conditions_met = FALSE
        BREAK
    
    IF all_conditions_met == TRUE:
      matched_rules.append(rule)
  
  SORT matched_rules BY priority DESCENDING
  RETURN matched_rules
```

### Algorithm 2: Condition Evaluation
```
FUNCTION evaluate_condition(condition, facts) -> Boolean
  key = condition.condition_key
  operator = condition.operator
  expected = condition.condition_value
  actual = facts.get(key)
  
  IF actual is NULL:
    RETURN FALSE
  
  SWITCH operator:
    CASE 'equals' or '==':
      RETURN str(actual).lower() == str(expected).lower()
    CASE 'not_equals' or '!=':
      RETURN str(actual).lower() != str(expected).lower()
    CASE 'less_than' or '<':
      RETURN float(actual) < float(expected)
    CASE 'greater_than' or '>':
      RETURN float(actual) > float(expected)
    CASE 'less_equal' or '<=':
      RETURN float(actual) <= float(expected)
    CASE 'greater_equal' or '>=':
      RETURN float(actual) >= float(expected)
    CASE 'in':
      RETURN str(actual) IN [split by comma and trim]
    CASE 'contains':
      RETURN str(expected) IN str(actual)
    DEFAULT:
      RETURN FALSE
```

### Algorithm 3: Product Filtering & Scoring
```
FUNCTION get_recommendations(user_input, limit) -> Dict
  // Filter products
  products = Database.fetch_all_active_products()
  
  // Budget filter
  IF user_input.budget EXISTS:
    products = FILTER(products, price <= budget)
  
  // Category filter
  IF user_input.category_id EXISTS:
    products = FILTER(products, category_id == category_id)
  
  // Brand preference filter  
  IF user_input.preferred_brand EXISTS:
    products = FILTER(products, brand.name == preferred_brand)
  
  // Scoring
  FOR EACH product IN products:
    confidence = 50 + matched_rule.priority
    reasoning = generate_explanation(product, matched_rule)
    product.confidence = confidence
    product.reasoning = reasoning
  
  // Sort by confidence descending
  products = SORT(products, confidence DESCENDING)
  
  RETURN products[0:limit]
```

---

## 12. KEY OBSERVATIONS

### ✅ Strengths
1. **True Expert System**: Not just filtering; actual rule-based inference
2. **Extensible**: Non-technical users can add rules via UI
3. **Transparent**: Every recommendation has explanation
4. **Secure**: RBAC + audit logging + CSRF protection
5. **Scalable**: Database-driven, ORM-based, supports migrations
6. **Well-Structured**: Clean separation of concerns
7. **Production-Ready**: Error handling, form validation, security headers

### ⚠️ Design Patterns Used
- **Forward Chaining**: Data-driven inference (all facts → conclusions)
- **Active Record**: SQLAlchemy models with relationships
- **Service Layer**: Business logic separate from routes
- **Factory Pattern**: Flask application factory in `create_app()`
- **Decorator Pattern**: Route protections (@login_required, @admin_required)
- **Template Pattern**: Base Jinja2 template with inheritance

### 📊 System Characteristics
- **Inference Type**: Forward Chaining (Data-Driven)
- **Knowledge Representation**: Database Rules + Conditions
- **Reasoning Method**: Explicit condition matching
- **Certainty Handling**: Confidence scores based on rule priority
- **Scalability**: Supports hundreds of products and rules

---

## Summary

**TechAdvisor** is a production-grade expert system that:
1. ✅ Automates product selection decisions using rule-based inference
2. ✅ Provides transparent, explained recommendations
3. ✅ Allows non-technical staff to manage rules and products
4. ✅ Maintains security through RBAC and audit logging
5. ✅ Follows best practices with clean architecture and testing
6. ✅ Demonstrates real-world expert system implementation

**Next Phase**: PHASE 2 — PROJECT STRUCTURE ANALYSIS
