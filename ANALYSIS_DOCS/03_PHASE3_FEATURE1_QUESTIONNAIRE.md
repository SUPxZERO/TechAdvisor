# PHASE 3: FEATURE-BY-FEATURE ANALYSIS

## FEATURE 1: SMART QUESTIONNAIRE ❓

**Status**: Actively used for user recommendations  
**Location**: `/recommend` endpoint (route + forms + templates)  
**Technology Stack**: Flask, WTForms, Jinja2, Tailwind CSS, JavaScript  
**User Audience**: General public (no login required)  

---

## 1️⃣ FEATURE OVERVIEW

### Purpose
Collect user preferences through an **interactive 4-step questionnaire** that gathers the essential information needed to feed the expert system's inference engine.

### Business Objective
- ✅ Minimize user friction (simple 4 questions, not 20)
- ✅ Gather sufficient data for intelligent recommendations
- ✅ Provide visual feedback during form completion
- ✅ Enable users to get recommendations in < 5 minutes

### Key Characteristics
- **No Login Required**: Fully public, accessible to anyone
- **Progressive Disclosure**: Show questions one at a time
- **Visual Feedback**: Progress bar, animations, icons
- **Interactive Controls**: Sliders, radio buttons, toggles
- **Input Validation**: Both client-side (HTML5) and server-side (WTForms)
- **Session-Based**: Store preferences for later comparison operations

---

## 2️⃣ USER INTERACTION FLOW (Step-by-Step)

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: USER ARRIVES AT /recommend                          │
│ GET request → Flask shows questionnaire.html                │
│ (Empty form, all questions disabled except first)           │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: USER ANSWERS QUESTION 1 - Category Selection        │
│ "What are you looking for?"                                 │
│ - Smartphone  (radio button with icon)                      │
│ - Laptop      (radio button with icon)                      │
│ JavaScript enables Question 2 when Q1 is selected           │
│ Progress bar updates: 1/4 → 25% widthQ                      │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: USER ANSWERS QUESTION 2 - Budget Entry              │
│ "What is your maximum budget?"                              │
│ Interactive controls:                                       │
│ - Slider range: $100 - $5,000                               │
│ - Quick preset buttons: Entry/Mid/Pro                       │
│ - Real-time display: "$1,000" updates as slider moves       │
│ JavaScript enables Question 3 when Q2 is entered            │
│ Progress bar updates: 2/4 → 50% width                       │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: USER ANSWERS QUESTION 3 - Usage Type Selection      │
│ "Primary usage?"                                            │
│ 5 options with icons (2×4 grid):                            │
│ - Gaming, Business, Education, General, Content Creation    │
│ Radio buttons with visual feedback                          │
│ JavaScript enables Question 4 when Q3 is selected           │
│ Progress bar updates: 3/4 → 75% width                       │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: USER ANSWERS QUESTION 4 - Brand (OPTIONAL)          │
│ "Preferred Brand (optional)"                                │
│ - Text input field (Optional, max 50 characters)            │
│ - Placeholder: "e.g., Apple, Samsung, Dell"                 │
│ JavaScript enables submit button                            │
│ Progress bar updates: 4/4 → 100% width                      │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 6: USER SUBMITS FORM                                   │
│ POST /recommend with form data:                             │
│ - category: "smartphone" or "laptop"                        │
│ - budget: 1000 (integer)                                    │
│ - usage_type: "gaming", "business", etc.                    │
│ - preferred_brand: "Apple" (optional)                       │
│ - csrf_token: (automatically added by Flask-WTF)            │
│                                                             │
│ Server-side validation on form data                         │
│ If validation fails: Re-show form with errors               │
│ If validation passes: Continue to STEP 7                    │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 7: INFERENCE ENGINE PROCESSES REQUEST                  │
│ (Internal - covered in separate feature analysis)           │
│ Calls RecommendationService.get_recommendations()           │
│ Returns JSON with matching products                         │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 8: RESULTS DISPLAYED                                   │
│ render_template('user/results.html')                        │
│ Displays:                                                   │
│ - Top 3 recommended products (cards)                        │
│ - Confidence scores (% match)                               │
│ - Reasoning explanations                                    │
│ - Product specifications                                   │
│ - Price range                                              │
│ - Options: View details, Compare, etc.                      │
│ - User preferences stored in session                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 3️⃣ FORM STRUCTURE & VALIDATION

### 3.1 Form Definition (WTForms)

**File**: `app/forms/recommendation_forms.py`

```python
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length

class RecommendationForm(FlaskForm):
    """Form for collecting user preferences"""
    
    # FIELD 1: Category Selection
    category = SelectField(
        label='What are you looking for?',
        choices=[
            ('smartphone', 'Smartphone'),
            ('laptop', 'Laptop')
        ],
        validators=[DataRequired()]  # Required field
    )
    # Type: Radio select (dropdown in HTML)
    # Validation: Must pick one option
    # SQL Error Handling: Validates against allowed choices
    
    # FIELD 2: Budget Input
    budget = IntegerField(
        label='What is your budget? (USD)',
        validators=[
            DataRequired(),                    # Cannot be empty
            NumberRange(min=100, max=10000)   # Range validation
        ],
        render_kw={'placeholder': 'e.g., 1000'}
    )
    # Type: Integer input with slider
    # Validation: 100 ≤ budget ≤ 10,000
    # Type Safety: Automatically converts string to int
    # Error Messages: "Enter a number between 100 and 10000"
    
    # FIELD 3: Usage Type Selection
    usage_type = SelectField(
        label='Primary Usage',
        choices=[
            ('gaming', 'Gaming'),
            ('work', 'Business'),
            ('study', 'Education'),
            ('general', 'General'),
            ('creative', 'Content Creation')
        ],
        validators=[DataRequired()]  # Required field
    )
    # Type: Radio select
    # Validation: Must pick one option
    # Note: Forms stored in database rules, so values must match
    
    # FIELD 4: Brand Preference (OPTIONAL)
    preferred_brand = StringField(
        label='Preferred Brand (Optional)',
        validators=[
            Optional(),               # This field is not required
            Length(max=50)            # But if provided, max 50 chars
        ],
        render_kw={'placeholder': 'e.g., Apple, Samsung, Dell'}
    )
    # Type: Text input
    # Validation: 0-50 characters
    # Nullability: Can be empty or None
    # Purpose: Filter products by brand name
    
    # FIELD 5: Additional Notes (Nice-to-have)
    additional_notes = TextAreaField(
        label='Any specific requirements?',
        validators=[
            Optional(),               # Not required
            Length(max=500)          # Max 500 chars
        ],
        render_kw={
            'placeholder': 'e.g., Need long battery life, prefer lightweight...',
            'rows': 3
        }
    )
    # Type: Large text area
    # Note: Currently NOT used in inference (future feature)
    # Could be used for admin review
    
    # FIELD 6: Submit Button
    submit = SubmitField('Get Recommendations')
```

### 3.2 Validation Layers

```
CLIENT SIDE (HTML5 + JavaScript)
  ├─ Form input type attributes (enforce format)
  ├─ Required attribute (enforce presence)
  ├─ Pattern attributes (enforce format)
  ├─ Range attributes (min/max for slider)
  └─ JavaScript event listeners (progressive disclosure)
         ↓ (Fast feedback, no server round-trip)

SERVER SIDE (WTForms + Flask)
  ├─ CSRF token validation (security)
  ├─ DataRequired validator (field presence)
  ├─ NumberRange validator (numeric boundaries)
  ├─ Length validator (string length)
  ├─ Type coercion (int/string conversion)
  └─ Choice validation (allowed values only)
         ↓ (Security-critical, authoritative)

IF VALIDATION FAILS:
  Form.validate_on_submit() returns False
  Re-render questionnaire.html with error messages
  Error messages displayed below each field

IF VALIDATION PASSES:
  Form data extracted as Python objects
  Data passed to recommendation service
  Inference engine begins processing
```

---

## 4️⃣ COMPONENT BREAKDOWN

### 4.1 Backend Route Handler

**File**: `app/routes/user.py` → `@user_bp.route('/recommend', methods=['GET', 'POST'])`

```python
@user_bp.route('/recommend', methods=['GET', 'POST'])
def recommend():
    """Recommendation questionnaire and results endpoint"""
    
    # ===== CREATE FORM INSTANCE =====
    form = RecommendationForm()
    
    # ===== HANDLE POST REQUEST (Form Submission) =====
    if form.validate_on_submit():
        
        # STEP 1: EXTRACT FORM DATA
        category_value = form.category.data      # 'smartphone' or 'laptop'
        budget = form.budget.data                # Integer: 100-10000
        usage_type = form.usage_type.data        # 'gaming', 'work', etc.
        preferred_brand = form.preferred_brand.data  # String or None
        
        # STEP 2: RESOLVE CATEGORY TO DATABASE ID
        # Why? Database stores category as an ID, not a string
        # Form returns string ('smartphone'), but we need the database ID
        category = Category.query.filter(
            db.func.lower(Category.name) == category_value.lower()
        ).first()
        # This query:
        # - Case-insensitive comparison (lower())
        # - Looks up category by name parameter
        # - Returns first matching record (should be only 1)
        # - Returns None if no match
        
        # STEP 3: BUILD USER INPUTS DICTIONARY
        # This dict is passed to the inference engine
        user_inputs = {
            'category': category_value.lower(),      # 'smartphone'
            'category_id': category.id if category else None,  # 1 or 2
            'budget': budget,                        # 1000
            'usage_type': usage_type,                # 'gaming'
            'preferred_brand': preferred_brand if preferred_brand else None  # 'Apple' or None
        }
        # These become "facts" in the expert system's working memory
        
        # STEP 4: CALL RECOMMENDATION SERVICE
        rec_service = RecommendationService()
        recommendations = rec_service.get_recommendations(
            user_inputs, 
            limit=9  # Return up to 9 products
        )
        # This service:
        # - Runs inference engine
        # - Fetches matching products
        # - Adds reasoning explanations
        # - Returns structured data with metadata
        
        # STEP 5: STORE PREFERENCES IN SESSION
        session['last_preferences'] = user_inputs
        # Why? For later use in comparison feature
        # Users might want to compare products using their original preferences
        
        # STEP 6: RENDER RESULTS TEMPLATE
        return render_template('user/results.html',
                             products=recommendations.get('products', []),
                             message=recommendations.get('message', ''),
                             total_matches=recommendations.get('total_matches', 0),
                             fired_rules=recommendations.get('fired_rules', 0))
        # Passes:
        # - products: List of recommended product dicts with reasoning
        # - message: Human-readable summary ("Found 3 products...")
        # - total_matches: Count of products returned
        # - fired_rules: Count of rules that matched
    
    # ===== HANDLE GET REQUEST (Initial Form Display) =====
    # If not POST or validation failed, show empty form
    return render_template('user/questionnaire.html', form=form)
```

### 4.2 Form Instantiation & CSRF

```python
form = RecommendationForm()  # Constructor creates form instance

# CSRF Token Handling:
# - RecommendationForm extends FlaskForm (not plain WTForms.Form)
# - FlaskForm automatically generates and validates CSRF tokens
# - In HTML template: {{ form.hidden_tag() }}
#   This renders: <input type="hidden" name="csrf_token" value="...">
# - On submission, Flask-WTF validates token matches session
# - If token invalid or missing: raises 400 Bad Request

# How CSRF Protection Works:
# 1. GET /recommend
#    - Flask creates random token
#    - Embeds in HTML form as hidden field
#    - Token also stored in user's session
#
# 2. User submits form (POST)
#    - Browser sends hidden token with form data
#    - Server compares:
#      - Token in form data
#      - Token in session (secretly stored on server)
#    - If mismatch → Attack detected → 400 response
#    - If match → Request genuine → Process form
```

---

## 5️⃣ FRONTEND PRESENTATION

### 5.1 Questionnaire HTML Template

**File**: `app/templates/user/questionnaire.html`

**Structure**:
```html
{% extends 'base.html' %}           ← Inherit from master template

{% block content %}
    <!-- Progress Indicator -->
    <div class="progress-bar">
        Step <span id="currentStepDisplay">1</span> of 4
        <div id="progressBar" width="25%"></div>
    </div>
    
    <!-- Header -->
    <h1>Let's find your match</h1>
    <p>Tell us a bit about what you need</p>
    
    <!-- Form -->
    <form method="POST" action="/recommend" id="recommendForm">
        {{ form.hidden_tag() }}         ← CSRF token
        
        <!-- Question 1: Category -->
        <div class="question-section" data-question="1">
            <h2>What type of device are you looking for?</h2>
            <div class="grid">
                {% for value, label in form.category.choices %}
                <label>
                    <input type="radio" name="category" value="{{ value }}">
                    <icon>{{ icon_for(value) }}</icon>
                    <span>{{ label }}</span>
                </label>
                {% endfor %}
            </div>
        </div>
        
        <!-- Question 2: Budget (Similar structure) -->
        <!-- Question 3: Usage (Similar structure) -->
        <!-- Question 4: Brand (Similar structure) -->
        
        <button type="submit">Get Recommendations</button>
    </form>
{% endblock %}
```

### 5.2 Visual Design Features

```
PROGRESSIVE DISCLOSURE PATTERN:
┌─ Question 1 (100% opacity, fully interactive)
├─ Question 2 (opacity: 30%, pointer-events: none → disabled)
├─ Question 3 (opacity: 30%, pointer-events: none → disabled)
├─ Question 4 (opacity: 30%, pointer-events: none → disabled)
└─ Submit Button (disabled until all required fields done)

ANIMATION FLOW:
- As user answers → Next question animates in
- Opacity: 30% → 100% (transition: 500ms)
- Blur effect: blur-sm → blur-none
- Progress bar width increases

CSS FRAMEWORK: Tailwind CSS
- Responsive grid: grid-cols-1 md:grid-cols-2 lg:grid-cols-3
- Color scheme: Brand colors (brand-900, brand-50, brand-100, etc.)
- Spacing: Consistent rem-based spacing
- Shadows: Subtle box-shadows for depth
- Transitions: 300-500ms easing for smooth animations

ICON SYSTEM:
- SVG icons inline (no image files)
- Smartphone icon: Mobile device symbol
- Laptop icon: Computer device symbol
- Gaming icon: Joystick symbol
- Business icon: Briefcase symbol
- Education icon: Graduation cap symbol
- Creative icon: Palette symbol

INPUT CONTROLS:
Q1: Radio buttons with custom styling
Q2: Range slider + preset quick-buttons
Q3: Radio button grid
Q4: Text input field
```

### 5.3 JavaScript Interactivity

```javascript
// FILE: static/js/questionnaire.js (inferred from functionality)

// PROGRESSIVE DISCLOSURE
function enableQuestion(questionNum) {
    const section = document.querySelector(`[data-question="${questionNum}"]`);
    section.classList.remove('opacity-30', 'pointer-events-none', 'blur-sm');
    section.classList.add('opacity-100', 'pointer-events-auto', 'blur-none');
    updateProgressBar(questionNum);
}

// BUDGET SLIDER INTERACTION
document.getElementById('budgetSlider').addEventListener('input', (e) => {
    const value = e.target.value;
    document.getElementById('budgetValue').textContent = value;
    // Format with commas: 1000 → 1,000
});

// BUDGET PRESET BUTTONS
document.querySelectorAll('.budget-preset').forEach(button => {
    button.addEventListener('click', (e) => {
        const value = e.target.dataset.value;
        document.getElementById('budgetSlider').value = value;
        document.getElementById('budgetValue').textContent = value;
        enableQuestion(3);
    });
});

// PROGRESS BAR UPDATE
function updateProgressBar(questionNum) {
    const percentage = (questionNum / 4) * 100;
    document.getElementById('progressBar').style.width = percentage + '%';
    document.getElementById('currentStepDisplay').textContent = questionNum;
}

// FORM SUBMISSION
document.getElementById('recommendForm').addEventListener('submit', (e) => {
    // Validate all fields before sending
    // Show loading spinner
    // Disable submit button
});
```

---

## 6️⃣ DATA FLOW PROCESSING

### Complete Data Transformation Pipeline

```
USER INPUT (Frontend)
│
├─ category: "smartphone" (raw form value)
├─ budget: 1000 (slider/input value)
├─ usage_type: "gaming" (radio selection)
├─ preferred_brand: "Apple" (optional text)
└─ csrf_token: "abc123xyz..." (hidden field)
  
  │ (HTTP POST to /recommend)
  ▼
  
FORM VALIDATION (WTForms)
│
├─ CSRF Token Check: valid? YES ✓
├─ DataRequired: category present? YES ✓
├─ DataRequired: budget present? YES ✓
├─ NumberRange: 100 ≤ 1000 ≤ 10000? YES ✓
├─ DataRequired: usage_type present? YES ✓
├─ Length: preferred_brand ≤ 50 chars? YES ✓
└─ Type Coercion: budget "1000" → int 1000 ✓
  
  (All validators pass)
  │
  ▼
  
PYTHON PROCESSING (Route Handler)
│
├─ form.validate_on_submit() = True
├─ Extract: category.data = "smartphone"
├─ Extract: budget.data = 1000
├─ Extract: usage_type.data = "gaming"
├─ Extract: preferred_brand.data = "Apple"
│
├─ Lookup: Category.query where name ≈ "smartphone"
│         Returns: Category(id=1, name="Smartphone")
│
├─ Build user_inputs dict:
│  {
│    'category': 'smartphone',
│    'category_id': 1,
│    'budget': 1000,
│    'usage_type': 'gaming',
│    'preferred_brand': 'Apple'
│  }
│
├─ Create service: rec_service = RecommendationService()
│
└─ Call service: recommendations = rec_service.get_recommendations(user_inputs)
  
  │ (Passed to inference_engine.py - FEATURE 2)
  ▼
  
EXPERT SYSTEM PROCESSING (Covered in separate analysis)
│
└─ Returns recommendations dict with products + metadata
  
  │
  ▼
  
SESSION STORAGE
│
└─ session['last_preferences'] = user_inputs (for comparison feature)
  
  │
  ▼
  
TEMPLATE RENDERING
│
├─ render_template('user/results.html')
├─ Pass products list
├─ Pass metadata (total_matches, fired_rules)
└─ Return HTML to browser
  
  │
  ▼
  
BROWSER DISPLAY
└─ User sees recommendation results page
   - Product cards with images
   - Confidence scores
   - Reasoning explanations
   - Options to compare or view details
```

---

## 7️⃣ SESSION MANAGEMENT

### Why Store Preferences?

```python
# After form submission, store in session:
session['last_preferences'] = {
    'category': 'smartphone',
    'category_id': 1,
    'budget': 1000,
    'usage_type': 'gaming',
    'preferred_brand': 'Apple'
}

# Later, when user compares 2 products:
@user_bp.route('/compare-analysis')
def compare_analysis():
    user_preferences = session.get('last_preferences', {})
    # Retrieve the preferences from earlier
    # Pass to comparison service for context-aware analysis
```

### Session Configuration

```python
# From config.py
SESSION_TYPE = 'filesystem'                    # Store on disk
PERMANENT_SESSION_LIFETIME = 3600              # 1 hour timeout
SESSION_COOKIE_SECURE = False                 # True in production
SESSION_COOKIE_HTTPONLY = True                # No JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'               # CSRF protection
```

### Security Implications

```
✓ HTTPOnly: JavaScript cannot access session data
  - Prevents XSS attacks from stealing session
  
✓ SameSite: Cookies only sent to same origin
  - Prevents CSRF attacks
  
✓ Timeout: Sessions expire after 1 hour
  - Limits exposure of compromised sessions
  
ℹ️ Filesystem storage: Good for development
  - In production: Use Redis or Memcached for scale
```

---

## 8️⃣ ERROR HANDLING & EDGE CASES

### 8.1 Invalid Form Submission

```python
# Scenario 1: Missing required field
if form.validate_on_submit():
    # form.validate() calls all validators
    # If DataRequired validator fails:
    # - DataRequired(message="This field is required.") runs
    # - Adds error to form.errors['field_name']
    # - validate_on_submit() returns False
else:
    # Re-render form with error messages
    return render_template('user/questionnaire.html', form=form)
    # Template iterates errors:
    # {% if form.errors %}
    #   {% for field, errors in form.errors.items() %}
    #     <div class="error">{{ errors[0] }}</div>
    #   {% endfor %}
    # {% endif %}
```

### 8.2 Budget Out of Range

```python
# Scenario: User submits budget=50000 (exceeds max=10000)
validators=[NumberRange(min=100, max=10000)]

# WTForms raises validation error:
# "Number must be between 100 and 10000"

# Form not submitted, user sees error, form cleared
# User must correct and resubmit
```

### 8.3 Category Not in Database

```python
category = Category.query.filter(
    db.func.lower(Category.name) == category_value.lower()
).first()

if not category:
    # Category lookup failed (shouldn't happen with current choices)
    # category_id becomes None
    # Inference service handles gracefully (returns no products)
    
# In data dict:
user_inputs = {
    'category_id': None,  # Defensive programming
    # ...
}
```

### 8.4 CSRF Token Missing/Invalid

```python
# If user's CSRF token doesn't match:
# Flask-WTF raises 400 Bad Request
# error_handler catches this
# User sees "Form expired, try again" message

# When can this happen?
# - JavaScript modified hidden input
# - Session cookie deleted
# - Attacker sent form from different site
# - Page cached longer than session timeout
```

### 8.5 Injection Attacks

```python
# Input: preferred_brand: "Apple'; DROP TABLE products; --"
# WTForms sanitizes this (escapes special characters)
# SQLAlchemy parameterized query prevents SQL injection:

brand = Brand.query.filter(
    db.func.lower(Brand.name) == user_input['preferred_brand'].lower()
).first()
# Internally: SELECT * FROM brands WHERE LOWER(name) = %s
#             params: ["apple'; drop table products; --"]
# Result: Searches for exact brand name (literal string)
# DROP TABLE never executes (it's treated as part of search string)

# XSS Prevention:
# Jinja2 auto-escapes HTML in templates
# {{ preferred_brand }} → "Apple" (if it contained HTML, filtered)
# {{ "<script>alert('xss')</script>" }} → &lt;script&gt;...
```

---

## 9️⃣ REAL-WORLD WORKFLOW EXAMPLE

### Complete User Journey with Real Data

```
=== SCENARIO: College Student Looking for Gaming Laptop ===

STEP 1: User navigates to http://localhost:5001/recommend
GET request reaches @user_bp.route('/')
≈ form = RecommendationForm()
≈ render_template('user/questionnaire.html', form=form)
Response: HTML questionnaire page loads

STEP 2: User selects "Laptop"
JavaScript: enableQuestion(2)
Visual: Q2 opacity changes 30% → 100%, blur removed
Progress: 25% width

STEP 3: User drags budget slider to $1,500
JavaScript: budgetSlider.onchange()
Real-time: $1,500 displayed
JavaScript: enableQuestion(3)
Progress: 50% width

STEP 4: User clicks "Gaming" usage option
JavaScript: enableQuestion(4)
Visual: Q4 becomes visible
Progress: 75% width

STEP 5: User types "ASUS" in brand field
Input validates as < 50 characters
JavaScript: Form submit button enabled
Progress: 100% width

STEP 6: User clicks "Get Recommendations"
JavaScript: preventDefault() → form.submit()
POST request: /recommend

SERVER RECEIVES:
form.category.data = "laptop"
form.budget.data = 1500
form.usage_type.data = "gaming"
form.preferred_brand.data = "ASUS"
form.csrf_token = "eyJ0eXAi..." (auto-generated)

FORM VALIDATION:
✓ CSRF token valid
✓ category present and in choices
✓ budget is integer between 100-10000
✓ usage_type present and in choices
✓ preferred_brand ≤ 50 chars
form.validate_on_submit() = True

DATA PROCESSING:
category = Category.query.filter(
    db.func.lower(Category.name) == "laptop"
).first()
→ Returns Category(id=2, name="Laptop")

user_inputs = {
    'category': 'laptop',
    'category_id': 2,
    'budget': 1500,
    'usage_type': 'gaming',
    'preferred_brand': 'ASUS'
}

SESSION STORAGE:
session['last_preferences'] = user_inputs

SERVICE CALL:
rec_service = RecommendationService()
recommendations = rec_service.get_recommendations(user_inputs, limit=9)

[Inference engine processes - see FEATURE 2 analysis]

RETURNS:
{
    'products': [
        {
            'id': 5,
            'name': 'ASUS TUF Gaming A16',
            'brand': 'ASUS',
            'price': 1399.99,
            'confidence': 92,
            'reasoning': 'Perfect gaming laptop under your budget',
            'matched_rule': 'Gaming Laptop Rule',
            'specifications': {...}
        },
        # ... 2 more products
    ],
    'total_matches': 3,
    'fired_rules': 5,
    'message': 'Found 3 products matching your preferences'
}

TEMPLATE RENDERING:
render_template('user/results.html',
    products=[3 product dicts],
    message='Found 3 products...',
    total_matches=3,
    fired_rules=5
)

RESPONSE: HTML results page with:
- 3 laptop recommendation cards
- 92% confidence score
- "Perfect gaming laptop under your budget"
- Specifications and price
- Compare buttons, View details links

USER SEES:
✓ ASUS TUF Gaming A16 - $1,399.99
  |- 92% Match
  |- "Perfect gaming laptop under your budget"
  |- RTX 4060, 16GB RAM, 512GB SSD
  |- [Compare] [View Details] buttons
✓ 2 more recommended laptops
```

---

## 🔟 KEY VALIDATION OPERATORS

```python
# From WTForms validators:

DataRequired()
  └─ Field cannot be empty/None
  └─ Error: "This field is required."

Optional()
  └─ Field can be empty/None
  └─ If provided, other validators apply

NumberRange(min=100, max=10000)
  └─ Value must be between min and max (inclusive)
  └─ Works with numeric types (int, float, Decimal)
  └─ Error: "Number must be between 100 and 10000"

Length(min=0, max=50)
  └─ String length must be within range
  └─ Error: "Field must be at most 50 characters"

Regexp(pattern)
  └─ String must match regex pattern
  └─ Example: Regexp('^[a-zA-Z0-9]+$')

Email()
  └─ Must be valid email format
  └─ Uses email_validator package

URL()
  └─ Must be valid URL
  └─ Validates protocol and format
```

---

## 1️⃣1️⃣ CUSTOM VALIDATION EXAMPLE

```python
# If we wanted to add business logic validation:

class RecommendationForm(FlaskForm):
    # ... existing fields ...
    
    def validate_budget(form, field):
        """Custom validator to ensure budget is sensible"""
        if field.data and field.data < 200:
            raise ValidationError('Budget too low for quality devices')
    
    def validate_on_submit(self):
        """Override to add extra checks"""
        if not super().validate_on_submit():
            return False
        
        # Custom business logic
        if self.usage_type.data == 'gaming' and self.budget.data < 500:
            # Gaming laptops usually > $500
            # Could warn user but still allow
            flash('Gaming laptops under $500 are limited')
        
        return True
```

---

## SUMMARY: FEATURE 1 - SMART QUESTIONNAIRE

| Aspect | Details |
|--------|---------|
| **Purpose** | Collect user preferences for recommendation system |
| **Entry Point** | GET /recommend (show form) + POST /recommend (process) |
| **Form Fields** | 4 required + 1 optional fields |
| **Validation** | 2-layer (client HTML5 + server WTForms) |
| **Security** | CSRF tokens, SQL injection prevention, XSS protection |
| **UX** | Progressive disclosure, visual feedback, animations |
| **Session** | Preferences stored for use in comparison feature |
| **Error Handling** | Form re-rendered with error messages |
| **Time Complexity** | O(1) - just form processing |
| **Database Calls** | 1 query (Category lookup) |
| **External Dependencies** | None (pure Flask) |

---

## KEY ARCHITECTURAL PATTERNS

### Pattern 1: Form-Based Data Collection
```
GET /recommend
  └─ Show form (QuestionnaireForm)
POST /recommend with form data
  ├─ Validate server-side
  ├─ Transform to Python objects
  └─ Pass to business logic
```

### Pattern 2: Progressive Disclosure
```javascript
// Based on form input state
// Enable/disable next question
// Create sense of progress
// Reduce cognitive load
```

### Pattern 3: Session-Based State
```python
session['last_preferences'] = {...}
# Later retrieved in comparison feature
# Eliminates need to repeat questionnaire
```

---

**Next Feature**: FEATURE 2 — INTELLIGENT RECOMMENDATION ENGINE (coming next)

This feature dives into:
- Inference engine execution
- Rule matching algorithm
- Confidence calculation
- Reasoning explanation generation
