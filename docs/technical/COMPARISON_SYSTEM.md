# Product Specification & Comparison System

This document explains how TechAdvisor understands product specifications, compares products, and determines which product is better for different use cases.

---

## System Overview

```
┌─────────────────┐     ┌────────────────────┐     ┌─────────────────┐
│  Specifications │────▶│  ComparisonService │────▶│   Analysis UI   │
│   (Database)    │     │   (Business Logic) │     │   (Templates)   │
└─────────────────┘     └────────────────────┘     └─────────────────┘
```

---

## 1. How Specifications are Stored

### Database Model

**File:** [app/models/product.py](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/models/product.py#L73-89)

```python
class Specification(db.Model):
    """Specification model for product technical details"""
    __tablename__ = 'specifications'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    spec_key = db.Column(db.String(100), nullable=False)    # e.g., "RAM", "Storage"
    spec_value = db.Column(db.Text, nullable=False)         # e.g., "16GB", "512GB SSD"
```

**Key Design Decision:** Specifications use a **key-value pattern** instead of fixed columns, allowing:
- Different products to have different specifications
- Easy addition of new specification types
- Flexible querying and comparison

### How Products Access Specifications

**File:** [app/models/product.py](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/models/product.py#L54)

```python
class Product(db.Model):
    # ...
    specifications = db.relationship('Specification', backref='product', 
                                     lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            # ...
            'specifications': {spec.spec_key: spec.spec_value for spec in self.specifications}
        }
```

---

## 2. Comparison Service Architecture

**File:** [app/services/comparison_service.py](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/services/comparison_service.py)

### Class Structure

```python
class ComparisonService:
    def __init__(self):
        # Category-specific benchmarks for evaluation
        self.benchmarks = {...}
        # Keywords to identify spec types
        self.spec_keywords = {...}
    
    # Main comparison method
    def compare_two_products(product1, product2, user_preferences) -> Dict
    
    # Analysis methods
    def extract_pros(product, user_preferences) -> List[str]
    def extract_cons(product, user_preferences) -> List[str]
    def get_comparative_advantages(product1, product2) -> Dict
    def calculate_overall_score(product, user_preferences) -> float
```

---

## 3. How the System Knows What's "Better"

### 3.1 Category Benchmarks

**File:** [comparison_service.py L14-30](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/services/comparison_service.py#L14-30)

```python
self.benchmarks = {
    'smartphone': {
        'ram': {'excellent': 12, 'good': 8, 'minimum': 6},
        'storage': {'excellent': 256, 'good': 128, 'minimum': 64},
        'battery': {'excellent': 5000, 'good': 4000, 'minimum': 3000},
        'camera_mp': {'excellent': 108, 'good': 48, 'minimum': 12}
    },
    'laptop': {
        'ram': {'excellent': 16, 'good': 8, 'minimum': 4},
        'storage': {'excellent': 512, 'good': 256, 'minimum': 128},
        'ssd': {'excellent': 1024, 'good': 512, 'minimum': 256},
        'battery_hours': {'excellent': 12, 'good': 8, 'minimum': 5}
    }
}
```

### 3.2 Specification Keywords

**File:** [comparison_service.py L32-41](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/services/comparison_service.py#L32-41)

```python
self.spec_keywords = {
    'performance': ['processor', 'cpu', 'ram', 'memory', 'graphics', 'gpu'],
    'storage': ['storage', 'ssd', 'hard drive', 'hdd', 'rom'],
    'display': ['display', 'screen', 'resolution', 'refresh rate'],
    'camera': ['camera', 'mp', 'megapixel', 'lens'],
    'battery': ['battery', 'mah', 'charging', 'power'],
    'connectivity': ['5g', '4g', 'wifi', 'bluetooth', 'nfc'],
    'build': ['weight', 'build', 'material', 'waterproof', 'durability']
}
```

---

## 4. Extracting Pros & Cons

### 4.1 Pros Extraction Logic

**File:** [comparison_service.py L114-222](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/services/comparison_service.py#L114-222)

```python
def extract_pros(self, product: Product, user_preferences: Dict) -> List[str]:
    pros = []
    category_name = product.category.name.lower()
    
    # 1. Budget-based pros
    if price <= budget * 0.7:
        pros.append(f"Excellent value - priced at ${price}, well under budget")
    
    # 2. Brand preference match
    if product.brand.name.lower() == preferred_brand.lower():
        pros.append(f"Your preferred brand: {product.brand.name}")
    
    # 3. Specification analysis
    for spec in product.specifications:
        # RAM analysis
        if 'ram' in spec_key:
            if ram_value >= benchmark['excellent']:
                pros.append(f"Excellent RAM capacity: {spec.spec_value}")
        
        # Storage analysis
        if 'storage' in spec_key:
            if storage_value >= benchmark['excellent']:
                pros.append(f"Ample storage space: {spec.spec_value}")
        
        # Display quality
        if 'oled' or 'amoled' or '4k' in value:
            pros.append(f"Premium display: {spec.spec_value}")
        
        # ... more checks for processor, graphics, connectivity
    
    return pros[:6]  # Limit to top 6 pros
```

### 4.2 Cons Extraction Logic

**File:** [comparison_service.py L224-307](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/services/comparison_service.py#L224-307)

```python
def extract_cons(self, product: Product, user_preferences: Dict) -> List[str]:
    cons = []
    
    # 1. Budget check
    if price > budget:
        cons.append(f"Over budget by ${price - budget}")
    
    # 2. Missing specs
    if not has_ram_spec:
        cons.append("RAM specifications not disclosed")
    
    # 3. Below-minimum specs
    if ram_value < benchmark['minimum']:
        cons.append(f"Limited RAM: {value} may struggle with multitasking")
    
    if battery_value < 3500:  # For smartphones
        cons.append(f"Smaller battery: may require frequent charging")
    
    # 4. Missing features
    if category == 'smartphone' and not has_5g:
        cons.append("No 5G support (4G only)")
    
    return cons[:6]
```

---

## 5. Comparative Advantages

**File:** [comparison_service.py L309-389](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/services/comparison_service.py#L309-389)

Determines which product wins in each category:

```python
def get_comparative_advantages(self, product1, product2) -> Dict:
    advantages = {}
    
    # Price comparison
    if price1 < price2:
        advantages['Price'] = {
            'winner': 1,
            'reason': f"{product1.name} is ${price2 - price1} cheaper"
        }
    
    # RAM comparison
    winner, reason = self._compare_numeric_specs(ram1, ram2, ...)
    advantages['RAM'] = {'winner': winner, 'reason': reason}
    
    # Storage, Battery, Processor comparisons...
    
    return advantages
```

---

## 6. Overall Score Calculation

**File:** [comparison_service.py L391-477](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/services/comparison_service.py#L391-477)

```python
def calculate_overall_score(self, product, user_preferences) -> float:
    score = 50.0  # Base score
    
    # Budget alignment (25% weight)
    if price <= budget:
        budget_ratio = price / budget
        score += 25 * (1 - abs(budget_ratio - 0.8))  # Optimal at 80% of budget
    else:
        score -= 15  # Penalty for over budget
    
    # Specification quality (40% weight)
    for spec in product.specifications:
        if 'ram' in spec_key:
            if ram >= benchmark['excellent']: spec_score += 10
            elif ram >= benchmark['good']: spec_score += 6
            else: spec_score += 2
        # ... similar for storage
        
        # Premium features bonus
        if 'oled' or '5g' or 'rtx' in value:
            spec_score += 5
    
    score += min(40, spec_score)
    
    # Brand preference (10% weight)
    if matches_preferred_brand:
        score += 10
    
    # Usage alignment (15% weight)
    if usage == 'gaming' and has_dedicated_graphics:
        score += 15
    
    return max(0, min(100, score))
```

### Score Weight Summary

| Factor | Weight | Description |
|--------|--------|-------------|
| Budget Alignment | 25% | Optimal at 80% of budget |
| Spec Quality | 40% | RAM, storage, premium features |
| Brand Preference | 10% | Matches user's preferred brand |
| Usage Alignment | 15% | Features match intended use |
| **Base Score** | 50 | Starting point for all products |

---

## 7. Processor Rating

**File:** [comparison_service.py L525-561](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/services/comparison_service.py#L525-561)

```python
def _rate_processor(self, processor_name: str) -> int:
    processor = processor_name.lower()
    
    # Intel ratings
    if 'i9' in processor: return 9
    if 'i7' in processor: return 7
    if 'i5' in processor: return 5
    if 'i3' in processor: return 3
    
    # AMD ratings
    if 'ryzen 9' in processor: return 9
    if 'ryzen 7' in processor: return 7
    if 'ryzen 5' in processor: return 5
    
    # Apple ratings
    if 'm3' in processor: return 9
    if 'm2' in processor: return 8
    if 'm1' in processor: return 7
    
    # Mobile (Qualcomm)
    if 'snapdragon 8' in processor: return 8
    if 'snapdragon 7' in processor: return 6
    
    return 5  # Default
```

---

## 8. Route Integration

### Compare Route (2-4 Products)

**File:** [app/routes/user.py L55-113](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/routes/user.py#L55-113)

```python
@user_bp.route('/compare')
def compare():
    # Parse product IDs from URL: /compare?ids=1,2,3
    ids = [int(id) for id in product_ids.split(',')]
    
    # Fetch products with specs
    products = Product.query.filter(Product.id.in_(ids)).all()
    
    # Build comparison data
    comparison_data = []
    all_spec_keys = set()
    
    for product in products:
        specs = {spec.spec_key: spec.spec_value for spec in product.specifications}
        all_spec_keys.update(specs.keys())
        comparison_data.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand.name,
            'price': float(product.price),
            'specifications': specs
        })
    
    return render_template('user/compare.html',
                          products=comparison_data,
                          spec_keys=sorted(all_spec_keys))
```

### Analysis Route (2 Products with Pros/Cons)

**File:** [app/routes/user.py L116-156](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/routes/user.py#L116-156)

```python
@user_bp.route('/compare-analysis')
def compare_analysis():
    ids = [int(id) for id in product_ids.split(',')]
    products = Product.query.filter(Product.id.in_(ids)).all()
    
    # Get user preferences from session
    user_preferences = session.get('last_preferences', {})
    
    # Perform analysis
    comp_service = ComparisonService()
    analysis_data = comp_service.compare_two_products(
        products[0], products[1], user_preferences
    )
    
    return render_template('user/comparison_analysis.html', **analysis_data)
```

---

## 9. Frontend Templates

### Side-by-Side Comparison

**File:** [app/templates/user/compare.html](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/templates/user/compare.html)

- Displays 2-4 products in table format
- Shows all specifications with highlighting for differences
- Scrollable on mobile

### Pros/Cons Analysis

**File:** [app/templates/user/comparison_analysis.html](file:///e:/promgramming/Y3n/Expert%20System/Assignment/TechAdvisor/app/templates/user/comparison_analysis.html)

- Head-to-head product cards
- Pros (green) and Cons (red) lists
- Match score progress bars
- Category leaders section
- Expert verdict with winner reason
- Full spec comparison table

---

## 10. Data Flow Diagram

```
User clicks "Compare" with selected products
          │
          ▼
┌─────────────────────────────────────┐
│  GET /compare-analysis?ids=1,2      │
└─────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  Fetch products from database       │
│  + specifications relationship      │
└─────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  ComparisonService.compare_two()    │
│  ├─ extract_pros() for each         │
│  ├─ extract_cons() for each         │
│  ├─ get_comparative_advantages()    │
│  ├─ calculate_overall_score()       │
│  └─ determine winner                │
└─────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  Render comparison_analysis.html    │
│  with pros, cons, scores, winner    │
└─────────────────────────────────────┘
```

---

## 11. All Involved Files

| File | Purpose |
|------|---------|
| `app/models/product.py` | Product and Specification models |
| `app/services/comparison_service.py` | All comparison logic |
| `app/routes/user.py` | `/compare` and `/compare-analysis` routes |
| `app/templates/user/compare.html` | Side-by-side spec table |
| `app/templates/user/comparison_analysis.html` | Pros/cons analysis UI |

---

*Last updated: January 20, 2026*
