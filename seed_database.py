"""
Database seeder script to populate initial data
Run with: python seed_database.py
"""
from app import create_app, db
from app.models.user import User
from app.models.product import Brand, Category

def seed_all():
    """Seed all initial data"""
    app = create_app('development')
    
    with app.app_context():
        print("Starting database seeding...")
        
        # Create default admin user
        print("\n1. Creating default admin user...")
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@techadvisor.local',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("   ✓ Admin user created (username: admin, password: admin123)")
        else:
            print("   ℹ Admin user already exists")
        
        # Create default categories
        print("\n2. Creating product categories...")
        categories_data = [
            {'name': 'Smartphone', 'description': 'Mobile smartphones for communication and entertainment'},
            {'name': 'Laptop', 'description': 'Portable computers for work and personal use'}
        ]
        
        for cat_data in categories_data:
            category = Category.query.filter_by(name=cat_data['name']).first()
            if not category:
                category = Category(**cat_data)
                db.session.add(category)
                print(f"   ✓ Category '{cat_data['name']}' created")
            else:
                print(f"   ℹ Category '{cat_data['name']}' already exists")
        
        # Create default brands
        print("\n3. Creating brands...")
        brands_data = [
            'Apple', 'Samsung', 'Dell', 'HP', 'Lenovo', 'ASUS', 
            'Xiaomi', 'OnePlus', 'Google', 'Microsoft', 'Acer', 'MSI'
        ]
        
        for brand_name in brands_data:
            brand = Brand.query.filter_by(name=brand_name).first()
            if not brand:
                brand = Brand(name=brand_name)
                db.session.add(brand)
                print(f"   ✓ Brand '{brand_name}' created")
            else:
                print(f"   ℹ Brand '{brand_name}' already exists")
        
        # Commit all changes
        db.session.commit()
        print("\n✅ Database seeding completed successfully!")
        print("\nYou can now login with:")
        print("   Username: admin")
        print("   Password: admin123")

if __name__ == '__main__':
    seed_all()
