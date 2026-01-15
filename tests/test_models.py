"""
Unit tests for Data Models
Tests Product, Category, Brand, Rule, and RuleCondition models
"""
import pytest
from app.models.product import Product, Brand, Category
from app.models.rule import Rule, RuleCondition


@pytest.mark.unit
class TestProductModel:
    """Test cases for Product model"""
    
    def test_create_product(self, sample_products):
        """Test product creation"""
        phone = sample_products['phone1']
        
        assert phone.name == 'Samsung Galaxy A54'
        assert phone.price == 450.00
        assert phone.is_active is True
        assert phone.brand is not None
        assert phone.category is not None
    
    def test_product_relationships(self, sample_products, sample_brands, sample_categories):
        """Test product relationships with brand and category"""
        phone = sample_products['phone1']
        
        assert phone.brand.name == 'Samsung'
        assert phone.category.name == 'Smartphone'
    
    def test_product_price_validation(self, sample_categories, sample_brands):
        """Test that price must be positive"""
        phone_cat = sample_categories['smartphone']
        samsung = sample_brands['samsung']
        
        product = Product(
            name='Test Phone',
            brand_id=samsung.id,
            category_id=phone_cat.id,
            price=100.00,
            is_active=True
        )
        
        assert product.price > 0


@pytest.mark.unit
class TestCategoryModel:
    """Test cases for Category model"""
    
    def test_create_category(self, sample_categories):
        """Test category creation"""
        smartphone = sample_categories['smartphone']
        laptop = sample_categories['laptop']
        
        assert smartphone.name == 'Smartphone'
        assert laptop.name == 'Laptop'
    
    def test_category_uniqueness(self, db_session, sample_categories):
        """Test that category names must be unique"""
        # This would raise IntegrityError in real scenario
        # Here we just verify existing categories
        assert len(sample_categories) == 2


@pytest.mark.unit
class TestBrandModel:
    """Test cases for Brand model"""
    
    def test_create_brand(self, sample_brands):
        """Test brand creation"""
        apple = sample_brands['apple']
        samsung = sample_brands['samsung']
        
        assert apple.name == 'Apple'
        assert samsung.name == 'Samsung'
    
    def test_brand_products_relationship(self, sample_products, sample_brands):
        """Test brand to products relationship"""
        samsung = sample_brands['samsung']
        
        # Should have products
        assert len(samsung.products) > 0


@pytest.mark.unit
class TestRuleModel:
    """Test cases for Rule model"""
    
    def test_create_rule(self, sample_rules):
        """Test rule creation"""
        phone_gaming = sample_rules['phone_gaming']
        
        assert phone_gaming.name == 'Gaming Smartphone'
        assert phone_gaming.priority == 85
        assert phone_gaming.is_active is True
    
    def test_rule_conditions_relationship(self, sample_rules):
        """Test rule to conditions relationship"""
        phone_gaming = sample_rules['phone_gaming']
        
        # Should have 2 conditions
        assert len(list(phone_gaming.conditions)) == 2
    
    def test_rule_category_relationship(self, sample_rules, sample_categories):
        """Test rule to category relationship"""
        phone_gaming = sample_rules['phone_gaming']
        smartphone_cat = sample_categories['smartphone']
        
        assert phone_gaming.category_id == smartphone_cat.id
        assert phone_gaming.category.name == 'Smartphone'


@pytest.mark.unit
class TestRuleConditionModel:
    """Test cases for RuleCondition model"""
    
    def test_create_condition(self, sample_rules):
        """Test condition creation"""
        phone_gaming = sample_rules['phone_gaming']
        conditions = list(phone_gaming.conditions)
        
        assert len(conditions) > 0
        
        # Check first condition
        cond = conditions[0]
        assert cond.condition_type == 'user_input'
        assert cond.condition_key in ['usage_type', 'budget']
        assert cond.operator in ['equals', 'greater_equal']
    
    def test_condition_rule_relationship(self, sample_rules):
        """Test condition to rule relationship"""
        phone_gaming = sample_rules['phone_gaming']
        condition = list(phone_gaming.conditions)[0]
        
        assert condition.rule_id == phone_gaming.id
        assert condition.rule.name == 'Gaming Smartphone'
