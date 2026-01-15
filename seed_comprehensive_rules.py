"""
Enhanced Rule Seeding Script
Creates 25+ comprehensive rules for TechAdvisor Expert System
Covers: Gaming, Study, Work, Creative, Photography, General use
"""
from app import create_app, db
from app.models.rule import Rule, RuleCondition
from app.models.product import Category


def clear_existing_rules():
    """Clear existing rules for clean seeding"""
    print("Clearing existing rules...")
    RuleCondition.query.delete()
    Rule.query.delete()
    db.session.commit()
    print("[OK] Existing rules cleared\n")


def create_rule_with_conditions(name, description, category_id, priority, conditions):
    """Helper to create a rule with its conditions"""
    rule = Rule(
        name=name,
        description=description,
        category_id=category_id,
        priority=priority,
        is_active=True
    )
    db.session.add(rule)
    db.session.flush()
    
    for cond in conditions:
        RuleCondition(
            rule_id=rule.id,
            condition_type=cond.get('type', 'user_input'),
            condition_key=cond['key'],
            operator=cond['operator'],
            condition_value=cond['value']
        ).save_to_db(db.session)
    
    return rule


def seed_enhanced_rules():
    """Create comprehensive rule set (25+ rules)"""
    app = create_app('development')
    
    with app.app_context():
        print("=" * 70)
        print("ENHANCED RULE SEEDING - 25+ COMPREHENSIVE RULES")
        print("=" * 70)
        
        # Get categories
        laptop_cat = Category.query.filter_by(name='Laptop').first()
        smartphone_cat = Category.query.filter_by(name='Smartphone').first()
        
        if not laptop_cat or not smartphone_cat:
            print("[X] Error: Categories not found")
            return
        
        # Optional: Clear existing rules
        # clear_existing_rules()
        
        rules_created = 0
        
        # ==================== SMARTPHONE RULES (12 rules) ====================
        print("\n📱 CREATING SMARTPHONE RULES...")
        print("-" * 70)
        
        # 1. Gaming Smartphone - High Budget
        if not Rule.query.filter_by(name='Gaming Smartphone - High Performance').first():
            create_rule_with_conditions(
                name='Gaming Smartphone - High Performance',
                description='High-end gaming phones with powerful processors',
                category_id=smartphone_cat.id,
                priority=90,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'gaming'},
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '800'}
                ]
            )
            print("  [OK] Gaming Smartphone - High Performance")
            rules_created += 1
        
        # 2. Gaming Smartphone - Mid Budget
        if not Rule.query.filter_by(name='Gaming Smartphone - Mid Range').first():
            create_rule_with_conditions(
                name='Gaming Smartphone - Mid Range',
                description='Balanced gaming phones for moderate budgets',
                category_id=smartphone_cat.id,
                priority=80,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'gaming'},
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '400'},
                    {'key': 'budget', 'operator': 'less_than', 'value': '800'}
                ]
            )
            print("  [OK] Gaming Smartphone - Mid Range")
            rules_created += 1
        
        #  3. Budget Smartphone - General Use
        if not Rule.query.filter_by(name='Budget Smartphone - Everyday').first():
            create_rule_with_conditions(
                name='Budget Smartphone - Everyday',
                description='Affordable smartphones for daily tasks',
                category_id=smartphone_cat.id,
                priority=60,
                conditions=[
                    {'key': 'budget', 'operator': 'less_than', 'value': '400'},
                    {'key': 'usage_type', 'operator': 'in', 'value': 'general,study'}
                ]
            )
            print("  [OK] Budget Smartphone - Everyday")
            rules_created += 1
        
        # 4. Photography Smartphone
        if not Rule.query.filter_by(name='Photography Smartphone - Camera Focus').first():
            create_rule_with_conditions(
                name='Photography Smartphone - Camera Focus',
                description='Smartphones optimized for photography',
                category_id=smartphone_cat.id,
                priority=85,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'creative'},
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '600'}
                ]
            )
            print("  [OK] Photography Smartphone - Camera Focus")
            rules_created += 1
        
        # 5. Premium Flagship Smartphone
        if not Rule.query.filter_by(name='Premium Flagship Smartphone').first():
            create_rule_with_conditions(
                name='Premium Flagship Smartphone',
                description='Top-tier flagship phones with all features',
                category_id=smartphone_cat.id,
                priority=95,
                conditions=[
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '1000'}
                ]
            )
            print("  [OK] Premium Flagship Smartphone")
            rules_created += 1
        
        # 6. Mid-Range All-Rounder Smartphone
        if not Rule.query.filter_by(name='Mid-Range All-Rounder Smartphone').first():
            create_rule_with_conditions(
                name='Mid-Range All-Rounder Smartphone',
                description='Balanced phones for versatile use',
                category_id=smartphone_cat.id,
                priority=70,
                conditions=[
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '500'},
                    {'key': 'budget', 'operator': 'less_than', 'value': '800'},
                    {'key': 'usage_type', 'operator': 'in', 'value': 'general,work'}
                ]
            )
            print("  [OK] Mid-Range All-Rounder Smartphone")
            rules_created += 1
        
        # 7. Work Smartphone - Professional
        if not Rule.query.filter_by(name='Work Smartphone - Professional').first():
            create_rule_with_conditions(
                name='Work Smartphone - Professional',
                description='Business-oriented smartphones',
                category_id=smartphone_cat.id,
                priority=75,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'work'},
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '600'}
                ]
            )
            print("  [OK] Work Smartphone - Professional")
            rules_created += 1
        
        # 8. Student Smartphone - Budget
        if not Rule.query.filter_by(name='Student Smartphone - Budget Friendly').first():
            create_rule_with_conditions(
                name='Student Smartphone - Budget Friendly',
                description='Affordable phones for students',
                category_id=smartphone_cat.id,
                priority=65,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'study'},
                    {'key': 'budget', 'operator': 'less_equal', 'value': '500'}
                ]
            )
            print("  [OK] Student Smartphone - Budget Friendly")
            rules_created += 1
        
        # 9. Content Creation Smartphone
        if not Rule.query.filter_by(name='Content Creation Smartphone').first():
            create_rule_with_conditions(
                name='Content Creation Smartphone',
                description='Smartphones for content creators (video, photos)',
                category_id=smartphone_cat.id,
                priority=85,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'creative'},
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '700'}
                ]
            )
            print("  [OK] Content Creation Smartphone")
            rules_created += 1
        
        # 10. Ultra-Budget Smartphone
        if not Rule.query.filter_by(name='Ultra-Budget Smartphone').first():
            create_rule_with_conditions(
                name='Ultra-Budget Smartphone',
                description='Most affordable smartphone options',
                category_id=smartphone_cat.id,
                priority=50,
                conditions=[
                    {'key': 'budget', 'operator': 'less_than', 'value': '250'}
                ]
            )
            print("  [OK] Ultra-Budget Smartphone")
            rules_created += 1
        
        # 11. 5G Smartphone - Future Ready
        if not Rule.query.filter_by(name='5G Smartphone - Future Ready').first():
            create_rule_with_conditions(
                name='5G Smartphone - Future Ready',
                description='5G-enabled smartphones for fast connectivity',
                category_id=smartphone_cat.id,
                priority=70,
                conditions=[
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '350'}
                ]
            )
            print("  [OK] 5G Smartphone - Future Ready")
            rules_created += 1
        
        # 12. General Purpose Smartphone
        if not Rule.query.filter_by(name='General Purpose Smartphone').first():
            create_rule_with_conditions(
                name='General Purpose Smartphone',
                description='All-purpose smartphones for everyday use',
                category_id=smartphone_cat.id,
                priority=55,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'general'}
                ]
            )
            print("  [OK] General Purpose Smartphone")
            rules_created += 1
        
        # ==================== LAPTOP RULES (13 rules) ====================
        print("\n💻 CREATING LAPTOP RULES...")
        print("-" * 70)
        
        # 13. Gaming Laptop - High Performance
        if not Rule.query.filter_by(name='Gaming Laptop - High Performance').first():
            create_rule_with_conditions(
                name='Gaming Laptop - High Performance',
                description='High-end gaming laptops with powerful GPUs',
                category_id=laptop_cat.id,
                priority=90,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'gaming'},
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '1200'}
                ]
            )
            print("  [OK] Gaming Laptop - High Performance")
            rules_created += 1
        
        # 14. Gaming Laptop - Entry Level
        if not Rule.query.filter_by(name='Gaming Laptop - Entry Level').first():
            create_rule_with_conditions(
                name='Gaming Laptop - Entry Level',
                description='Affordable gaming laptops for casual gamers',
                category_id=laptop_cat.id,
                priority=75,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'gaming'},
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '600'},
                    {'key': 'budget', 'operator': 'less_than', 'value': '1200'}
                ]
            )
            print("  [OK] Gaming Laptop - Entry Level")
            rules_created += 1
        
        # 15. Student Laptop - Budget
        if not Rule.query.filter_by(name='Student Laptop - Budget Friendly').first():
            create_rule_with_conditions(
                name='Student Laptop - Budget Friendly',
                description='Affordable laptops for students',
                category_id=laptop_cat.id,
                priority=70,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'study'},
                    {'key': 'budget', 'operator': 'less_equal', 'value': '700'}
                ]
            )
            print("  [OK] Student Laptop - Budget Friendly")
            rules_created += 1
        
        # 16. Student Laptop - Premium
        if not Rule.query.filter_by(name='Student Laptop - Premium').first():
            create_rule_with_conditions(
                name='Student Laptop - Premium',
                description='High-quality laptops for demanding students',
                category_id=laptop_cat.id,
                priority=80,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'study'},
                    {'key': 'budget', 'operator': 'greater_than', 'value': '700'}
                ]
            )
            print("  [OK] Student Laptop - Premium")
            rules_created += 1
        
        # 17. Professional Work Laptop
        if not Rule.query.filter_by(name='Professional Work Laptop').first():
            create_rule_with_conditions(
                name='Professional Work Laptop',
                description='Business laptops for professionals',
                category_id=laptop_cat.id,
                priority=85,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'work'},
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '800'}
                ]
            )
            print("  [OK] Professional Work Laptop")
            rules_created += 1
        
        # 18. Work Laptop - Budget
        if not Rule.query.filter_by(name='Work Laptop - Budget').first():
            create_rule_with_conditions(
                name='Work Laptop - Budget',
                description='Affordable business laptops',
                category_id=laptop_cat.id,
                priority=65,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'work'},
                    {'key': 'budget', 'operator': 'less_than', 'value': '800'}
                ]
            )
            print("  [OK] Work Laptop - Budget")
            rules_created += 1
        
        # 19. Content Creation Laptop
        if not Rule.query.filter_by(name='Content Creation Laptop').first():
            create_rule_with_conditions(
                name='Content Creation Laptop',
                description='Laptops for video editing, design, and creative work',
                category_id=laptop_cat.id,
                priority=90,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'creative'},
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '1000'}
                ]
            )
            print("  [OK] Content Creation Laptop")
            rules_created += 1
        
        # 20. General Purpose Laptop - Budget
        if not Rule.query.filter_by(name='General Purpose Laptop - Budget').first():
            create_rule_with_conditions(
                name='General Purpose Laptop - Budget',
                description='Affordable laptops for everyday tasks',
                category_id=laptop_cat.id,
                priority=60,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'general'},
                    {'key': 'budget', 'operator': 'less_equal', 'value': '600'}
                ]
            )
            print("  [OK] General Purpose Laptop - Budget")
            rules_created += 1
        
        # 21. General Purpose Laptop - Premium
        if not Rule.query.filter_by(name='General Purpose Laptop - Premium').first():
            create_rule_with_conditions(
                name='General Purpose Laptop - Premium',
                description='High-quality all-purpose laptops',
                category_id=laptop_cat.id,
                priority=75,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'general'},
                    {'key': 'budget', 'operator': 'greater_than', 'value': '600'}
                ]
            )
            print("  [OK] General Purpose Laptop - Premium")
            rules_created += 1
        
        # 22. Ultra-Portable Laptop
        if not Rule.query.filter_by(name='Ultra-Portable Laptop').first():
            create_rule_with_conditions(
                name='Ultra-Portable Laptop',
                description='Lightweight laptops for mobility',
                category_id=laptop_cat.id,
                priority=70,
                conditions=[
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '500'}
                ]
            )
            print("  [OK] Ultra-Portable Laptop")
            rules_created += 1
        
        # 23. Premium Flagship Laptop
        if not Rule.query.filter_by(name='Premium Flagship Laptop').first():
            create_rule_with_conditions(
                name='Premium Flagship Laptop',
                description='Top-tier laptops with best specs',
                category_id=laptop_cat.id,
                priority=95,
                conditions=[
                    {'key': 'budget', 'operator': 'greater_equal', 'value': '1500'}
                ]
            )
            print("  [OK] Premium Flagship Laptop")
            rules_created += 1
        
        # 24. Chromebook - Budget
        if not Rule.query.filter_by(name='Chromebook - Budget Friendly').first():
            create_rule_with_conditions(
                name='Chromebook - Budget Friendly',
                description='Affordable Chromebooks for basic tasks',
                category_id=laptop_cat.id,
                priority=55,
                conditions=[
                    {'key': 'budget', 'operator': 'less_than', 'value': '400'}
                ]
            )
            print("  [OK] Chromebook - Budget Friendly")
            rules_created += 1
        
        # 25. Creative Professional Laptop - Budget
        if not Rule.query.filter_by(name='Creative Laptop - Entry Level').first():
            create_rule_with_conditions(
                name='Creative Laptop - Entry Level',
                description='Entry-level laptops for creative work',
                category_id=laptop_cat.id,
                priority=70,
                conditions=[
                    {'key': 'usage_type', 'operator': 'equals', 'value': 'creative'},
                    {'key': 'budget', 'operator': 'less_than', 'value': '1000'}
                ]
            )
            print("  [OK] Creative Laptop - Entry Level")
            rules_created += 1
        
        db.session.commit()
        
        # Summary
        total_rules = Rule.query.count()
        active_rules = Rule.query.filter_by(is_active=True).count()
        smartphone_rules = Rule.query.filter_by(category_id=smartphone_cat.id).count()
        laptop_rules = Rule.query.filter_by(category_id=laptop_cat.id).count()
        
        print("\n" + "=" * 70)
        print("✅ ENHANCED RULE SEEDING COMPLETED!")
        print("=" * 70)
        print(f"New Rules Created: {rules_created}")
        print(f"Total Rules in DB: {total_rules}")
        print(f"Active Rules: {active_rules}")
        print(f"  - Smartphone Rules: {smartphone_rules}")
        print(f"  - Laptop Rules: {laptop_rules}")
        print("\n[OK] Proposal requirement (20-30 rules): {'MET [OK]' if total_rules >= 20 else 'NOT MET ✗'}")
        print(f"\nView rules at: http://127.0.0.1:5000/admin/rules")
        print("=" * 70)


# Helper method for RuleCondition
def save_to_db(self, session):
    session.add(self)

RuleCondition.save_to_db = save_to_db


if __name__ == '__main__':
    seed_enhanced_rules()
