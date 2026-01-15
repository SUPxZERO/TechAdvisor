"""
Test fixtures and configuration for pytest
"""
import pytest
from app import create_app, db
from app.models.user import User
from app.models.product import Product, Brand, Category, Specification
from app.models.rule import Rule, RuleCondition


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    """Create database session for testing"""
    with app.app_context():
        yield db.session
        db.session.rollback()


@pytest.fixture
def sample_categories(db_session):
    """Create sample categories"""
    smartphone = Category(name='Smartphone')
    laptop = Category(name='Laptop')
    
    db_session.add_all([smartphone, laptop])
    db_session.commit()
    
    return {'smartphone': smartphone, 'laptop': laptop}


@pytest.fixture
def sample_brands(db_session):
    """Create sample brands"""
    apple = Brand(name='Apple')
    samsung = Brand(name='Samsung')
    dell = Brand(name='Dell')
    hp = Brand(name='HP')
    
    db_session.add_all([apple, samsung, dell, hp])
    db_session.commit()
    
    return {'apple': apple, 'samsung': samsung, 'dell': dell, 'hp': hp}


@pytest.fixture
def sample_products(db_session, sample_categories, sample_brands):
    """Create sample products"""
    smartphone_cat = sample_categories['smartphone']
    laptop_cat = sample_categories['laptop']
    samsung = sample_brands['samsung']
    dell = sample_brands['dell']
    
    # Create smartphones
    phone1 = Product(
        name='Samsung Galaxy A54',
        brand_id=samsung.id,
        category_id=smartphone_cat.id,
        price=450.00,
        description='Mid-range smartphone',
        is_active=True
    )
    
    phone2 = Product(
        name='Samsung Galaxy S23',
        brand_id=samsung.id,
        category_id=smartphone_cat.id,
        price=899.99,
        description='Flagship smartphone',
        is_active=True
    )
    
    # Create laptops
    laptop1 = Product(
        name='Dell XPS 13',
        brand_id=dell.id,
        category_id=laptop_cat.id,
        price=1299.99,
        description='Premium ultrabook',
        is_active=True
    )
    
    laptop2 = Product(
        name='Dell Inspiron 15',
        brand_id=dell.id,
        category_id=laptop_cat.id,
        price=599.99,
        description='Budget laptop',
        is_active=True
    )
    
    db_session.add_all([phone1, phone2, laptop1, laptop2])
    db_session.commit()
    
    return {
        'phone1': phone1,
        'phone2': phone2,
        'laptop1': laptop1,
        'laptop2': laptop2
    }


@pytest.fixture
def sample_rules(db_session, sample_categories):
    """Create sample rules"""
    smartphone_cat = sample_categories['smartphone']
    laptop_cat = sample_categories['laptop']
    
    # Smartphone gaming rule
    phone_gaming = Rule(
        name='Gaming Smartphone',
        description='High-performance smartphones for gaming',
        category_id=smartphone_cat.id,
        priority=85,
        is_active=True
    )
    db_session.add(phone_gaming)
    db_session.commit()
    
    # Add conditions
    cond1 = RuleCondition(
        rule_id=phone_gaming.id,
        condition_type='user_input',
        condition_key='usage_type',
        operator='equals',
        condition_value='gaming'
    )
    cond2 = RuleCondition(
        rule_id=phone_gaming.id,
        condition_type='user_input',
        condition_key='budget',
        operator='greater_equal',
        condition_value='400'
    )
    
    # Laptop work rule
    laptop_work = Rule(
        name='Work Laptop',
        description='Professional laptops for business',
        category_id=laptop_cat.id,
        priority=75,
        is_active=True
    )
    db_session.add(laptop_work)
    db_session.commit()
    
    cond3 = RuleCondition(
        rule_id=laptop_work.id,
        condition_type='user_input',
        condition_key='usage_type',
        operator='equals',
        condition_value='work'
    )
    
    db_session.add_all([cond1, cond2, cond3])
    db_session.commit()
    
    return {'phone_gaming': phone_gaming, 'laptop_work': laptop_work}


@pytest.fixture
def admin_user(db_session):
    """Create admin user for testing"""
    user = User(
        email='admin@test.com',
        username='admin',
        role='admin',
        is_active=True
    )
    user.set_password('admin123')
    
    db_session.add(user)
    db_session.commit()
    
    return user


@pytest.fixture
def authenticated_client(client, admin_user):
    """Create authenticated client"""
    client.post('/auth/login', data={
        'email': 'admin@test.com',
        'password': 'admin123'
    }, follow_redirects=True)
    
    return client
