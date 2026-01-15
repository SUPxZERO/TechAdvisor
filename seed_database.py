"""
Database seeder script to populate initial data
Run with: python seed_database.py
"""
from app import create_app, db
from app.models.user import User
from app.models.role import Role
from app.models.product import Brand, Category, Product, Specification
from werkzeug.security import generate_password_hash
import random

def seed_all():
    """Seed all initial data"""
    app = create_app('development')
    
    with app.app_context():
        print("Starting database seeding...")
        
        # 0. Ensure Roles Exist (Dependencies)
        admin_role = Role.query.filter_by(name='Admin').first()
        staff_role = Role.query.filter_by(name='Staff').first()
        if not admin_role or not staff_role:
            print("❌ Roles missing! Please run init_rbac.py first.")
            return

        # 1. Create Users
        print("\n1. Creating users...")
        # Admin
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@techadvisor.local', role='admin', role_obj=admin_role, is_active=True)
            admin.set_password('admin123')
            db.session.add(admin)
            print("   ✓ Admin user created")
        else:
            # Ensure RBAC role is linked
            if not admin.role_obj:
                admin.role_obj = admin_role
                db.session.add(admin)
                print("   ✓ Admin user updated with RBAC role")
            print("   ℹ Admin user exists")

        # Staff
        staff = User.query.filter_by(username='staff').first()
        if not staff:
            staff = User(username='staff', email='staff@techadvisor.local', role='staff', role_obj=staff_role, is_active=True)
            staff.set_password('staff123')
            db.session.add(staff)
            print("   ✓ Staff user created (username: staff, password: staff123)")
        else:
            if not staff.role_obj:
                staff.role_obj = staff_role
                db.session.add(staff)
                print("   ✓ Staff user updated with RBAC role")
            print("   ℹ Staff user exists")
        
        # 2. Create Categories
        print("\n2. Creating categories...")
        categories_data = [
            {'name': 'Smartphone', 'description': 'Mobile smartphones for communication and entertainment'},
            {'name': 'Laptop', 'description': 'Portable computers for work and personal use'}
        ]
        cats = {}
        for cat_data in categories_data:
            category = Category.query.filter_by(name=cat_data['name']).first()
            if not category:
                category = Category(**cat_data)
                db.session.add(category)
                print(f"   ✓ Category '{cat_data['name']}' created")
            cats[cat_data['name']] = category
        db.session.commit() # Commit to get IDs

        # 3. Create Brands
        print("\n3. Creating brands...")
        brands_data = [
            'Apple', 'Samsung', 'Dell', 'HP', 'Lenovo', 'ASUS', 
            'Xiaomi', 'Google', 'Microsoft', 'Acer', 'MSI', 'Sony'
        ]
        brands = {}
        for brand_name in brands_data:
            brand = Brand.query.filter_by(name=brand_name).first()
            if not brand:
                brand = Brand(name=brand_name, logo_url=None)
                db.session.add(brand)
                print(f"   ✓ Brand '{brand_name}' created")
            brands[brand_name] = brand
        db.session.commit() # Commit to get IDs

        # 4. Create Products
        print("\n4. Creating products...")
        
        # Helper to get brand object
        def get_brand(name):
            return brands.get(name) or Brand.query.filter_by(name=name).first()

        products_data = [
            # Laptops
            {
                'name': 'MacBook Pro 16 M3', 'brand': 'Apple', 'category': 'Laptop', 'price': 2499.00,
                'description': 'The most powerful MacBook Pro ever enabled by M3 Max chips.',
                'specs': {'CPU': 'M3 Max', 'RAM': '36GB', 'Storage': '1TB SSD', 'Screen': '16.2 Liquid Retina XDR', 'Battery': '22 hours'}
            },
            {
                'name': 'Dell XPS 15', 'brand': 'Dell', 'category': 'Laptop', 'price': 1899.00,
                'description': 'High performance 15-inch laptop with InfinityEdge display.',
                'specs': {'CPU': 'Intel Core i9', 'RAM': '32GB', 'Storage': '1TB NVMe', 'Screen': '15.6 4K OLED', 'Battery': '10 hours'}
            },
            {
                'name': 'HP Spectre x360', 'brand': 'HP', 'category': 'Laptop', 'price': 1599.00,
                'description': 'Convertible 2-in-1 laptop with stunning design.',
                'specs': {'CPU': 'Intel Core i7', 'RAM': '16GB', 'Storage': '512GB SSD', 'Screen': '14 3K2K OLED', 'Battery': '13 hours'}
            },
            {
                'name': 'Lenovo ThinkPad X1 Carbon', 'brand': 'Lenovo', 'category': 'Laptop', 'price': 1799.00,
                'description': 'Ultralight business laptop with legendary durability.',
                'specs': {'CPU': 'Intel Core i7', 'RAM': '16GB', 'Storage': '1TB SSD', 'Screen': '14 WUXGA', 'Battery': '15 hours'}
            },
            {
                'name': 'ASUS ROG Zephyrus G14', 'brand': 'ASUS', 'category': 'Laptop', 'price': 1499.00,
                'description': 'Powerful gaming laptop in a compact form factor.',
                'specs': {'CPU': 'AMD Ryzen 9', 'RAM': '16GB', 'Storage': '1TB SSD', 'Screen': '14 120Hz IPS', 'Battery': '10 hours'}
            },

            # Smartphones
            {
                'name': 'iPhone 15 Pro Max', 'brand': 'Apple', 'category': 'Smartphone', 'price': 1199.00,
                'description': 'The first iPhone with an aerospace-grade titanium design.',
                'specs': {'Processor': 'A17 Pro', 'RAM': '8GB', 'Storage': '256GB', 'Screen': '6.7 Super Retina XDR', 'Battery': '4422 mAh'}
            },
            {
                'name': 'Samsung Galaxy S24 Ultra', 'brand': 'Samsung', 'category': 'Smartphone', 'price': 1299.00,
                'description': 'Epic Galaxy AI features and titanium frame.',
                'specs': {'Processor': 'Snapdragon 8 Gen 3', 'RAM': '12GB', 'Storage': '512GB', 'Screen': '6.8 QHD+ AMOLED', 'Battery': '5000 mAh'}
            },
            {
                'name': 'Google Pixel 8 Pro', 'brand': 'Google', 'category': 'Smartphone', 'price': 999.00,
                'description': 'Google designed phone with the best camera and helpful AI.',
                'specs': {'Processor': 'Tensor G3', 'RAM': '12GB', 'Storage': '128GB', 'Screen': '6.7 LTPO OLED', 'Battery': '5050 mAh'}
            },
            {
                'name': 'Xiaomi 14 Ultra', 'brand': 'Xiaomi', 'category': 'Smartphone', 'price': 1099.00,
                'description': 'Professional photography kit in a smartphone.',
                'specs': {'Processor': 'Snapdragon 8 Gen 3', 'RAM': '16GB', 'Storage': '512GB', 'Screen': '6.73 AMOLED', 'Battery': '5000 mAh'}
            }
        ]

        for p_data in products_data:
            # Check if product exists
            existing_product = Product.query.filter_by(name=p_data['name']).first()
            if not existing_product:
                brand_obj = get_brand(p_data['brand'])
                cat_obj = cats.get(p_data['category']) or Category.query.filter_by(name=p_data['category']).first()
                
                if brand_obj and cat_obj:
                    product = Product(
                        name=p_data['name'],
                        brand=brand_obj,
                        category=cat_obj,
                        price=p_data['price'],
                        description=p_data['description'],
                        is_active=True
                    )
                    db.session.add(product)
                    db.session.flush() # Get ID
                    
                    # Add specs
                    for k, v in p_data['specs'].items():
                        spec = Specification(product_id=product.id, spec_key=k, spec_value=v)
                        db.session.add(spec)
                        
                    print(f"   ✓ Product '{p_data['name']}' created")
                else:
                    print(f"   ⚠️ Skipping {p_data['name']}: Brand or Category not found")
            else:
                print(f"   ℹ Product '{p_data['name']}' already exists")
        
        db.session.commit()
        print("\n✅ Database seeding completed successfully!")
        print("\nLogin Credentials:")
        print("   Admin: admin / admin123")
        print("   Staff: staff / staff123")

if __name__ == '__main__':
    seed_all()
