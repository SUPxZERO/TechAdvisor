"""
Test script to verify category filtering fix
"""
from app import create_app, db
from app.models.product import Product, Category
from app.services.recommendation_service import RecommendationService

# Create app context
app = create_app()
app.app_context().push()

# Get categories
smartphone_cat = Category.query.filter_by(name='Smartphone').first()
laptop_cat = Category.query.filter_by(name='Laptop').first()

print("=" * 60)
print("CATEGORY FILTER TEST")
print("=" * 60)

# Test 1: Request smartphones
print("\n[TEST 1] Requesting SMARTPHONES (Category ID:", smartphone_cat.id, ")")
print("-" * 60)

user_input_smartphone = {
    'category': 'smartphone',
    'category_id': smartphone_cat.id,
    'budget': 1000,
    'usage_type': 'gaming'
}

service = RecommendationService()
results = service.get_recommendations(user_input_smartphone, limit=10)

print(f"Total products found: {results['total_matches']}")
print(f"Fired rules: {results['fired_rules']}")
print("\nProducts returned:")
for product in results['products']:
    print(f"  - {product['name']} (Category: {product['category']}, Price: ${product['price']})")

# Verify all are smartphones
categories_found = set([p['category'] for p in results['products']])
if categories_found == {'Smartphone'} or len(categories_found) == 0:
    print("[PASS] Only smartphones returned (or no products)")
else:
    print("[FAIL] Other categories found:", categories_found)

# Test 2: Request laptops
print("\n\n[TEST 2] Requesting LAPTOPS (Category ID:", laptop_cat.id, ")")
print("-" * 60)

user_input_laptop = {
    'category': 'laptop',
    'category_id': laptop_cat.id,
    'budget': 1500,
    'usage_type': 'gaming'
}

results = service.get_recommendations(user_input_laptop, limit=10)

print(f"Total products found: {results['total_matches']}")
print(f"Fired rules: {results['fired_rules']}")
print("\nProducts returned:")
for product in results['products']:
    print(f"  - {product['name']} (Category: {product['category']}, Price: ${product['price']})")

# Verify all are laptops
categories_found = set([p['category'] for p in results['products']])
if categories_found == {'Laptop'} or len(categories_found) == 0:
    print("[PASS] Only laptops returned (or no products)")
else:
    print("[FAIL] Other categories found:", categories_found)

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
