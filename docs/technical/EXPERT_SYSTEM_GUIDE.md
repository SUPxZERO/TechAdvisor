# Expert System Guide

Technical documentation for the TechAdvisor rule-based expert system and inference engine.

---

## Overview

TechAdvisor uses a **forward-chaining inference engine** to generate product recommendations based on user preferences and predefined rules.

```
User Input → Working Memory → Rule Matching → Product Filtering → Recommendations
```

---

## Core Concepts

### 1. Working Memory

The working memory stores facts derived from user input during a single recommendation session.

**Example Facts:**
```python
{
    "category": "smartphone",
    "category_id": 1,
    "budget": 1000,
    "usage_type": "gaming",
    "preferred_brand": "Samsung"
}
```

### 2. Rules

Rules are IF-THEN statements stored in the database.

**Structure:**
- **Name**: Human-readable rule identifier
- **Priority**: 1-100 (higher = more important)
- **Category**: Target product category
- **Conditions**: List of conditions that must ALL be true

### 3. Rule Conditions

Each condition specifies an attribute, operator, and expected value.

**Example Rule:**
```
IF usage_type == "gaming" 
AND budget >= 1500
THEN recommend Laptop category (priority: 80)
```

---

## Inference Engine Algorithm

```python
def infer(user_inputs):
    # Step 1: Initialize working memory
    working_memory = {}
    for key, value in user_inputs.items():
        working_memory[key] = value
    
    # Step 2: Query relevant rules
    rules = get_active_rules(category_id=user_inputs.get('category_id'))
    
    # Step 3: Match rules against facts
    matched_rules = []
    for rule in rules:
        if all_conditions_satisfied(rule, working_memory):
            matched_rules.append(rule)
    
    # Step 4: Sort by priority
    return sorted(matched_rules, key=lambda r: r.priority, reverse=True)
```

---

## Supported Operators

| Operator | Alias | Description | Example |
|----------|-------|-------------|---------|
| `equals` | `==` | Exact match (case-insensitive) | `usage_type == "gaming"` |
| `not_equals` | `!=` | Not equal | `brand != "Apple"` |
| `less_than` | `<` | Numeric less than | `budget < 500` |
| `greater_than` | `>` | Numeric greater than | `budget > 1000` |
| `less_equal` | `<=` | Less than or equal | `budget <= 1500` |
| `greater_equal` | `>=` | Greater than or equal | `budget >= 800` |
| `in` | - | Value in comma-separated list | `usage_type in "gaming,creative"` |
| `contains` | - | Substring match | `notes contains "lightweight"` |

---

## Creating Effective Rules

### Rule Priority Guidelines

| Priority Range | Use Case |
|---------------|----------|
| 1-20 | Fallback/default recommendations |
| 21-50 | General category rules |
| 51-75 | Specific use case rules |
| 76-100 | High-priority specialty rules |

### Best Practices

1. **Start Broad**: Create general rules first, then add specific exceptions
2. **Avoid Conflicts**: Higher priority rules override lower ones
3. **Test Incrementally**: Add rules one at a time and verify behavior
4. **Use Descriptions**: Document WHY a rule exists

### Example Rule Set

```
Rule: Budget Laptop
Priority: 40
Category: Laptop
Conditions:
  - budget <= 800
  - category == "laptop"
Description: Entry-level laptops for budget-conscious users

---

Rule: Gaming Laptop High-End
Priority: 75
Category: Laptop  
Conditions:
  - usage_type == "gaming"
  - budget >= 1500
Description: Recommend gaming laptops with dedicated graphics

---

Rule: Professional Workstation
Priority: 70
Category: Laptop
Conditions:
  - usage_type == "work"
  - budget >= 1200
Description: Business laptops with reliability focus
```

---

## Recommendation Scoring

After rules are matched, products are filtered and scored.

### Confidence Score Calculation

```python
confidence = 50 + matched_rule.priority  # Base + rule priority
confidence = min(100, confidence)         # Cap at 100
```

### Product Filtering

1. **Active Only**: Only `is_active=True` products
2. **Category Match**: From matched rule categories
3. **Budget Filter**: `price <= user_budget`
4. **Brand Filter**: If specified, filter by brand
5. **Order**: By price ascending
6. **Limit**: Top N products (default: 10)

---

## Comparison Service

The comparison service provides detailed analysis between products.

### Scoring Weights

| Factor | Weight | Description |
|--------|--------|-------------|
| Budget Alignment | 25% | Optimal at 80% of budget |
| Specification Quality | 40% | RAM, storage, premium features |
| Brand Preference | 10% | Match to user preference |
| Usage Alignment | 15% | Feature match for use case |

### Benchmark Values

**Smartphones:**
| Spec | Excellent | Good | Minimum |
|------|-----------|------|---------|
| RAM | 12GB+ | 8GB+ | 6GB |
| Storage | 256GB+ | 128GB+ | 64GB |
| Battery | 5000mAh+ | 4000mAh+ | 3000mAh |

**Laptops:**
| Spec | Excellent | Good | Minimum |
|------|-----------|------|---------|
| RAM | 16GB+ | 8GB+ | 4GB |
| Storage | 512GB+ | 256GB+ | 128GB |
| Battery Life | 12h+ | 8h+ | 5h |

---

## Extending the Expert System

### Adding New Categories

1. Add category to `categories` table
2. Create rules for the new category
3. Add products with specifications
4. Update comparison benchmarks in `ComparisonService`

### Adding New Condition Types

1. Define the condition key (e.g., "screen_size")
2. Add to questionnaire form if user-facing
3. Create rules using the new condition
4. Update inference engine if special logic needed

### Custom Operators

To add a new operator, modify `InferenceEngine.evaluate_condition()`:

```python
elif operator == 'between':
    min_val, max_val = expected.split(',')
    return float(min_val) <= float(actual) <= float(max_val)
```

---

## Debugging Rules

### Enable SQL Logging

In `config.py`:
```python
SQLALCHEMY_ECHO = True
```

### Test Rule Matching

```python
from app.services.inference_engine import InferenceEngine

engine = InferenceEngine()
user_input = {
    'category': 'laptop',
    'category_id': 2,
    'budget': 1500,
    'usage_type': 'gaming'
}

matched = engine.infer(user_input)
for rule in matched:
    print(f"Matched: {rule.name} (priority: {rule.priority})")
```

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| No rules matched | Conditions too strict | Relax conditions or add fallback rules |
| Wrong products shown | Category mismatch | Verify category_id in rules |
| Low confidence scores | Low priority rules | Increase rule priorities |
