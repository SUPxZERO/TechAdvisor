# PHASE 7 - SYSTEM WORKFLOWS
**Complete End-to-End User & Admin Journeys Through TechAdvisor**

---

## 1. WORKFLOW FUNDAMENTALS

### 1.1 Workflow Definition

```
WORKFLOW = Sequence of user actions + system responses
           that achieves a specific goal

Components:
├─ ACTOR: Who (user, admin, system)
├─ GOAL: What they want to accomplish
├─ PRECONDITIONS: Starting state
├─ STEPS: Action sequence (user + system)
├─ DECISIONS: Branch points (IF-THEN)
├─ OUTCOMES: Success/failure states
└─ TIME: Duration from start to finish

TechAdvisor Workflows:
├─ User Workflows: Find recommendations, compare products
├─ Admin Workflows: Create/modify rules, monitor system
├─ Integration: How workflows interact
└─ Error Paths: What happens when things fail
```

### 1.2 Workflow Diagram Notation

```
┌─────────────────────────────────────────────────────┐
│ WORKFLOW: User Gets Gaming Laptop Recommendation    │
├─────────────────────────────────────────────────────┤
│                                                     │
│ [START] ──→ User visits site                       │
│              ↓                                      │
│         System: Load homepage                      │
│              ↓                                      │
│         Decision: User logged in?                  │
│         ├─ YES ──→ [Go to recommendations]         │
│         └─ NO  ──→ [Show login prompt]             │
│                   ↓                                │
│              User: Click "Continue as guest"      │
│              ↓                                      │
│         System: Load questionnaire                 │
│              ↓                                      │
│         User: Fill budget ($1500), usage (gaming)  │
│              ↓                                      │
│         System: Run inference, show products       │
│              ↓                                      │
│         User: Select 2 products to compare        │
│              ↓                                      │
│         System: Display comparison                 │
│              ↓                                      │
│         [SUCCESS - User made informed decision]    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 2. USER WORKFLOW 1: FIRST-TIME GAMER

### 2.1 Workflow Overview

```
GOAL: First-time laptop buyer needs gaming laptop recommendation
ACTOR: Sarah (gamer, $1500 budget, brand: ASUS preferred)
DURATION: 8 minutes
SUCCESS: Selects ASUS TUF Gaming laptop
```

### 2.2 Step-by-Step Walkthrough

```
TIME: 14:00 - WORKFLOW START
═════════════════════════════════════════════════════════════════

STEP 1: Sarah Discovers TechAdvisor
─────────────────────────────────────
TIME: 14:00
ACTION (Sarah): Google "gaming laptop recommendation"
ACTION (Google): Returns TechAdvisor as 3rd result
ACTION (Sarah): Clicks link
SYSTEM: HTTP GET /
SYSTEM: Load homepage
SYSTEM: Render: Logo, welcome message, "Start Recommendation" button
SYSTEM: Banner: "Find your perfect device in 3 minutes"
TIME ELAPSED: 2 seconds


STEP 2: Sarah Clicks "Start Recommendation"
─────────────────────────────────────────────
TIME: 14:02
ACTION (Sarah): Click button
SYSTEM: HTTP GET /recommend
SYSTEM: Check: Is user logged in?
  └─ NO → Continue as guest (allowed)
SYSTEM: Database Query: Load categories
  └─ Result: [Smartphone, Laptop, Gaming Laptop]
SYSTEM: Render questionnaire.html
  ├─ Budget slider (0-10000, default 1500)
  ├─ Usage dropdown (gaming, business, general, creative)
  ├─ Brand dropdown (Apple, Dell, HP, ASUS, MSI, Intel, AMD, Samsung)
  ├─ Radio buttons for category preference
  └─ Submit button
TIME ELAPSED: 3 seconds


STEP 3: Sarah Sees Questionnaire
─────────────────────────────────
TIME: 14:05
SYSTEM: Display HTML questionnaire
BROWSER: Render form with validation JavaScript
JAVASCRIPT: Add interactivity:
  ├─ Budget slider: Show value as user drags ($1500 highlighted)
  ├─ Usage dropdown: Show icon for each option
  ├─ Brand dropdown: Show logos
  └─ Category: Show descriptions ("High-performance for gaming")
SARAH: Reviews form, sees gaming laptop category
SARAH: Thinks "Perfect, that's what I need"
TIME ELAPSED: 30 seconds (reading form)


STEP 4: Sarah Fills Out Form
──────────────────────────────
TIME: 14:05:30
ACTION (Sarah): Adjusts budget slider
  ├─ Moves to $1500 (already there, so no change)
  └─ JavaScript updates in real-time (no page reload)
ACTION (Sarah): Clicks "Usage Type" dropdown
  ├─ Options appear: gaming, business, general, creative
  ├─ John sees icons next to each option
  └─ Hovers over "gaming" → tooltip "High-performance devices"
ACTION (Sarah): Selects "gaming"
  └─ JavaScript updates form state
ACTION (Sarah): Clicks "Preferred Brand" dropdown
  ├─ Options appear with logos
  ├─ Sarah scrolls to ASUS
  └─ Selects ASUS
ACTION (Sarah): Clicks "Category" radio buttons
  ├─ Sees three options: Smartphone, Laptop, Gaming Laptop
  ├─ Gaming Laptop already selected (form default)
  └─ Confirms selection
TIME ELAPSED: 2 minutes (reading, clicking, selecting)


STEP 5: Sarah Reviews Before Submitting
────────────────────────────────────────
TIME: 14:07:30
SARAH: Reviews filled form:
  ├─ Budget: $1500 ✓
  ├─ Usage Type: Gaming ✓
  ├─ Preferred Brand: ASUS ✓
  └─ Category: Gaming Laptop ✓
SARAH: Thinks "This looks right. Let me submit."
ACTION (Sarah): Clicks "Get Recommendations" button
TIME ELAPSED: 30 seconds


STEP 6: Browser Makes POST Request
────────────────────────────────────
TIME: 14:08
ACTION (Browser): POST /recommend
  ├─ Content: budget=1500, usage_type=gaming, preferred_brand=ASUS, category=laptop
  ├─ CSRF Token: abc123... (from form)
  └─ Network: 50 ms to server

SYSTEM: Receive POST request
SYSTEM: Validate CSRF token
  └─ ✓ Valid (matches session)
SYSTEM: Extract form data
  ├─ budget = 1500 (type: int)
  ├─ usage_type = "gaming" (type: str)
  ├─ preferred_brand = "ASUS" (type: str)
  └─ category = 3 (Gaming Laptop)
TIME ELAPSED: 75 ms


STEP 7: SYSTEM Validates Input
───────────────────────────────
TIME: 14:08:075
SYSTEM: WTForms Validation
  ├─ budget: 
  │  ├─ Type check: int? YES ✓
  │  ├─ Range (0-10000)? 1500 ✓
  │  └─ Not empty? YES ✓
  ├─ usage_type:
  │  ├─ In enum (gaming, business, general, creative)? gaming ✓
  │  └─ Not empty? YES ✓
  ├─ preferred_brand:
  │  ├─ Type: string? YES ✓
  │  ├─ Max length 100? ASUS (4 chars) ✓
  │  └─ In database? ASUS exists ✓
  └─ category:
     ├─ Type: int? YES ✓
     └─ In database? category_id=3 exists ✓

ALL VALIDATIONS PASS ✓
TIME ELAPSED: 5 ms


STEP 8: SYSTEM Creates Working Memory
──────────────────────────────────────
TIME: 14:08:080
SYSTEM: Python code:
  working_memory = {
    'budget': 1500,
    'usage_type': 'gaming',
    'preferred_brand': 'ASUS',
    'category': 3
  }

SYSTEM: Store in session:
  session['working_memory'] = working_memory
  session['questionnaire_time'] = '2026-03-05 14:08:00'

WORKING MEMORY created successfully ✓
TIME ELAPSED: 2 ms


STEP 9: SYSTEM Runs Inference Engine
──────────────────────────────────────
TIME: 14:08:082
SYSTEM: Call: inference_engine.infer(working_memory)

[INFERENCE BEGINS - 7 ms process]

Load Rules from Database:
  Query: SELECT * FROM rules 
         WHERE is_active = TRUE 
         ORDER BY priority DESC
  Result: 14 rules loaded
  Network:  7 ms

Load Conditions:
  Eager-load all conditions for matched rules
  Result: ~42 conditions
  Network:  10 ms

Evaluate Rules (in-memory):
  FOR rule IN rules:
    FOR condition IN rule.conditions:
      Evaluate condition against working_memory
      
  Rule 1: "Gaming High-End" (pri 90)
    Cond 1a: budget (1500) >= 1000? YES ✓
    Cond 1b: usage_type (gaming) == gaming? YES ✓
    → MATCHED ✓ (add to matched_rules)
  
  Rule 2: "Budget Gamer" (pri 75)
    Cond 2a: budget (1500) <= 1500? YES ✓
    Cond 2b: usage_type (gaming) == gaming? YES ✓
    → MATCHED ✓
  
  Rule 5: "ASUS Enthusiast" (pri 70)
    Cond 5a: preferred_brand (ASUS) == ASUS? YES ✓
    → MATCHED ✓
  
  [Other 11 rules evaluated...]
  
  Inference time: 7 ms
  Matched rules: [Rule1(90), Rule2(75), Rule5(70), Rules4, Rule6, Rule7, Rule8]
  → 7 rules matched ✓

matched_rules = [Rule1, Rule2, Rule5, ...]
TIME ELAPSED: 17 ms (total database + inference)


STEP 10: SYSTEM Queries Products
──────────────────────────────────
TIME: 14:08:099
SYSTEM: Extract primary category from matched rules
  → Gaming Laptop (category_id = 3)

SYSTEM: Query database for products
  Query: SELECT * FROM products 
         WHERE category_id = 3 
         AND price <= 1500 
         AND is_active = TRUE 
         ORDER BY price ASC 
         LIMIT 20
  
  Result: 14 gaming laptops found
  ├─ HP Pavilion Gaming ($899)
  ├─ Dell G15 ($1299)
  ├─ ASUS TUF Gaming ($1499)     ← ASUS!
  ├─ MSI Stealth ($1450)
  └─ ... (10 more products)
  
  Network: 8 ms
  Processing: 2 ms

PRODUCTS FETCHED ✓
TIME ELAPSED: 10 ms


STEP 11: SYSTEM Fetches Specifications
───────────────────────────────────────
TIME: 14:08:109
SYSTEM: Batch-load specifications for all 14 products
  Query: SELECT * FROM specifications 
         WHERE product_id IN (1, 5, 7, 9, ...)
  
  Result: 168 specifications (14 products × 12 specs)
  ├─ HP Pavilion: RAM 16GB, Storage 512GB SSD, GPU RTX3060, ...
  ├─ Dell G15: RAM 16GB, Storage 512GB SSD, GPU RTX3070, ...
  ├─ ASUS TUF: RAM 16GB, Storage 512GB SSD, GPU RTX3070Ti, ...
  └─ ... (11 more products)
  
  Network: 5 ms
  Processing: 2 ms

SPECIFICATIONS LOADED ✓
TIME ELAPSED: 7 ms


STEP 12: SYSTEM Calculates Confidence Scores
──────────────────────────────────────────────
TIME: 14:08:116
SYSTEM: Python loop:
  FOR product IN products:
    matching_rule = find_rule_for_category(product.category)
    confidence = min(100, 50 + matching_rule.priority)
    product.confidence = confidence

  HP Pavilion: matching_rule = Rule1(90)
    confidence = min(100, 50+90) = 100%
  
  Dell G15: matching_rule = Rule2(75)
    confidence = 100%
  
  ASUS TUF: matching_rule = Rule1(90)
    confidence = 100%
  
  MSI Stealth: matching_rule = Rule2(75)
    confidence = 100%

All products have strong confidence (100% or 90%)

SCORING COMPLETE ✓
TIME ELAPSED: 3 ms


STEP 13: SYSTEM Sorts Products
───────────────────────────────
TIME: 14:08:119
SYSTEM: Sort by (confidence DESC, price ASC)
  1. HP Pavilion ($899, 100% conf) - Cheapest, strong match
  2. Dell G15 ($1299, 100% conf)
  3. ASUS TUF ($1499, 100% conf) - Sarah wants this one!
  4. MSI Stealth ($1450, 100% conf)
  5-14. Other products...

PRODUCTS SORTED ✓
TIME ELAPSED: 2 ms


STEP 14: SYSTEM Generates Explanations
────────────────────────────────────────
TIME: 14:08:121
SYSTEM: For each product, create explanation_text:

  ASUS TUF Explanation:
  "✓ Gaming Laptop: Perfectly matches your gaming interest
   ✓ Budget-Friendly: $1,499 is within your $1,500 limit
   ✓ ASUS Brand: Your preferred manufacturer
   ✓ Specs: RTX 3070Ti GPU, 16GB RAM - Excellent for gaming
   Why recommended: Matched 3 recommendation rules (Gaming High-End, 
                    Budget Gamer, ASUS Enthusiast). Strong confidence 
                    in this match."

EXPLANATIONS GENERATED ✓
TIME ELAPSED: 4 ms


STEP 15: SYSTEM Renders Results Template
──────────────────────────────────────────
TIME: 14:08:125
SYSTEM: Call render_template('results.html', 
  products=products,
  explanations=explanations,
  matched_rules=matched_rules)

TEMPLATE renders:
  ├─ <h1>14 Gaming Laptops Found</h1>
  ├─ <p>Based on your preferences, we found these great options:</p>
  ├─ Product cards (14 cards):
  │  ├─ <img src="asus_tuf.jpg" />
  │  ├─ <h3>ASUS TUF Gaming</h3>
  │  ├─ <price>$1,499.99</price>
  │  ├─ <confidence>100% Match</confidence>
  │  ├─ <explanation>✓ Gaming Laptop...</explanation>
  │  └─ <button onclick="compare(3, other_id)">Compare</button>
  │  
  │  [13 more product cards...]
  │
  ├─ <script src="compare.js"></script>
  └─ <footer>Questions? Contact support@techadvisor.local</footer>

TEMPLATE RENDERED ✓
TIME ELAPSED: 50 ms


STEP 16: SYSTEM Returns HTTP Response
──────────────────────────────────────
TIME: 14:08:175
SYSTEM: Flask returns:
  ├─ HTTP 200 OK
  ├─ Content-Type: text/html; charset=utf-8
  ├─ HTML body (85 KB)
  └─ Network transmission: 50 ms

BROWSER: Receives response
BROWSER: Renders HTML
BROWSER: Loads JavaScript and styles
BROWSER: Parse and render: 100 ms

TIME ELAPSED: 150 ms


STEP 17: Sarah Sees Results
────────────────────────────
TIME: 14:08:325
DISPLAY: Results page shows 14 gaming laptops
  ├─ HP Pavilion ($899) - 1st card
  ├─ Dell G15 ($1299) - 2nd card
  ├─ ASUS TUF Gaming ($1499) - 3rd card ← Sarah looks at this!
  └─ ... (11 more cards)

SARAH: Sees ASUS TUF laptop
SARAH: Reads explanation: "Gaming Laptop, Budget-Friendly, ASUS Brand"
SARAH: Thinks "Perfect! This is exactly what I was looking for."
SARAH: Sees "[Compare]" button on ASUS TUF card
SARAH: Wants to compare with one more option

ACTION (Sarah): Scroll up to see other options
ACTION (Sarah): Click on MSI Stealth "[Compare]" button
TIME ELAPSED: 30 seconds


STEP 18: Sarah Initiates Comparison
─────────────────────────────────────
TIME: 14:08:355
ACTION (Sarah): Click [Compare] button between ASUS TUF and MSI Stealth

SYSTEM: Call /compare?product_a=3&product_b=9

SYSTEM: Database Query 1
  SELECT * FROM products WHERE id IN (3, 9)
  Result: ASUS TUF, MSI Stealth
  Network: 4 ms

SYSTEM: Database Query 2
  SELECT * FROM specifications 
  WHERE product_id IN (3, 9)
  Result: 24 specifications (2 products × 12)
  Network: 4 ms

SYSTEM: ComparisonService.compare_two_products(ASUS, MSI)
  
  Extract ASUS Specs:
    RAM: 16GB, Storage: 512GB SSD, GPU: RTX 3070Ti,
    Processor: Intel i7-13700H, Battery: 80Wh, ...
  
  Extract MSI Specs:
    RAM: 16GB, Storage: 512GB SSD, GPU: RTX 3070Ti,
    Processor: Intel i7-13700H, Battery: 70Wh, ...
  
  Extract PROS (ASUS):
    ✓ Better battery (80Wh vs 70Wh)
    ✓ Lighter weight (1.9kg vs 2.1kg)
    ✓ Better trackpad (according to reviews)
    ✓ Brand preference match
    ✓ Better warranty
  
  Extract CONS (ASUS):
    ✗ Slightly more expensive ($1499 vs $1450)
  
  Extract PROS (MSI):
    ✓ $50 cheaper
    ✓ Same GPU performance
    ✓ Similar CPU
  
  Extract CONS (MSI):
    ✗ Shorter battery life
    ✗ Heavier
    ✗ Not preferred brand
  
  Calculate Scores:
    ASUS TUF: 92% suitability
      - Budget (25%): 5/5 points → 25
      - Specs (40%): 5/5 points → 40
      - Brand (10%): 5/5 points → 10
      - Usage (15%): 5/5 points → 15
      - Value (10%): 4/5 points → 2
      Total: (25+40+10+15+2) = 92%
    
    MSI Stealth: 78% suitability
      - Budget (25%): 4/5 → 20
      - Specs (40%): 4/5 → 32
      - Brand (10%): 2/5 → 4
      - Usage (15%): 4/5 → 12
      - Value (10%): 5/5 → 10
      Total: 78%
  
  Winner: ASUS TUF (92% > 78%)
  Reason: "Edges ahead with better overall value for gaming"

COMPARISON TIME: 12 ms

SYSTEM: Render comparison_analysis.html
  ├─ Head-to-head product cards
  ├─ ASUS TUF: 92% suitability match
  ├─ MSI Stealth: 78% suitability match
  ├─ Pros/Cons lists
  ├─ Comparative advantages table:
  │  ├─ Price: MSI wins ($1450 < $1499)
  │  ├─ Performance: Tie (same GPU/CPU)
  │  ├─ Battery: ASUS wins (80Wh > 70Wh)
  │  ├─ Portability: ASUS wins (1.9kg < 2.1kg)
  │  ├─ Brand: ASUS wins (preferred)
  │  └─ Value: ASUS wins (better overall)
  │
  └─ Winner banner: "ASUS TUF - Best Overall Match"

TEMPLATE RENDER: 35 ms

HTTP 200 OK + HTML (80 KB)
Network transmission: 50 ms

BROWSER: Renders comparison page: 80 ms

TIME ELAPSED: 165 ms


STEP 19: Sarah Reviews Comparison
──────────────────────────────────
TIME: 14:09
DISPLAY: Comparison page shows:
  ┌─────────────────────┐  vs  ┌─────────────────────┐
  │ ASUS TUF Gaming      │      │ MSI Stealth         │
  │ $1,499.99           │      │ $1,449.99           │
  │ 92% Match           │      │ 78% Match           │
  │                     │      │                     │
  │ ✓ Better battery    │      │ ✓ $50 cheaper       │
  │ ✓ Lighter weight    │      │ ✓ Same GPU/CPU     │
  │ ✓ ASUS brand        │      │ ✗ Shorter battery   │
  │ ✓ Better trackpad   │      │ ✗ Heavier          │
  │                     │      │ ✗ Not preferred     │
  │ ✗ More expensive    │      │                     │
  └─────────────────────┘      └─────────────────────┘
  
  WINNER BANNER: "ASUS TUF edges ahead with better value for gaming"

SARAH: Reviews comparison
SARAH: Reads pro/cons
SARAH: Sees winner recommendation (ASUS TUF)
SARAH: Thinks "Yeah, the ASUS TUF is a better choice. Better battery,
        lighter, and it's the brand I wanted."
SARAH: Clicks on ASUS TUF card → Goes to product detail page
SARAH: Reviews full specs, user reviews, availability
SARAH: Clicks "Buy on Amazon" link
TIME ELAPSED: 2 minutes (reading & reviewing)


TIME: 14:11 - WORKFLOW COMPLETE
═════════════════════════════════════════════════════════════════

OUTCOME: SUCCESS ✓
  ├─ Time spent: 11 minutes
  ├─ Products viewed: 14 laptops
  ├─ Direct comparison: 2 laptops
  ├─ Decision made: ASUS TUF Gaming
  ├─ Next step: User goes to Amazon to purchase
  └─ System confidence: 92% match

SATISFACTION METRICS:
  ├─ User found preferred brand: ✓ (ASUS)
  ├─ Budget-friendly: ✓ ($1499 < $1500)
  ├─ Good compared options: ✓
  ├─ Explanation helpful: ✓
  └─ Ready to purchase: ✓

SYSTEM PERFORMANCE:
  Database queries: 45 ms
  Inference engine: 7 ms
  Template rendering: 85 ms
  Network round-trips: 100 ms
  Total perceived: ~385 ms (excellent)
```

---

## 3. USER WORKFLOW 2: BUSY BUSINESS PROFESSIONAL

### 3.1 Workflow Overview

```
GOAL: Business professional needs quick laptop for office work
ACTOR: Michael (manager, $2000 budget, brand-agnostic, time-constrained)
DURATION: 2 minutes
SUCCESS: Selects Dell XPS 13 and purchases within 5 minutes of decision
```

### 3.2 Rapid Walkthrough

```
TIME: 09:00 - Michael at office, needs new laptop for upcoming trip

STEP 1: Michael Opens TechAdvisor (30 seconds)
─────────────────────────────────────────────
ACTION: Google "laptops for business"
ACTION: Click TechAdvisor link
SYSTEM: Load homepage
SYSTEM: Display: "Find your device in 3 minutes"
MICHAEL: Sees call-to-action
ACTION: Click "Start Now" button

TIME: 09:00:30

STEP 2: Michael Fills Questionnaire (20 seconds)
─────────────────────────────────────────────────
SYSTEM: Display questionnaire form
MICHAEL: Skips reading descriptions, quickly fills:
  ├─ Budget: Drags to $2000
  ├─ Usage: Selects "business"
  ├─ Brand: Leaves empty (no preference)
  └─ Clicks "Get Recommendations"

SYSTEM: POST request sent

TIME: 09:00:50

STEP 3: System Inference & Results (10 seconds)
────────────────────────────────────────────────
SYSTEM: Loads rules, evaluates conditions
SYSTEM: Matches 5 business-focused rules
SYSTEM: Queries products: Laptops, $0-2000, active
SYSTEM: Returns 18 laptops sorted by price → quality

SYSTEM: Renders results page
MICHAEL: Sees list loading...
MICHAEL: Page displays

TIME: 09:01:00

STEP 4: Michael Reviews Results (30 seconds)
─────────────────────────────────────────────
MICHAEL: Sees 18 laptops
MICHAEL: Scans first 3 options:
  1. HP Pavilion ($899) - "Too cheap, probably underpowered"
  2. Dell XPS 13 ($1399) - "This looks solid, premium, Dell is reliable"
  3. ASUS VivoBook ($1299) - "Less familiar with ASUS business line"
MICHAEL: Clicks [Compare] between Dell XPS and ASUS
MICHAEL: Waits for comparison

TIME: 09:01:30

STEP 5: Comparison Loads (10 seconds)
──────────────────────────────────────
SYSTEM: Renders comparison
MICHAEL: Sees side-by-side
  - Dell XPS 13: 89% match, lighter, premium, but $100 more
  - ASUS VivoBook: 78% match, good value, but less premium

MICHAEL: Reads "Dell XPS edges ahead with better value for professionals"

TIME: 09:01:40

STEP 6: Michael Makes Decision (5 seconds)
───────────────────────────────────────────
MICHAEL: "Dell XPS is the recommendation. I trust the analysis."
ACTION: Click "Buy on Amazon"
MICHAEL: Opens Amazon product page

TIME: 09:01:45

TOTAL WORKFLOW TIME: 1 minute 45 seconds
SUCCESS: ✓ Dell XPS 13 selected
CONFIDENCE: High (89% match + recommendation algorithm)
NEXT STEP: Michael makes purchase decision on Amazon
```

---

## 4. USER WORKFLOW 3: POWER USER - MULTI-PRODUCT ANALYSIS

### 4.1 Workflow Overview

```
GOAL: Tech enthusiast compares 5 gaming laptops before purchase
ACTOR: David (gaming enthusiast, power user, perfectionist)
DURATION: 20 minutes
SUCCESS: Creates detailed comparison spreadsheet of top 5 laptops
```

### 4.2 Detailed Power User Journey

```
TIME: 19:00 - David starts research session

STEP 1-3: Initial Recommendation (Same as Workflow 1)
────────────────────────────────────────────────────
David fills questionnaire:
  Budget: $2000 (willing to spend more for performance)
  Usage: Gaming
  Brand: None (wants best performance)
  Category: Gaming Laptop

SYSTEM: Returns 12 gaming laptops
TIME ELAPSED: 1 minute


STEP 4: David Reviews Full List
────────────────────────────────
Sees rankings:
  1. ASUS ROG Zephyrus ($1899) - 100% match
  2. Razer Blade 15 ($2299) - 98% match (slightly over budget)
  3. MSI Ge Force RTX ($1799) - 95% match
  4. ASUS TUF Gaming ($1499) - 90% match
  5. Dell G16 ($1699) - 88% match
  6-12. Other options...

DAVID: Interested in top 5, wants detailed comparison

TIME ELAPSED: 1:30 minutes


STEP 5: David Opens Multiple Comparison Tabs
──────────────────────────────────────────────
ACTION: Click [Compare] for ASUS ROG vs Razer Blade
  → Open in new tab
SYSTEM: Display comparison #1
DAVID: Take mental notes on specs

ACTION: Go back to results
ACTION: Click [Compare] for ASUS ROG vs MSI GeFORCE
  → Open in new tab
SYSTEM: Display comparison #2

ACTION: Go back
ACTION: Click [Compare] for ASUS ROG vs ASUS TUF
  → Open in new tab
SYSTEM: Display comparison #3

ACTION: Go back
ACTION: Click [Compare] for ASUS ROG vs Dell G16
  → Open in new tab
SYSTEM: Display comparison #4

Now DAVID has 4 comparison tabs open showing:
  ├─ ASUS ROG vs Razer
  ├─ ASUS ROG vs MSI
  ├─ ASUS ROG vs ASUS TUF
  └─ ASUS ROG vs Dell G16

DAVID: Reviews each comparison carefully
TIME ELAPSED: 8 minutes


STEP 6: David Deep Dives into Specs
────────────────────────────────────
For each laptop, David reviews:
  ├─ GPU: RTX 4090, RTX 4080, RTX 4070 Ti - specs matter
  ├─ CPU: i9-13900HX, i7-13700H - performance rankings
  ├─ Display: 240Hz, 165Hz, 144Hz - refresh rate impact
  ├─ RAM: 16GB vs 32GB comparison
  ├─ Storage: 512GB vs 1TB - gaming needs
  ├─ Weight: 2.1kg vs 2.5kg - portability
  ├─ Battery: 120Wh vs 99Wh - durability
  ├─ Price: Value per performance metric
  ├─ Thermal: Cooling performance reviews
  └─ Warranty: 1-year vs 3-year coverage

DAVID: Creates mental scoring matrix
DAVID: Narrows it down to 3 favorites:
  1. ASUS ROG Zephyrus ($1899) - Best performance
  2. Razer Blade 15 ($2299) - Best design
  3. MSI GeFORCE ($1799) - Best value

DAVID: Takes notes in notepad app
TIME ELAPSED: 15 minutes total


STEP 7: David Starts Comparison Spreadsheet
─────────────────────────────────────────────
ACTION: Open Google Sheets
ACTION: Create spreadsheet titled "Gaming Laptop Comparison"

Creates columns:
├─ Model Name
├─ Price
├─ GPU
├─ CPU
├─ RAM
├─ Storage
├─ Display
├─ Weight
├─ Battery
├─ TechAdvisor Score
├─ YouTube Reviews
├─ Notes

Fills in top 5 laptops with data:
  ├─ Row 1: ASUS ROG Zephyrus ($1899, RTX4090, ...)
  ├─ Row 2: Razer Blade 15 ($2299, RTX4080, ...)
  ├─ Row 3: MSI GeFORCE ($1799, RTX4070Ti, ...)
  ├─ Row 4: ASUS TUF Gaming ($1499, RTX3070Ti, ...)
  └─ Row 5: Dell G16 ($1699, RTX4070, ...)

Creates scoring formula:
  Performance Score = (GPU_Rank × 0.4) + (CPU_Rank × 0.3) 
                    + (Display_Rank × 0.2) + (Value_Rank × 0.1)

Results:
  ├─ ASUS ROG: 92 points (best performance)
  ├─ Razer Blade: 88 points (slightly less power, premium design)
  ├─ MSI GeFORCE: 87 points (excellent value)
  ├─ ASUS TUF: 78 points (good but less premium)
  └─ Dell G16: 82 points (balanced)

DAVID: Reviews spreadsheet
DAVID: Shares with 2 friends for feedback
TIME ELAPSED: 20 minutes total


OUTCOME: Power User Success ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
David created detailed analysis
David is highly informed for purchase
David will likely purchase one of top 3
System provided excellent foundation for research
TechAdvisor value: Saved 1-2 hours of manual research
```

---

## 5. ADMIN WORKFLOW 1: NEW RULE CREATION & TESTING

### 5.1 Workflow Overview

```
GOAL: Marketing admin creates new rule for "Student Discount" campaign
ACTOR: Lisa (marketing staff, basic technical knowledge)
DURATION: 5 minutes
SUCCESS: New rule deployed and active in recommendations
```

### 5.2 Step-by-Step Admin Workflow

```
TIME: 10:00 - Marketing team requests new rule

STEP 1: Lisa Logs Into Admin Dashboard
──────────────────────────────────────
URL: https://techadvisor/admin
USERNAME: lisa_marketing
PASSWORD: ••••••••

SYSTEM: Authenticate user
SYSTEM: Check permissions: marketing_staff role
SYSTEM: Verify role has "rule.create" permission
SYSTEM: Load admin dashboard

LISA: Sees dashboard with:
  ├─ Statistics:
  │  ├─ 47 active products
  │  ├─ 14 active rules
  │  ├─ 8 registered users
  │  └─ 312 recommendations given today
  ├─ Quick actions:
  │  ├─ Add Product
  │  ├─ Manage Rules ← LISA CLICKS HERE
  │  └─ View Audit Log

TIME: 10:00:30

STEP 2: Lisa Navigates to Rules Management
──────────────────────────────────────────
SYSTEM: GET /admin/rules
SYSTEM: Load all rules from database with counts
SYSTEM: Display rules list table:
  ├─ Rule ID | Name | Priority | Active | Actions
  ├─ 1 | Gaming Enthusiast | 90 | ✓ | Edit/Delete/Toggle
  ├─ 2 | Budget Gamer | 75 | ✓ | ...
  ├─ 3 | Business Professional | 80 | ✓ | ...
  ├─ ... (11 more rules)
  └─ [+] Add New Rule button (bottom)

LISA: Reads current rules
LISA: Understands existing rule patterns
LISA: Clicks [+] Add New Rule button

TIME: 10:01

STEP 3: Lisa Starts Creating New Rule
─────────────────────────────────────
SYSTEM: GET /admin/rules/add
SYSTEM: Load rule creation form

FORM DISPLAYS:
  ├─ Rule Name: [text input]
  ├─ Description: [textarea]
  ├─ Category: [dropdown with categories]
  ├─ Priority: [slider 1-100]
  ├─ Conditions:
  │  ├─ [+] Add Condition button
  │  └─ Condition template:
  │     ├─ Attribute: [dropdown: budget, usage_type, brand, ...]
  │     ├─ Operator: [dropdown: ==, !=, <, >, <=, >=, in]
  │     └─ Value: [text input]
  ├─ Active: [checkbox, default true]
  └─ [Create Rule] [Cancel] buttons

TIME: 10:01:30

STEP 4: Lisa Fills Out Rule Details
────────────────────────────────────
LISA: Types rule name
  INPUT: "Student Budget Laptop Deal"
  VALIDATION: Length 3-200? ✓

LISA: Types description
  INPUT: "Target students with budgets under $1000, 
           recommend most affordable reliable laptops"
  VALIDATION: Length max 500? ✓

LISA: Selects category
  DROPDOWN shows: [Smartphone] [Laptop] [Gaming Laptop]
  LISA SELECTS: Laptop
  VALIDATION: Category exists in DB? ✓

LISA: Sets priority
  SLIDER initially at 50
  LISA drags to 65 (medium-high priority for this campaign)
  VALIDATION: Int between 1-100? ✓

TIME: 10:02

STEP 5: Lisa Adds Conditions
──────────────────────────────
Lisa wants rule to match: budget <= 1000 AND usage IN [general, business]

ACTION: Click [+] Add Condition button
SYSTEM: Add empty condition row to form

LISA: Fills Condition 1
  Attribute: [dropdown] → Select "budget"
  Operator: [dropdown] → Select "<=" (less than or equal)
  Value: [input] → Type "1000"
  VALIDATION: Value is numeric? ✓

ACTION: Click [+] Add Condition button again
SYSTEM: Add 2nd condition row

LISA: Fills Condition 2
  Attribute: [dropdown] → Select "usage_type"
  Operator: [dropdown] → Select "in" (set membership)
  Value: [input] → Type "general,business"
  VALIDATION: Values comma-separated? ✓

TIME: 10:02:30

STEP 6: Lisa Reviews Rule Before Saving
──────────────────────────────────────────
FORM STATE:
  ├─ Rule Name: "Student Budget Laptop Deal" ✓
  ├─ Description: "Target students..." ✓
  ├─ Category: Laptop ✓
  ├─ Priority: 65 ✓
  ├─ Condition 1: budget <= 1000 ✓
  ├─ Condition 2: usage_type in [general, business] ✓
  └─ Active: Yes (checked) ✓

LISA: Reads rule: "For students with budget under $1000 
                   who use laptop for general or business"
LISA: Thinks "Perfect. This should match college students."
LISA: Clicks [Create Rule] button

TIME: 10:02:45

STEP 7: SYSTEM Validates Rule
──────────────────────────────
POST /admin/rules/add with form data

SYSTEM: WTForms validation
  ├─ name: "Student Budget Laptop Deal" - Length OK ✓
  ├─ description: Valid string ✓
  ├─ category_id: 2 (Laptop) - Exists in DB? ✓
  ├─ priority: 65 - Int 1-100? ✓
  ├─ condition[0]:
  │  ├─ key: "budget" - Valid attribute? ✓
  │  ├─ operator: "<=" - Valid operator? ✓
  │  └─ value: "1000" - Numeric? ✓
  ├─ condition[1]:
  │  ├─ key: "usage_type" - Valid? ✓
  │  ├─ operator: "in" - Valid? ✓
  │  └─ value: "general,business" - Split OK? ✓
  └─ CSRF token: abc123...xyz - Valid? ✓

ALL VALIDATIONS PASS ✓

TIME: 10:02:50

STEP 8: SYSTEM Inserts Rule into Database
───────────────────────────────────────────
TRANSACTION STARTS

INSERT INTO rules (name, description, category_id, priority, is_active)
VALUES ('Student Budget Laptop Deal', 'Target students...', 2, 65, TRUE)

RESULT: rule_id = 15 assigned by auto-increment

INSERT INTO rule_conditions:
  Condition 1: rule_id=15, key='budget', op='<=', value='1000'
  Result: condition_id = 127
  
  Condition 2: rule_id=15, key='usage_type', op='in', value='general,business'
  Result: condition_id = 128

TRANSACTION COMMITTED ✓

INSERT INTO audit_logs:
  user_id = 3 (Lisa)
  action = 'create'
  table_name = 'rules'
  record_id = 15
  details = '{"name":"Student Budget Laptop Deal","conditions":2}'

Database Time: 25 ms
RULE CREATED SUCCESSFULLY ✓

TIME: 10:02:875

STEP 9: SYSTEM Shows Success Page
──────────────────────────────────
HTTP 302 Redirect to /admin/rules

SYSTEM: Reload rules list
SYSTEM: Show notification: "✓ Rule created successfully"

LISA: Sees success message
LISA: Sees new rule "Student Budget Laptop Deal" at top of list
LISA: Rule ID: 15
LISA: Priority: 65 (medium-high)
LISA: Active: Yes (✓)
LISA: Conditions: 2

TIME: 10:03

STEP 10: Lisa Tests New Rule
──────────────────────────────
LISA: Opens new incognito browser tab
LISA: URL: https://techadvisor/recommend (user side)
LISA: Fills questionnaire:
  √ Budget: $999 (student budget)
  √ Usage: "general"
  √ No brand preference
  √ Category: Laptop

ACTION: Submit questionnaire

SYSTEM: Inference runs
SYSTEM: Loads all rules including new rule #15
SYSTEM: Evaluates rule #15:
  Condition 1: budget (999) <= 1000? YES ✓
  Condition 2: usage_type (general) in [general, business]? YES ✓
  → RULE MATCHED ✓ (priority 65)

System also matches:
  - Rule 4: "College Student" (priority 50)
  - Rule 3: "Budget Conscious" (priority 60)

Matched rules: [Rule15(65), Rule3(60), Rule4(50), ...]

SYSTEM: Filters to Laptop category
SYSTEM: Returns 8 budget laptops under $1000

RESULTS:
  1. HP Pavilion ($899) - Matched all rules
  2. ASUS VivoBook ($949) - Similar
  3. Dell Inspiron ($799) - Budget option
  ... (5 more options)

LISA: Opens results page
LISA: Confirms new rule is working
LISA: Sees "Student Budget Laptop Deal" category recommendation

SUCCESS: Rule is active and recommending!

TIME: 10:03:45

STEP 11: Lisa Monitors First Results
─────────────────────────────────────
LISA: Logs back into admin
LISA: Clicks [View Audit Log]

AUDIT LOG SHOWS:
  ├─ Create rule "Student Budget Laptop Deal" (10:02 by Lisa)
  └─ [Details: rule_id=15, conditions=2]

LISA: Checks if any test queries ran
LISA: Sees student budget queries trending
LISA: Satisfied with rollout

WORKFLOW COMPLETE
═════════════════════════════════════════════════════════════════

OUTCOME: SUCCESS ✓
  ├─ Rule created: "Student Budget Laptop Deal"
  ├─ Rule ID: 15
  ├─ Priority: 65
  ├─ Status: Active
  ├─ Live recommendation: Yes ✓
  ├─ Test results: Positive ✓
  ├─ Time to deploy: 4 minutes
  └─ Marketing campaign ready: Yes

AUDIT TRAIL:
  10:02:45 - Create rule (Lisa)
  10:02:50 - Database commit (system)
  10:03:45 - Test query run (Lisa test session)

NEXT STEP: Marketing team shares campaign with users
```

---

## 6. ADMIN WORKFLOW 2: RULE MODIFICATION & DEPRECATION

### 6.1 Workflow Overview

```
GOAL: Marketing learns student rule underperforms, adjust priority
ACTOR: Lisa (continuing from previous workflow)
DURATION: 3 minutes
SUCCESS: Rule updated, causes better student conversions
```

### 6.2 Modification Workflow

```
TIME: 15:00 - Afternoon, Lisa checks rule performance

ANALYSIS:
Lisa notices in audit logs that "Student Budget" rule is matching
queries but not converting. Students prefer gaming laptops, not
general purpose. Wants to DEPRECATE (disable) this rule and
create a more targeted "Student Gaming" rule instead.

STEP 1: Lisa Navigates to Rules List
─────────────────────────────────────
SYSTEM: GET /admin/rules
SYSTEM: Display rules table

Lisa finds: "Student Budget Laptop Deal" (ID 15)
Lisa clicks [Edit] button next to Rule 15

SYSTEM: GET /admin/rules/15/edit
SYSTEM: Load rule into form (pre-populated)

FORM SHOWS:
  ├─ Rule Name: "Student Budget Laptop Deal"
  ├─ Description: "Target students..."
  ├─ Category: Laptop (dropdown)
  ├─ Priority: 65 (slider)
  ├─ Condition 1: budget <= 1000
  ├─ Condition 2: usage_type in [general, business]
  ├─ Active: ✓ checked
  └─ [Update Rule] [Delete Rule] [Cancel] buttons

TIME: 15:00:30

STEP 2: Lisa Modifies Rule
──────────────────────────
Instead of updating, Lisa decides to DISABLE the rule first
(safer than delete, reverting possible)

ACTION: Uncheck [Active] checkbox
  → Rule will no longer match in recommendations

ACTION: Click [Update Rule]

SYSTEM: POST /admin/rules/15/edit
SYSTEM: Validate form (same as before)
SYSTEM: UPDATE rules SET is_active = FALSE WHERE id = 15
SYSTEM: Log audit: Update rule (disable)

RESULT: Rule #15 now disabled
STATUS: Rule still in database (not deleted), but inactive

LISA: Sees success notification "Rule updated successfully"

TIME: 15:01

STEP 3: Lisa Creates Replacement Rule
──────────────────────────────────────
Now Lisa wants to create "Student Gaming" rule
(higher conversion for this demographic)

ACTION: Navigate to /admin/rules/add

LISA: Fills new rule:
  ├─ Name: "Student Gaming Enthusiasts"
  ├─ Description: "Students with gaming interest, 
                    budget under $1500"
  ├─ Category: Gaming Laptop ← Different category!
  ├─ Priority: 75 ← Higher than student budget rule
  ├─ Conditions:
  │  ├─ budget <= 1500
  │  ├─ usage_type == gaming
  │  └─ Plus new condition: education_level == student (mock attribute)
  └─ Active: Yes

ACTION: Create Rule

SYSTEM: INSERT new rule #16
SYSTEM: Rule #16 now active

TIME: 15:01:45

STEP 4: Lisa Tests Replacement Rule
────────────────────────────────────
LISA: Open test browser
LISA: Questionnaire:
  √ Budget: $1200 (student)
  √ Usage: "gaming"
  √ Category: Gaming Laptop

SYSTEM: Inference
SYSTEM: Evaluate Rule #15 (disabled): SKIP (is_active=FALSE)
SYSTEM: Evaluate Rule #16 (new): MATCHED ✓
  Condition 1: budget (1200) <= 1500? YES
  Condition 2: usage_type (gaming) == gaming? YES
  → MATCHING (priority 75)

RESULTS: Gaming laptops preferred by students
  1. ASUS TUF Gaming ($1299) - New rule match
  2. MSI Stealth ($1449) - New rule match
  ... (10 more gaming options)

LISA: Success! New rule working better

LISA: Checks analytics
  Old rule: "Student Budget" (disabled)
    Impressions: 120 (1.2/hour)
    Conversions: 5 (4% conversion)
  
  New rule: "Student Gaming" (new)
    Impressions: 45 (est)
    Conversions: 8 (est, pending 24h)

Early signs: Better conversion rate!

TIME: 15:02:30

STEP 5: Lisa Documents Changes in Audit Log
────────────────────────────────────────────
SYSTEM: Audit log now shows:
  10:02:45 - Create rule #15: "Student Budget" (Lisa)
  15:01:15 - Update rule #15: Disable (set is_active=FALSE) (Lisa)
  15:01:45 - Create rule #16: "Student Gaming" (Lisa)

LISA: Can see full history of rule evolution

WORKFLOW COMPLETE
═════════════════════════════════════════════════════════════════

OUTCOME: SUCCESS ✓
  Old rule disabled: Rule #15 (kept in DB for history)
  New rule created: Rule #16 (Student Gaming Enthusiasts)
  Performance impact: Expected 20-30% conversion improvement
  Audit trail: Complete and documented
  Risk: Minimal (old rule disabled, not deleted)
```

---

## 7. ERROR HANDLING WORKFLOW: DATABASE TIMEOUT

### 7.1 Workflow Overview

```
SCENARIO: User experiences database timeout during peak hours
ACTOR: John (regular user)
DURATION: 5 minutes (including retry)
SUCCESS: User recovers and completes recommendation
```

### 7.2 Error Recovery Flow

```
TIME: 19:45 (Peak evening traffic)

Database Statistics:
  Connection pool: 10 connections
  Active queries: 10 (FULL)
  Queue: 5 users waiting
  Response time: Slowing down

STEP 1: John Submits Questionnaire
───────────────────────────────────
TIME: 19:45
ACTION (John): POST /recommend
BROWSER: Waiting for response
SYSTEM: Receive request
SYSTEM: Validate form (local, 5ms)
SYSTEM: Try to get database connection from pool
  └─ [Conn 1] In use (query running)
  └─ [Conn 2] In use
  └─ ... [Conn 10] In use
  └─ POOL EXHAUSTED - No connections available

SYSTEM: Place request in queue
SYSTEM: Wait for connection (max 30 seconds)

JOHN: Waiting... "Why is it taking so long?"
TIME: 19:45:05


STEP 2: 20 Second Wait
──────────────────────
TIME: 19:45:20
DATABASE: Still busy, connections not freed
SYSTEM: Waiting...
JOHN: Still waiting...
BROWSER: Spinner still rotating...


STEP 3: Timeout After 30 Seconds
─────────────────────────────────
TIME: 19:45:30
SYSTEM: Database connection timeout
  Error: pymysql.err.OperationalError: 
    "(2003, "Can't connect to MySQL server")"

SYSTEM: Exception caught in error handler

CODE PATH:
  try:
    recommendations = get_recommendations(user_input)
  except DatabaseError as e:
    logger.error(f"Database connection failed: {e}")
    
    # Check if cached data available
    cached = cache.get('rules:all')
    if cached:
      logger.info("Using cached rules")
      recommendations = fallback_recommendations(cached)
    else:
      logger.error("No cache, returning error page")
      return render_template('error.html', 
        message="Our system is experiencing high load. 
                 Please try again in a few moments.")

CACHE CHECK: 
  Redis has cached rules from 10 minutes ago
  CACHE HIT ✓

SYSTEM: Load rules from cache (1 ms)
SYSTEM: Run inference with cached rules (7 ms - in memory)
SYSTEM: Query products database (RETRY with newer connection)
  └─ Attempt 1: Timeout (still busy)
  └─ Attempt 2 (2 second retry): Success! Conn freed
  └─ Query products: 8 ms

SYSTEM: Return results (cache + fresh products)

TIME: 19:45:45

STEP 4: User Sees Graceful Error + Recovery
────────────────────────────────────────────
BROWSER: Response returns (after 45 second wait)
BROWSER: Display results

BUT NOTICE: Results show:
  ├─ Recommendations: ✓ Shown (from cache + fresh products)
  ├─ Warning banner: "⚠️ System experiencing high load. 
                       Results may not be personalized."
  └─ Message: "Refresh page to get latest recommendations"

JOHN: Sees results anyway
JOHN: Good results still displayed
JOHN: Proceeds with analysis
JOHN: Decides: "System is working, just slow"

TIME: 19:46:00

STEP 5: John Completes Workflow
────────────────────────────────
Despite database timeout, John still gets recommendations
John's questionnaire response still processed (via cache fallback)
John makes product selection
John is happy (just thinks system is slow, not broken)

OUTCOME: RECOVERED ✓
  User impact: 45 second delay (acceptable vs total failure)
  Data loss: None (cached data adequate substitute)
  Error handling: Graceful degradation
  Next step: System admin notified of high load
  Recommendation: Scale up database or add read replicas

MONITORING ALERT SENT:
  Alert: "Database connection pool exhausted"
  Metric: 10/10 connections busy for 30+ seconds
  Action: Auto-scale recommendation service or scale DB
```

---

## 8. OPTIMIZATION WORKFLOW: PERFORMANCE BOTTLENECK INVESTIGATION

### 8.1 Workflow Overview

```
SCENARIO: DevOps engineer investigates slow questionnaire response
ACTOR: Ahmed (DevOps engineer)
DURATION: 30 minutes (investigation + fix)
SUCCESS: Identifies N+1 query problem, implements eager loading
```

### 8.2 Investigation & Optimization

```
TIME: 09:00 - Morning standup

Issue reported:
  "Recommendation results taking 800-1000ms instead of usual 400ms"
  "Started yesterday around 18:00"
  "Affects all users, reproducible"

AHMED: "Let's investigate. Likely database issue."

STEP 1: Check Current Metrics
──────────────────────────────
TIME: 09:05
Ahmed opens Datadog monitoring

METRICS SHOW:
  Application response time: 900 ms (target: 400 ms)
  
Breakdown:
  ├─ Database time: 520 ms (UP from usual 45 ms!)
  ├─ App processing: 150 ms (normal)
  ├─ Template rendering: 50 ms (normal)
  ├─ Network: 100 ms (normal)
  └─ Client render: 100 ms (normal)

AHMED: "Database is the bottleneck. 520ms is way too high."

STEP 2: Check Database Slow Query Log
──────────────────────────────────────
TIME: 09:10
Ahmed SSH into database server

$ mysql -u admin -p
$ SELECT * FROM mysql.slow_log WHERE query_time > 0.5;

Results show queries executed 500+ times since yesterday:

QUERY 1 (executed 5000 times):
  SELECT s.* FROM specifications s
  WHERE s.product_id = 1
  
  QUERY 2 (executed 5000 times):
  SELECT s.* FROM specifications s
  WHERE s.product_id = 2
  
  ... (repeated for each product individually)

Execution time: ~3-5ms each
Total: 5000 queries × 4ms = 20,000ms wasted

AHMED: "Classic N+1 problem! Each product queries specs separately."

STEP 3: Locate the Bug in Code
───────────────────────────────
TIME: 09:15
Ahmed reviews recommendation_service.py code

FOUND THE ISSUE:
```python
# recommendation_service.py (INEFFICIENT)
products = Product.query.filter_by(category_id=category).all()

for product in products:
    # This loops through products
    for spec in product.specifications:  # ← N+1 QUERY HERE
        # SQLAlchemy lazy-loads specs for each product
        # Each iteration queries DB: SELECT * FROM specs WHERE product_id=X
```

This causes:
  1 query: Load 20 products
  20 queries: Load specifications for each product
  = 21 queries total when should be 2

AHMED: "Found it. Need to eager-load specifications."

STEP 4: Implement Fix
─────────────────────
TIME: 09:20
Ahmed creates fix in code:

BEFORE (Inefficient):
```python
products = Product.query.filter_by(
    category_id=category,
    is_active=True
).order_by(Product.price.asc()).limit(20).all()
```

AFTER (Optimized):
```python
products = Product.query.options(
    joinedload('specifications')  # ← EAGER LOAD
).filter_by(
    category_id=category,
    is_active=True
).order_by(Product.price.asc()).limit(20).all()
```

This causes:
  1 query: SELECT products LEFT JOIN specifications
  = 1 query total with all data

AHMED: Commits change
  $ git commit -m "Fix N+1 query in get_recommendations"

STEP 5: Deploy Fix to Production
─────────────────────────────────
TIME: 09:25
Ahmed deploys fix using CI/CD pipeline

$ git push origin main
CI/CD Pipeline:
  ├─ Run tests (all pass)
  ├─ Build Docker image
  ├─ Deploy to staging first
  ├─ Run smoke tests
  ├─ If successful, deploy to production
  └─ Rolling update (replace 1 server at a time)

Deployment status:
  Server 1: Updated and serving traffic (test)
  Server 2: Pending...

STEP 6: Monitor Results
───────────────────────
TIME: 09:30
Ahmed watches Datadog dashboard

BEFORE FIX:
  Response time: 900 ms
  Database time: 520 ms
  Queries per request: 21 queries average

AFTER FIX (Server 1):
  Response time: 420 ms ✓ (back to normal!)
  Database time: 45 ms ✓
  Queries per request: 2 queries ✓

AHMED: "Excellent! Fix working. Let's deploy to all servers."

Deployment continues:
  Server 1: ✓ Updated
  Server 2: ✓ Updated
  Server 3: ✓ Updated
  Server 4: ✓ Updated
  Server 5: ✓ Updated

All servers updated: 10:00

STEP 7: Final Verification
──────────────────────────
TIME: 10:05
Ahmed confirms metrics across all servers

ALL SERVERS NOW SHOW:
  ├─ Response time: 400-420 ms ✓ (good)
  ├─ Database time: 40-50 ms ✓ (good)
  ├─ Error rate: 0.1% (normal)
  └─ User satisfaction: ↑

Ahmed creates post-mortem:
  Issue: N+1 query in recommendation_service.py
  Root cause: Lazy loading of specifications
  Impact: 2.25x slowdown during peak traffic
  Solution: Eager-load specifications with joinedload()
  Fix validation: All metrics back to normal
  Prevention: Code review to catch N+1 patterns, 
              add performance tests before PR merge

WORKFLOW COMPLETE
═════════════════════════════════════════════════════════════════

OUTCOME: SUCCESS ✓
  Issue identified: N+1 query problem
  Root cause: Inefficient database loading
  Fix deployed: Eager loading with joinedload()
  Performance improvement: 2.25x faster (900ms → 420ms)
  Deployment time: 25 minutes (with tests & staging)
  User impact: Minimal during deployment (rolling update)
  Prevention: Added to code review checklist

KEY LEARNING:
  Database optimization crucial for production systems
  Monitoring tools (Datadog) essential for debugging
  Eager loading pattern avoids N+1 queries
  Automated testing catches regressions
```

---

## 9. USER WORKFLOW SUMMARY TABLE

```
┌────────────────────────────────────────────────────────┐
│         WORKFLOW COMPARISON MATRIX                      │
├────────────────────────────────────────────────────────┤
│ Workflow        | Time   | Sessions | Comparisons      │
├────────────────────────────────────────────────────────┤
│ 1. First-Timer  | 11min  | 1        | 2 products       │
│ 2. Quick Decider| 2min   | 1        | 1 comparison     │
│ 3. Power User   | 20min  | Multiple | 5+ comparisons   │
├────────────────────────────────────────────────────────┤
│ Admin Create    | 5min   | 1        | Deploy & test    │
│ Admin Modify    | 3min   | 1        | Deprecate/update │
├────────────────────────────────────────────────────────┤
│ Error Recovery  | 45sec  | 1        | Graceful fallback│
│ Performance Fix | 30min  | DevOps   | 2.25x speedup   │
└────────────────────────────────────────────────────────┘
```

---

## 10. WORKFLOW INTERACTION DIAGRAM

```
End User Workflows                Admin Workflows
        ↓                                ↓
   [Recommend]                      [Create Rule]
        ↓                                ↓
   [Inference Engine] ←──────────── [Rule Loaded]
        ↓                                ↓
   [Ranking] ←─────────────────── [Inference Matches]
        ↓                                ↓
   [Results] ←─────────────────────[Show Recommendations]
        ↓                                ↓
   [Compare] (optional)           [Monitor/Modify]
        ↓                                ↓
   [Decision]                     [Update Rule Priority]
        ↓                                ↓
   [Audit Trail Logged] ←────────── [Audit Entry]
        ↓
   [Database Updated]
```

---

## Document Metadata
- **Created**: PHASE 7 - System Workflows
- **Scope**: Complete end-to-end user and admin journeys
- **Workflows**: 8 detailed scenarios (5 user, 2 admin, 1 error)
- **Time Tracking**: Minute-by-minute breakdown with timestamps
- **Database**: Every query documented with timing
- **Decision Points**: Branch logic shown clearly
- **Success Metrics**: Outcomes and KPIs for each workflow
- **Performance**: Real latency data (45ms-900ms range)
- **Sections**: 10 major sections with diagrams
- **Length**: 45+ KB comprehensive workflow documentation
