
import pytest
from app.services.comparison_service import ComparisonService
from app.models.product import Product, Brand, Category, Specification
from decimal import Decimal

class MockBrand:
    def __init__(self, name):
        self.name = name
        self.id = 1

class MockCategory:
    def __init__(self, name):
        self.name = name
        self.id = 1

class MockSpec:
    def __init__(self, key, value):
        self.spec_key = key
        self.spec_value = value

class MockProduct:
    def __init__(self, id, name, price, brand, category, specs):
        self.id = id
        self.name = name
        self.price = Decimal(price)
        self.brand = MockBrand(brand)
        self.brand_id = 1
        self.category = MockCategory(category)
        self.category_id = 1
        self.image_url = "http://example.com/image.jpg"
        self.description = "Test Description"
        self.specifications = [MockSpec(k, v) for k, v in specs.items()]

@pytest.fixture
def comparison_service():
    return ComparisonService()

@pytest.fixture
def products():
    product1 = MockProduct(
        id=1,
        name="High-End Phone",
        price=999.99,
        brand="BrandA",
        category="Smartphone",
        specs={
            "Processor": "Snapdragon 8 Gen 2",
            "RAM": "12GB",
            "Storage": "256GB",
            "Battery": "5000mAh",
            "Display": "6.8 inch OLED 120Hz",
            "Camera": "Main 108MP"
        }
    )
    
    product2 = MockProduct(
        id=2,
        name="Budget Phone",
        price=499.99,
        brand="BrandB",
        category="Smartphone",
        specs={
            "Processor": "Snapdragon 7",
            "RAM": "6GB",
            "Storage": "128GB",
            "Battery": "4500mAh",
            "Display": "6.5 inch LCD 60Hz",
            "Camera": "Main 48MP"
        }
    )
    
    return product1, product2

def test_extract_pros(comparison_service, products):
    p1, p2 = products
    user_prefs = {"budget": 1000.0, "preferred_brand": "BrandA"}
    
    pros1 = comparison_service.extract_pros(p1, user_prefs)
    assert any("Fits your budget" in p for p in pros1)
    assert any("Your preferred brand" in p for p in pros1)
    assert any("Excellent RAM" in p for p in pros1)
    assert any("Long-lasting battery" in p for p in pros1)
    assert any("Premium display" in p for p in pros1)
    
    pros2 = comparison_service.extract_pros(p2, user_prefs)
    assert any("Excellent value" in p for p in pros2)

def test_extract_cons(comparison_service, products):
    p1, p2 = products
    user_prefs = {"budget": 600.0}
    
    cons1 = comparison_service.extract_cons(p1, user_prefs)
    assert any("Over budget" in c for c in cons1)
    
    cons2 = comparison_service.extract_cons(p2, user_prefs)
    assert "Limited RAM: 6GB may struggle with multitasking" in cons2

def test_get_comparative_advantages(comparison_service, products):
    p1, p2 = products
    
    advantages = comparison_service.get_comparative_advantages(p1, p2)
    
    assert advantages['Price']['winner'] == 2  # Budget phone is cheaper
    assert advantages['RAM']['winner'] == 1    # High-end has more RAM
    assert advantages['Battery']['winner'] == 1 # High-end has bigger battery
    assert advantages['Processor']['winner'] == 1 # High-end has better CPU

def test_calculate_overall_score(comparison_service, products):
    p1, p2 = products
    user_prefs_high = {"budget": 1200.0, "usage_type": "Gaming"}
    
    score1 = comparison_service.calculate_overall_score(p1, user_prefs_high)
    score2 = comparison_service.calculate_overall_score(p2, user_prefs_high)
    
    # High-end phone should score higher for gaming and high budget
    assert score1 > score2
    
    user_prefs_budget = {"budget": 550.0}
    score1_budget = comparison_service.calculate_overall_score(p1, user_prefs_budget)
    score2_budget = comparison_service.calculate_overall_score(p2, user_prefs_budget)
    
    # Budget phone should score higher (or close) for strict budget due to penalty on high price
    # Actually p1 is way over budget, so it should be penalized heavily
    assert score2_budget > score1_budget

def test_compare_two_products_flow(comparison_service, products):
    p1, p2 = products
    user_prefs = {"budget": 1000.0}
    
    result = comparison_service.compare_two_products(p1, p2, user_prefs)
    
    assert 'product1' in result
    assert 'product2' in result
    assert 'winner' in result
    assert 'comparative_advantages' in result
    assert result['product1']['id'] == 1
    assert result['product2']['id'] == 2
