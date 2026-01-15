"""
Seed database with sample products
Run with: python seed_products.py
"""
from app import create_app, db
from app.models.product import Brand, Category, Product, Specification
from decimal import Decimal

def seed_products():
    """Seed sample products with specifications"""
    app = create_app('development')
    
    with app.app_context():
        print("Starting product seeding...")
        
        # Get categories
        smartphone_cat = Category.query.filter_by(name='Smartphone').first()
        laptop_cat = Category.query.filter_by(name='Laptop').first()
        
        if not smartphone_cat or not laptop_cat:
            print("Error: Categories not found. Run seed_database.py first.")
            return
        
        # Get brands
        brands = {brand.name: brand for brand in Brand.query.all()}
        
        # Smartphones data
        smartphones = [
            {
                'name': 'iPhone 15 Pro Max 256GB',
                'brand': 'Apple',
                'price': Decimal('1199.99'),
                'description': 'Premium flagship with titanium design and A17 Pro chip',
                'image_url': 'https://i5.walmartimages.com/seo/Restored-Apple-iPhone-15-Pro-Max-256GB-AT-T-Blue-Titanium-MU693LL-A-Excellent-Condition_dd2d42c6-cc25-4bee-81ef-7847120498d5.663475b807d168a41e9082d258d9c7ce.jpeg',
                'specs': {
                    'Processor': 'A17 Pro Chip',
                    'RAM': '8GB',
                    'Storage': '256GB',
                    'Display': '6.7" Super Retina XDR',
                    'Camera': '48MP Main + 12MP Ultra Wide',
                    'Battery': '4422mAh',
                    'OS': 'iOS 17'
                }
            },
            {
                'name': 'iPhone 14 128GB',
                'brand': 'Apple',
                'price': Decimal('799.99'),
                'description': 'Reliable daily driver with excellent camera',
                'image_url': 'https://m.media-amazon.com/images/I/51twnyEBC8L.jpg',
                'specs': {
                    'Processor': 'A15 Bionic',
                    'RAM': '6GB',
                    'Storage': '128GB',
                    'Display': '6.1" Super Retina XDR',
                    'Camera': '12MP Dual Camera',
                    'Battery': '3279mAh',
                    'OS': 'iOS 17'
                }
            },
            {
                'name': 'Samsung Galaxy S24 Ultra 512GB',
                'brand': 'Samsung',
                'price': Decimal('1399.99'),
                'description': 'Ultimate productivity powerhouse with S Pen',
                'image_url': 'https://angkormeas.com/wp-content/uploads/2022/05/S24-Ultrra_Global_v5.jpg?v=1721791628',
                'specs': {
                    'Processor': 'Snapdragon 8 Gen 3',
                    'RAM': '12GB',
                    'Storage': '512GB',
                    'Display': '6.8" Dynamic AMOLED 2X',
                    'Camera': '200MP Main + 50MP Telephoto',
                    'Battery': '5000mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'Samsung Galaxy A54 5G 128GB',
                'brand': 'Samsung',
                'price': Decimal('449.99'),
                'description': 'Mid-range champion with great value',
                'image_url': 'https://via.placeholder.com/200x200?text=Galaxy+A54',
                'specs': {
                    'Processor': 'Exynos 1380',
                    'RAM': '8GB',
                    'Storage': '128GB',
                    'Display': '6.4" Super AMOLED',
                    'Camera': '50MP Triple Camera',
                    'Battery': '5000mAh',
                    'OS': 'Android 13'
                }
            },
            {
                'name': 'Google Pixel 8 Pro 256GB',
                'brand': 'Google',
                'price': Decimal('999.99'),
                'description': 'AI-powered photography with pure Android',
                'image_url': 'https://via.placeholder.com/200x200?text=Pixel+8+Pro',
                'specs': {
                    'Processor': 'Google Tensor G3',
                    'RAM': '12GB',
                    'Storage': '256GB',
                    'Display': '6.7" LTPO OLED',
                    'Camera': '50MP + 48MP Telephoto',
                    'Battery': '5050mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'Xiaomi 13T Pro 512GB',
                'brand': 'Xiaomi',
                'price': Decimal('649.99'),
                'description': 'Flagship killer with Leica optics',
                'image_url': 'https://via.placeholder.com/200x200?text=Xiaomi+13T+Pro',
                'specs': {
                    'Processor': 'MediaTek Dimensity 9200+',
                    'RAM': '12GB',
                    'Storage': '512GB',
                    'Display': '6.67" AMOLED',
                    'Camera': '50MP Leica Triple Camera',
                    'Battery': '5000mAh',
                    'OS': 'Android 13'
                }
            },
            {
                'name': 'OnePlus 11 256GB',
                'brand': 'OnePlus',
                'price': Decimal('699.99'),
                'description': 'Speed and performance at great value',
                'image_url': 'https://via.placeholder.com/200x200?text=OnePlus+11',
                'specs': {
                    'Processor': 'Snapdragon 8 Gen 2',
                    'RAM': '16GB',
                    'Storage': '256GB',
                    'Display': '6.7" AMOLED 120Hz',
                    'Camera': '50MP Hasselblad Triple',
                    'Battery': '5000mAh',
                    'OS': 'Android 13'
                }
            },
        ]
        
        # Laptops data
        laptops = [
            {
                'name': 'MacBook Pro 16" M3 Pro 512GB',
                'brand': 'Apple',
                'price': Decimal('2499.99'),
                'description': 'Professional powerhouse for creators',
                'image_url': 'https://via.placeholder.com/200x200?text=MacBook+Pro+16',
                'specs': {
                    'Processor': 'Apple M3 Pro',
                    'RAM': '18GB Unified Memory',
                    'Storage': '512GB SSD',
                    'Display': '16.2" Liquid Retina XDR',
                    'Graphics': 'Integrated 18-core GPU',
                    'Battery': 'Up to 22 hours',
                    'Weight': '2.15 kg'
                }
            },
            {
                'name': 'MacBook Air 13" M2 256GB',
                'brand': 'Apple',
                'price': Decimal('1199.99'),
                'description': 'Ultra-portable for everyday tasks',
                'image_url': 'https://via.placeholder.com/200x200?text=MacBook+Air',
                'specs': {
                    'Processor': 'Apple M2',
                    'RAM': '8GB Unified Memory',
                    'Storage': '256GB SSD',
                    'Display': '13.6" Liquid Retina',
                    'Graphics': 'Integrated 8-core GPU',
                    'Battery': 'Up to 18 hours',
                    'Weight': '1.24 kg'
                }
            },
            {
                'name': 'Dell XPS 15 9530 RTX 4060',
                'brand': 'Dell',
                'price': Decimal('2199.99'),
                'description': 'Premium Windows laptop for professionals',
                'image_url': 'https://via.placeholder.com/200x200?text=Dell+XPS+15',
                'specs': {
                    'Processor': 'Intel Core i7-13700H',
                    'RAM': '16GB DDR5',
                    'Storage': '512GB NVMe SSD',
                    'Display': '15.6" OLED 3.5K',
                    'Graphics': 'NVIDIA RTX 4060 8GB',
                    'Battery': '86Whr',
                    'Weight': '1.86 kg'
                }
            },
            {
                'name': 'HP Pavilion 15 Ryzen 5',
                'brand': 'HP',
                'price': Decimal('649.99'),
                'description': 'Affordable everyday laptop',
                'image_url': 'https://via.placeholder.com/200x200?text=HP+Pavilion',
                'specs': {
                    'Processor': 'AMD Ryzen 5 5500U',
                    'RAM': '8GB DDR4',
                    'Storage': '512GB SSD',
                    'Display': '15.6" FHD IPS',
                    'Graphics': 'AMD Radeon Graphics',
                    'Battery': '41Whr',
                    'Weight': '1.75 kg'
                }
            },
            {
                'name': 'Lenovo ThinkPad X1 Carbon Gen 11',
                'brand': 'Lenovo',
                'price': Decimal('1899.99'),
                'description': 'Business ultrabook with durability',
                'image_url': 'https://via.placeholder.com/200x200?text=ThinkPad+X1',
                'specs': {
                    'Processor': 'Intel Core i7-1365U',
                    'RAM': '16GB LPDDR5',
                    'Storage': '512GB SSD',
                    'Display': '14" WUXGA IPS',
                    'Graphics': 'Intel Iris Xe',
                    'Battery': '57Whr',
                    'Weight': '1.12 kg'
                }
            },
            {
                'name': 'ASUS ROG Zephyrus G14 RTX 4060',
                'brand': 'ASUS',
                'price': Decimal('1599.99'),
                'description': 'Compact gaming powerhouse',
                'image_url': 'https://via.placeholder.com/200x200?text=ROG+Zephyrus',
                'specs': {
                    'Processor': 'AMD Ryzen 9 7940HS',
                    'RAM': '16GB DDR5',
                    'Storage': '1TB NVMe SSD',
                    'Display': '14" QHD+ 165Hz',
                    'Graphics': 'NVIDIA RTX 4060 8GB',
                    'Battery': '76Whr',
                    'Weight': '1.65 kg'
                }
            },
            {
                'name': 'MSI Creator Z16P RTX 4070',
                'brand': 'MSI',
                'price': Decimal('2299.99'),
                'description': 'Content creation workstation',
                'image_url': 'https://via.placeholder.com/200x200?text=MSI+Creator',
                'specs': {
                    'Processor': 'Intel Core i9-13900H',
                    'RAM': '32GB DDR5',
                    'Storage': '1TB NVMe SSD',
                    'Display': '16" QHD+ 165Hz',
                    'Graphics': 'NVIDIA RTX 4070 8GB',
                    'Battery': '90Whr',
                    'Weight': '2.39 kg'
                }
            },
            {
                'name': 'Acer Swift 3 Intel i5',
                'brand': 'Acer',
                'price': Decimal('599.99'),
                'description': 'Budget-friendly productivity laptop',
                'image_url': 'https://via.placeholder.com/200x200?text=Acer+Swift+3',
                'specs': {
                    'Processor': 'Intel Core i5-1235U',
                    'RAM': '8GB LPDDR4X',
                    'Storage': '512GB SSD',
                    'Display': '14" FHD IPS',
                    'Graphics': 'Intel Iris Xe',
                    'Battery': '56Whr',
                    'Weight': '1.25 kg'
                }
            },
        ]
        
        # Add smartphones
        print(f"\n{'='*50}")
        print("Adding Smartphones...")
        print(f"{'='*50}")
        for phone_data in smartphones:
            brand = brands.get(phone_data['brand'])
            if not brand:
                print(f"  ⚠ Brand '{phone_data['brand']}' not found, skipping {phone_data['name']}")
                continue
            
            existing = Product.query.filter_by(name=phone_data['name']).first()
            if existing:
                print(f"  ℹ {phone_data['name']} already exists")
                continue
            
            product = Product(
                name=phone_data['name'],
                brand_id=brand.id,
                category_id=smartphone_cat.id,
                price=phone_data['price'],
                description=phone_data['description'],
                image_url=phone_data['image_url'],
                is_active=True
            )
            db.session.add(product)
            db.session.flush()
            
            # Add specifications
            for spec_key, spec_value in phone_data['specs'].items():
                spec = Specification(
                    product_id=product.id,
                    spec_key=spec_key,
                    spec_value=spec_value
                )
                db.session.add(spec)
            
            print(f"  ✓ Added: {phone_data['name']} - ${phone_data['price']}")
        
        # Add laptops
        print(f"\n{'='*50}")
        print("Adding Laptops...")
        print(f"{'='*50}")
        for laptop_data in laptops:
            brand = brands.get(laptop_data['brand'])
            if not brand:
                print(f"  ⚠ Brand '{laptop_data['brand']}' not found, skipping {laptop_data['name']}")
                continue
            
            existing = Product.query.filter_by(name=laptop_data['name']).first()
            if existing:
                print(f"  ℹ {laptop_data['name']} already exists")
                continue
            
            product = Product(
                name=laptop_data['name'],
                brand_id=brand.id,
                category_id=laptop_cat.id,
                price=laptop_data['price'],
                description=laptop_data['description'],
                image_url=laptop_data['image_url'],
                is_active=True
            )
            db.session.add(product)
            db.session.flush()
            
            # Add specifications
            for spec_key, spec_value in laptop_data['specs'].items():
                spec = Specification(
                    product_id=product.id,
                    spec_key=spec_key,
                    spec_value=spec_value
                )
                db.session.add(spec)
            
            print(f"  ✓ Added: {laptop_data['name']} - ${laptop_data['price']}")
        
        # Commit all changes
        db.session.commit()
        
        # Display summary
        total_products = Product.query.count()
        total_smartphones = Product.query.filter_by(category_id=smartphone_cat.id).count()
        total_laptops = Product.query.filter_by(category_id=laptop_cat.id).count()
        
        print(f"\n{'='*50}")
        print("✅ Product seeding completed!")
        print(f"{'='*50}")
        print(f"Total Products: {total_products}")
        print(f"  - Smartphones: {total_smartphones}")
        print(f"  - Laptops: {total_laptops}")
        print(f"\nView products at: http://127.0.0.1:5001/admin/products")

if __name__ == '__main__':
    seed_products()
