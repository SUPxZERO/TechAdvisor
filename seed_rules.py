"""
Seed sample rules for testing the inference engine
Run with: python seed_rules.py
"""
from app import create_app, db
from app.models.rule import Rule, RuleCondition
from app.models.product import Category

def seed_sample_rules():
    """Create sample rules for testing recommendations"""
    app = create_app('development')
    
    with app.app_context():
        print("Starting rule seeding...")
        
        # Get categories
        laptop_cat = Category.query.filter_by(name='Laptop').first()
        smartphone_cat = Category.query.filter_by(name='Smartphone').first()
        
        if not laptop_cat or not smartphone_cat:
            print("Error: Categories not found")
            return
        
        print(f"\n{'='*60}")
        print("Creating Sample Rules...")
        print(f"{'='*60}")
        
        # Rule 1: Gaming Laptop Recommendation
        rule1 = Rule.query.filter_by(name='Gaming Laptop Recommendation').first()
        if not rule1:
            rule1 = Rule(
                name='Gaming Laptop Recommendation',
                description='Recommend high-performance laptops for gaming',
                category_id=laptop_cat.id,
                priority=85,
                is_active=True
            )
            db.session.add(rule1)
            db.session.flush()
            
            # Add conditions
            RuleCondition(
                rule_id=rule1.id,
                condition_type='user_input',
                condition_key='usage_type',
             operator='equals',
                condition_value='gaming'
            ).save_to_db(db.session)
            
            RuleCondition(
                rule_id=rule1.id,
                condition_type='user_input',
                condition_key='budget',
                operator='greater_equal',
                condition_value='1200'
            ).save_to_db(db.session)
            
            print(f"  ✓ Created: {rule1.name}")
        else:
            print(f"  ℹ Rule exists: {rule1.name}")
        
        # Rule 2: Budget Smartphone
        rule2 = Rule.query.filter_by(name='Budget Smartphone').first()
        if not rule2:
            rule2 = Rule(
                name='Budget Smartphone',
                description='Recommend affordable smartphones under $500',
                category_id=smartphone_cat.id,
                priority=60,
                is_active=True
            )
            db.session.add(rule2)
            db.session.flush()
            
            RuleCondition(
                rule_id=rule2.id,
                condition_type='user_input',
                condition_key='budget',
                operator='less_than',
                condition_value='500'
            ).save_to_db(db.session)
            
            RuleCondition(
                rule_id=rule2.id,
                condition_type='user_input',
                condition_key='category',
                operator='equals',
                condition_value='smartphone'
            ).save_to_db(db.session)
            
            print(f"  ✓ Created: {rule2.name}")
        else:
            print(f"  ℹ Rule exists: {rule2.name}")
        
        # Rule 3: Professional Laptop
        rule3 = Rule.query.filter_by(name='Professional Work Laptop').first()
        if not rule3:
            rule3 = Rule(
                name='Professional Work Laptop',
                description='Recommend business laptops for productivity',
                category_id=laptop_cat.id,
                priority=75,
                is_active=True
            )
            db.session.add(rule3)
            db.session.flush()
            
            RuleCondition(
                rule_id=rule3.id,
                condition_type='user_input',
                condition_key='usage_type',
                operator='equals',
                condition_value='work'
            ).save_to_db(db.session)
            
            RuleCondition(
                rule_id=rule3.id,
                condition_type='user_input',
                condition_key='budget',
                operator='greater_than',
                condition_value='1000'
            ).save_to_db(db.session)
            
            print(f"  ✓ Created: {rule3.name}")
        else:
            print(f"  ℹ Rule exists: {rule3.name}")
        
        # Rule 4: Premium Flagship Smartphone
        rule4 = Rule.query.filter_by(name='Premium Flagship Smartphone').first()
        if not rule4:
            rule4 = Rule(
                name='Premium Flagship Smartphone',
                description='Recommend high-end flagship smartphones',
                category_id=smartphone_cat.id,
                priority=80,
                is_active=True
            )
            db.session.add(rule4)
            db.session.flush()
            
            RuleCondition(
                rule_id=rule4.id,
                condition_type='user_input',
                condition_key='budget',
                operator='greater_equal',
                condition_value='1000'
            ).save_to_db(db.session)
            
            RuleCondition(
                rule_id=rule4.id,
                condition_type='user_input',
                condition_key='category',
                operator='equals',
                condition_value='smartphone'
            ).save_to_db(db.session)
            
            print(f"  ✓ Created: {rule4.name}")
        else:
            print(f"  ℹ Rule exists: {rule4.name}")
        
        # Rule 5: Student Laptop
        rule5 = Rule.query.filter_by(name='Student Budget Laptop').first()
        if not rule5:
            rule5 = Rule(
                name='Student Budget Laptop',
                description='Recommend affordable laptops for students',
                category_id=laptop_cat.id,
                priority=65,
                is_active=True
            )
            db.session.add(rule5)
            db.session.flush()
            
            RuleCondition(
                rule_id=rule5.id,
                condition_type='user_input',
                condition_key='usage_type',
                operator='equals',
                condition_value='study'
            ).save_to_db(db.session)
            
            RuleCondition(
                rule_id=rule5.id,
                condition_type='user_input',
                condition_key='budget',
                operator='less_equal',
                condition_value='800'
            ).save_to_db(db.session)
            
            print(f"  ✓ Created: {rule5.name}")
        else:
            print(f"  ℹ Rule exists: {rule5.name}")
        
        db.session.commit()
        
        total_rules = Rule.query.count()
        active_rules = Rule.query.filter_by(is_active=True).count()
        
        print(f"\n{'='*60}")
        print("✅ Rule seeding completed!")
        print(f"{'='*60}")
        print(f"Total Rules: {total_rules}")
        print(f"Active Rules: {active_rules}")
        print(f"\nView rules at: http://127.0.0.1:5001/admin/rules")


# Helper method for RuleCondition
def save_to_db(self, session):
    session.add(self)
    
RuleCondition.save_to_db = save_to_db


if __name__ == '__main__':
    seed_sample_rules()
