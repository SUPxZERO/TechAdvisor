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
                'name': 'Samsung Galaxy S24 256GB',
                'brand': 'Samsung',
                'price': Decimal('999.99'),
                'description': 'Compact flagship with AI-powered features',
                'image_url': 'https://images.unsplash.com/photo-1706372073521-9e9d1b3e2d9c?w=400',
                'specs': {
                    'Processor': 'Exynos 2400 / Snapdragon 8 Gen 3',
                    'RAM': '8GB',
                    'Storage': '256GB',
                    'Display': '6.2" Dynamic AMOLED 2X 120Hz',
                    'Camera': '50MP Triple Camera',
                    'Battery': '4000mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'iPhone 15 128GB',
                'brand': 'Apple',
                'price': Decimal('799.99'),
                'description': 'Latest iPhone with USB-C and A16 performance',
                'image_url': 'https://images.unsplash.com/photo-1695048133142-1a20484d256c?w=400',
                'specs': {
                    'Processor': 'A16 Bionic',
                    'RAM': '6GB',
                    'Storage': '128GB',
                    'Display': '6.1" Super Retina XDR',
                    'Camera': '48MP Dual Camera',
                    'Battery': '3349mAh',
                    'OS': 'iOS 17'
                }
            },
            {
                'name': 'Google Pixel 8 128GB',
                'brand': 'Google',
                'price': Decimal('699.99'),
                'description': 'Smart AI phone with long software support',
                'image_url': 'https://images.unsplash.com/photo-1696180374313-bf6713d7cbcf?w=400',
                'specs': {
                    'Processor': 'Google Tensor G3',
                    'RAM': '8GB',
                    'Storage': '128GB',
                    'Display': '6.2" OLED 120Hz',
                    'Camera': '50MP + 12MP',
                    'Battery': '4575mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'Xiaomi Redmi Note 13 Pro+ 5G',
                'brand': 'Xiaomi',
                'price': Decimal('399.99'),
                'description': 'Best value mid-range phone with 200MP camera',
                'image_url': 'https://m.media-amazon.com/images/I/71d7rfSl0wL.jpg',
                'specs': {
                    'Processor': 'MediaTek Dimensity 7200 Ultra',
                    'RAM': '12GB',
                    'Storage': '256GB',
                    'Display': '6.67" AMOLED 120Hz',
                    'Camera': '200MP Triple Camera',
                    'Battery': '5000mAh',
                    'OS': 'Android 13'
                }
            },
                        {
                'name': 'Samsung Galaxy S25 Ultra 512GB',
                'brand': 'Samsung',
                'price': Decimal('1299.99'),
                'description': 'Top tier flagship with Snapdragon 8 Gen 4 and pro-grade camera',
                'image_url': 'https://via.placeholder.com/200x200?text=Galaxy+S25+Ultra',
                'specs': {
                    'Processor': 'Snapdragon 8 Gen 4',
                    'RAM': '12GB',
                    'Storage': '512GB',
                    'Display': '6.9" AMOLED 2X 144Hz',
                    'Camera': '200MP Quad Camera',
                    'Battery': '5500mAh',
                    'OS': 'Android 15'
                }
            },
            {
                'name': 'iPhone 17 Pro 256GB',
                'brand': 'Apple',
                'price': Decimal('1199.99'),
                'description': 'Apple’s latest flagship with A19 Pro chip and advanced cameras',
                'image_url': 'https://via.placeholder.com/200x200?text=iPhone+17+Pro',
                'specs': {
                    'Processor': 'A19 Pro Bionic',
                    'RAM': '8GB',
                    'Storage': '256GB',
                    'Display': '6.3" OLED 120Hz',
                    'Camera': 'Triple 48MP',
                    'Battery': '4500mAh',
                    'OS': 'iOS 18'
                }
            },
            {
                'name': 'Google Pixel 9 Pro 256GB',
                'brand': 'Google',
                'price': Decimal('999.99'),
                'description': 'AI-centric camera flagship with Tensor G4 chip',
                'image_url': 'https://via.placeholder.com/200x200?text=Pixel+9+Pro',
                'specs': {
                    'Processor': 'Google Tensor G4',
                    'RAM': '12GB',
                    'Storage': '256GB',
                    'Display': '6.7" LTPO OLED',
                    'Camera': 'Triple Camera',
                    'Battery': '4700mAh',
                    'OS': 'Android 15'
                }
            },
            {
                'name': 'OnePlus 13s 256GB',
                'brand': 'OnePlus',
                'price': Decimal('649.99'),
                'description': 'Compact flagship-level performance with Snapdragon 8 Elite', 
                'image_url': 'https://via.placeholder.com/200x200?text=OnePlus+13s',
                'specs': {
                    'Processor': 'Snapdragon 8 Elite',
                    'RAM': '12GB',
                    'Storage': '256GB',
                    'Display': '6.32" AMOLED',
                    'Camera': '50MP + Ultrawide',
                    'Battery': '6260mAh',
                    'OS': 'Android 15'
                }
            },
            {
                'name': 'Samsung Galaxy A56 5G 128GB',
                'brand': 'Samsung',
                'price': Decimal('499.99'),
                'description': '2025 mid-range phone with AMOLED display and solid battery life',
                'image_url': 'https://via.placeholder.com/200x200?text=Galaxy+A56',
                'specs': {
                    'Processor': 'Exynos 1580',
                    'RAM': '8GB',
                    'Storage': '128GB',
                    'Display': '6.7" Super AMOLED 120Hz',
                    'Camera': '50MP + 12MP + 5MP',
                    'Battery': '5000mAh',
                    'OS': 'Android 16'
                }
            },
            {
                'name': 'Motorola Razr 50 Fold 256GB',
                'brand': 'Motorola',
                'price': Decimal('1099.99'),
                'description': 'Modern foldable with large inner display and clamshell design',
                'image_url': 'https://via.placeholder.com/200x200?text=Motorola+Razr+50',
                'specs': {
                    'Processor': 'Dimensity 7300X',
                    'RAM': '12GB',
                    'Storage': '256GB',
                    'Display': '8.0" Foldable + 6.9" Cover',
                    'Camera': '50MP + 13MP',
                    'Battery': '4200mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'iQOO Z10 128GB',
                'brand': 'iQOO',
                'price': Decimal('399.99'),
                'description': 'Massive battery phone with big display and smooth performance',
                'image_url': 'https://via.placeholder.com/200x200?text=iQOO+Z10',
                'specs': {
                    'Processor': 'Snapdragon 7s Gen 3',
                    'RAM': '8GB',
                    'Storage': '128GB',
                    'Display': '6.77" AMOLED 120Hz',
                    'Camera': '50MP Main',
                    'Battery': '7300mAh',
                    'OS': 'Android 15'
                }
            },
            {
                'name': 'Vivo Y400 5G 128GB',
                'brand': 'vivo',
                'price': Decimal('279.99'),
                'description': 'Fast charging mid-range with strong display and selfie camera',
                'image_url': 'https://via.placeholder.com/200x200?text=Vivo+Y400',
                'specs': {
                    'Processor': 'Snapdragon 4 Gen 2',
                    'RAM': '8GB',
                    'Storage': '128GB',
                    'Display': '6.67" AMOLED 120Hz',
                    'Camera': '50MP + 2MP',
                    'Battery': '5000mAh',
                    'OS': 'Android 15'
                }
            },
                        {
                'name': 'Samsung Galaxy A15 5G',
                'brand': 'Samsung',
                'price': Decimal('229.99'),
                'description': 'Affordable 5G phone with AMOLED display and solid battery life',
                'image_url': 'https://via.placeholder.com/200x200?text=Samsung+Galaxy+A15+5G',
                'specs': {
                    'Processor': 'MediaTek Dimensity 6100+',
                    'RAM': '6GB',
                    'Storage': '128GB',
                    'Display': '6.5" Super AMOLED 90Hz',
                    'Camera': '50MP Triple Camera',
                    'Battery': '5000mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'Motorola Moto G Power 5G (2025)',
                'brand': 'Motorola',
                'price': Decimal('249.99'),
                'description': 'Great battery endurance with clean Android experience',
                'image_url': 'https://via.placeholder.com/200x200?text=Moto+G+Power+5G+2025',
                'specs': {
                    'Processor': 'MediaTek Dimensity 7020',
                    'RAM': '8GB',
                    'Storage': '128GB',
                    'Display': '6.7" LCD 120Hz',
                    'Camera': '50MP Main + 8MP Ultra-wide',
                    'Battery': '5200mAh',
                    'OS': 'Android 15'
                }
            },
            {
                'name': 'Realme Narzo 70 Pro',
                'brand': 'Realme',
                'price': Decimal('229.99'),
                'description': 'Budget phone with flagship-style camera performance',
                'image_url': 'https://via.placeholder.com/200x200?text=Realme+Narzo+70+Pro',
                'specs': {
                    'Processor': 'MediaTek Dimensity 7050',
                    'RAM': '8GB',
                    'Storage': '256GB',
                    'Display': '6.67" AMOLED 120Hz',
                    'Camera': '50MP Sony IMX890',
                    'Battery': '5000mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'Infinix Zero 30 5G',
                'brand': 'Infinix',
                'price': Decimal('279.99'),
                'description': 'Budget creator-friendly phone with high-end selfie camera',
                'image_url': 'https://via.placeholder.com/200x200?text=Infinix+Zero+30+5G',
                'specs': {
                    'Processor': 'MediaTek Dimensity 8020',
                    'RAM': '8GB',
                    'Storage': '128GB',
                    'Display': '6.78" AMOLED 144Hz',
                    'Camera': '108MP Main + 50MP Front',
                    'Battery': '5000mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'Xiaomi Redmi Note 13 5G',
                'brand': 'Xiaomi',
                'price': Decimal('199.99'),
                'description': 'Excellent overall budget performer with smooth display',
                'image_url': 'https://via.placeholder.com/200x200?text=Redmi+Note+13+5G',
                'specs': {
                    'Processor': 'MediaTek Dimensity 6100+',
                    'RAM': '6GB',
                    'Storage': '128GB',
                    'Display': '6.6" LCD 120Hz',
                    'Camera': '50MP Dual Camera',
                    'Battery': '5000mAh',
                    'OS': 'Android 13'
                }
            },
            {
                'name': 'POCO M6 Pro 5G',
                'brand': 'POCO',
                'price': Decimal('199.99'),
                'description': 'Top budget choice with smooth AMOLED display and fast charging',
                'image_url': 'https://via.placeholder.com/200x200?text=POCO+M6+Pro+5G',
                'specs': {
                    'Processor': 'MediaTek Helio G99',
                    'RAM': '8GB',
                    'Storage': '256GB',
                    'Display': '6.6" AMOLED 120Hz',
                    'Camera': '50MP Triple Camera',
                    'Battery': '5000mAh, 67W fast charging',
                    'OS': 'Android 13'
                }
            },
            {
                'name': 'Samsung Galaxy A26 5G',
                'brand': 'Samsung',
                'price': Decimal('299.99'),
                'description': 'Balanced budget phone with AMOLED display and software support',
                'image_url': 'https://via.placeholder.com/200x200?text=Samsung+Galaxy+A26+5G',
                'specs': {
                    'Processor': 'Exynos 1380',
                    'RAM': '8GB',
                    'Storage': '128GB',
                    'Display': '6.7" Super AMOLED 120Hz',
                    'Camera': '50MP Triple Camera',
                    'Battery': '5000mAh',
                    'OS': 'Android 14'
                }
            },
                        {
                'name': 'Xiaomi Redmi 14C',
                'brand': 'Xiaomi',
                'price': Decimal('105.00'),
                'description': 'Affordable all‑round phone with large battery and smooth display',
                'image_url': 'https://via.placeholder.com/200x200?text=Redmi+14C',
                'specs': {
                    'Processor': 'Unisoc T606',
                    'RAM': '4GB',
                    'Storage': '128GB',
                    'Display': '6.53" 120Hz LCD',
                    'Camera': '50MP Main',
                    'Battery': '5000mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'Motorola Moto G Play (2024)',
                'brand': 'Motorola',
                'price': Decimal('139.99'),
                'description': 'Clean Android experience with solid battery life for everyday use',
                'image_url': 'https://via.placeholder.com/200x200?text=Moto+G+Play+2024',
                'specs': {
                    'Processor': 'Unisoc T612',
                    'RAM': '4GB',
                    'Storage': '64GB',
                    'Display': '6.6" HD+ LCD',
                    'Camera': '50MP Main',
                    'Battery': '5000mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'Samsung Galaxy A05',
                'brand': 'Samsung',
                'price': Decimal('139.99'),
                'description': 'Basic Samsung phone with reliable performance and battery life',
                'image_url': 'https://via.placeholder.com/200x200?text=Samsung+Galaxy+A05',
                'specs': {
                    'Processor': 'Unisoc T606',
                    'RAM': '4GB',
                    'Storage': '64GB',
                    'Display': '6.6" LCD',
                    'Camera': '50MP Main + 2MP Depth',
                    'Battery': '5000mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'TCL 40 SE',
                'brand': 'TCL',
                'price': Decimal('129.99'),
                'description': 'Budget‑friendly phone with long battery life and large storage',
                'image_url': 'https://via.placeholder.com/200x200?text=TCL+40+SE',
                'specs': {
                    'Processor': 'Unisoc Tiger T606',
                    'RAM': '4GB',
                    'Storage': '128GB',
                    'Display': '6.75" HD+ 90Hz',
                    'Camera': '13MP Main',
                    'Battery': '5010mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'Realme C55 (base)',
                'brand': 'Realme',
                'price': Decimal('149.99'),
                'description': 'One of the faster budget performers with big battery and solid camera',
                'image_url': 'https://via.placeholder.com/200x200?text=Realme+C55',
                'specs': {
                    'Processor': 'Helio G88',
                    'RAM': '6GB',
                    'Storage': '128GB',
                    'Display': '6.72" FHD+ LCD',
                    'Camera': '64MP Main + 2MP Macro',
                    'Battery': '5000mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'Redmi A3',
                'brand': 'Xiaomi',
                'price': Decimal('125.00'),
                'description': 'Entry‑level Android phone with big battery and basic daily performance',
                'image_url': 'https://via.placeholder.com/200x200?text=Redmi+A3',
                'specs': {
                    'Processor': 'Unisoc SC9863A',
                    'RAM': '4GB',
                    'Storage': '128GB',
                    'Display': '6.71" HD+ LCD',
                    'Camera': '8MP Main',
                    'Battery': '5000mAh',
                    'OS': 'Android 13'
                }
            },
            {
                'name': 'OPPO Reno 11 Pro 5G',
                'brand': 'OPPO',
                'price': Decimal('549.99'),
                'description': 'Stylish phone with excellent portrait camera',
                'image_url': 'https://m.media-amazon.com/images/I/61JZCk7dUpL.jpg',
                'specs': {
                    'Processor': 'MediaTek Dimensity 8200',
                    'RAM': '12GB',
                    'Storage': '256GB',
                    'Display': '6.7" AMOLED 120Hz',
                    'Camera': '50MP Sony IMX890',
                    'Battery': '4600mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'vivo X100 Pro',
                'brand': 'vivo',
                'price': Decimal('899.99'),
                'description': 'Photography flagship with ZEISS optics',
                'image_url': 'https://m.media-amazon.com/images/I/61y2VVWcGBL.jpg',
                'specs': {
                    'Processor': 'MediaTek Dimensity 9300',
                    'RAM': '16GB',
                    'Storage': '512GB',
                    'Display': '6.78" LTPO AMOLED',
                    'Camera': '50MP ZEISS Triple Camera',
                    'Battery': '5400mAh',
                    'OS': 'Android 14'
                }
            },
            {
                'name': 'iPhone 15 Pro Max 256GB',
                'brand': 'Apple',
                'price': Decimal('1199.99'),
                'description': 'Premium flagship with titanium design and A17 Pro chip',
                'image_url': 'https://images.unsplash.com/photo-1592286927505-0960c995c1a5?w=400',
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
                'image_url': 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400',
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
                'image_url': 'https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=400',
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
                'image_url': 'https://m.media-amazon.com/images/I/71XEjCc4yLL.jpg',
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
                'image_url': 'https://m.media-amazon.com/images/I/61v0jm3fW1L._AC_UF350,350_QL50_.jpg',
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
                'name': 'Dell XPS 15 (2025)',
                'brand': 'Dell',
                'price': Decimal('1999.99'),
                'description': 'Premium Windows laptop with 16″ OLED display and powerful performance',
                'image_url': 'https://via.placeholder.com/200x200?text=Dell+XPS+15+2025',
                'specs': {
                    'Processor': 'Intel Core Ultra 9 / AMD Ryzen 9 9950X',
                    'RAM': '32GB',
                    'Storage': '1TB SSD',
                    'Display': '15.6" 4K OLED',
                    'Graphics': 'Intel Arc / Optional NVIDIA',
                    'Battery': 'Up to 12 hours',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'HP Spectre x360 14 (2025)',
                'brand': 'HP',
                'price': Decimal('1499.99'),
                'description': 'Convertible 2‑in‑1 with 14″ OLED touchscreen and Intel Core i7 performance',
                'image_url': 'https://via.placeholder.com/200x200?text=HP+Spectre+x360+14',
                'specs': {
                    'Processor': 'Intel Core i7-1360P',
                    'RAM': '16GB',
                    'Storage': '1TB SSD',
                    'Display': '14" OLED Touchscreen',
                    'Graphics': 'Intel Iris Xe',
                    'Battery': 'Up to 10 hours',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'Asus ROG Zephyrus G16 (2025)',
                'brand': 'ASUS',
                'price': Decimal('2299.99'),
                'description': 'High‑end gaming laptop with QHD+ display and RTX 5090 GPU',
                'image_url': 'https://via.placeholder.com/200x200?text=Asus+ROG+Zephyrus+G16',
                'specs': {
                    'Processor': 'AMD Ryzen 9 9950HX / Intel Core i9-14900HX',
                    'RAM': '32GB DDR5',
                    'Storage': '2TB SSD',
                    'Display': '16" QHD+ 165Hz',
                    'Graphics': 'NVIDIA RTX 5090 16GB',
                    'Battery': '90Whr',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'Lenovo ThinkPad X1 Carbon Gen 12 (2025)',
                'brand': 'Lenovo',
                'price': Decimal('1599.99'),
                'description': 'Business ultrabook with lightweight design and enterprise features',
                'image_url': 'https://via.placeholder.com/200x200?text=ThinkPad+X1+Carbon+Gen+12',
                'specs': {
                    'Processor': 'Intel Core Ultra 7 / AMD Ryzen 7 Pro',
                    'RAM': '16GB',
                    'Storage': '1TB SSD',
                    'Display': '14" 2.8K OLED',
                    'Graphics': 'Intel Iris Xe',
                    'Battery': 'Up to 15 hours',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'Microsoft Surface Laptop 6',
                'brand': 'Microsoft',
                'price': Decimal('1299.99'),
                'description': 'ARM‑based ultraportable laptop with long battery life and premium build',
                'image_url': 'https://via.placeholder.com/200x200?text=Surface+Laptop+6',
                'specs': {
                    'Processor': 'Qualcomm Snapdragon X Elite',
                    'RAM': '16GB LPDDR5X',
                    'Storage': '512GB SSD',
                    'Display': '13.5" 2.8K',
                    'Graphics': 'Integrated ARM',
                    'Battery': 'Up to 20 hours',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'Acer Swift X 14 (2025)',
                'brand': 'Acer',
                'price': Decimal('1199.99'),
                'description': '16‑core performance laptop with RTX 5060 GPU for creator workflows',
                'image_url': 'https://via.placeholder.com/200x200?text=Acer+Swift+X+14',
                'specs': {
                    'Processor': 'Intel Core Ultra 7 155H',
                    'RAM': '16GB',
                    'Storage': '1TB SSD',
                    'Display': '14.5" 2.8K 120Hz',
                    'Graphics': 'NVIDIA RTX 5060 6GB',
                    'Battery': '76Whr',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'Acer Aspire Lite 15',
                'brand': 'Acer',
                'price': Decimal('599.99'),
                'description': 'Everyday laptop for study and productivity with Ryzen 3 performance',
                'image_url': 'https://via.placeholder.com/200x200?text=Acer+Aspire+Lite+15',
                'specs': {
                    'Processor': 'AMD Ryzen 3 7330U',
                    'RAM': '16GB DDR4',
                    'Storage': '512GB SSD',
                    'Display': '15.6" FHD',
                    'Graphics': 'Integrated',
                    'Battery': 'Up to 8 hours',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'HP 15 (Intel Core i5)',
                'brand': 'HP',
                'price': Decimal('499.99'),
                'description': 'Budget‑friendly everyday laptop with crisp FHD display',
                'image_url': 'https://via.placeholder.com/200x200?text=HP+15+i5',
                'specs': {
                    'Processor': 'Intel Core i5-1334U',
                    'RAM': '8GB',
                    'Storage': '512GB SSD',
                    'Display': '15.6" FHD',
                    'Graphics': 'Intel Iris Xe',
                    'Battery': 'Up to 7 hours',
                    'OS': 'Windows 11'
                }
            },
                        {
                'name': 'Acer Chromebook Plus 515',
                'brand': 'Acer',
                'price': Decimal('299.99'),
                'description': 'Balanced Chromebook with strong performance and battery for school tasks',
                'image_url': 'https://via.placeholder.com/200x200?text=Acer+Chromebook+Plus+515',
                'specs': {
                    'Processor': 'Intel Core i3-1215U',
                    'RAM': '8GB LPDDR5',
                    'Storage': '128GB SSD',
                    'Display': '15.6" FHD',
                    'Battery': 'Up to 10 hours',
                    'OS': 'Chrome OS'
                }
            },
            {
                'name': 'HP Chromebook Plus 15.6"',
                'brand': 'HP',
                'price': Decimal('329.99'),
                'description': 'Large screen Chromebook for productivity and school work',
                'image_url': 'https://via.placeholder.com/200x200?text=HP+Chromebook+Plus+15.6',
                'specs': {
                    'Processor': 'Intel Core i3‑N305',
                    'RAM': '8GB LPDDR5',
                    'Storage': '128GB UFS',
                    'Display': '15.6" FHD 144Hz',
                    'Battery': 'Up to 10 hours',
                    'OS': 'Chrome OS'
                }
            },
            {
                'name': 'Lenovo IdeaPad Flex 5i Chromebook Plus',
                'brand': 'Lenovo',
                'price': Decimal('379.99'),
                'description': 'Versatile 2‑in‑1 Chromebook with touch display, ideal for school and creativity',
                'image_url': 'https://via.placeholder.com/200x200?text=Lenovo+IdeaPad+Flex+5i+Chromebook',
                'specs': {
                    'Processor': 'Intel Core i3‑1315U',
                    'RAM': '8GB',
                    'Storage': '128GB eMMC',
                    'Display': '14" Full HD Touch',
                    'Battery': 'Up to 10 hours',
                    'OS': 'Chrome OS'
                }
            },
            {
                'name': 'Acer Chromebook Spin 312',
                'brand': 'Acer',
                'price': Decimal('249.99'),
                'description': 'Budget 2‑in‑1 Chromebook with solid battery life for note‑taking and browser tasks',
                'image_url': 'https://via.placeholder.com/200x200?text=Acer+Chromebook+Spin+312',
                'specs': {
                    'Processor': 'Intel Core i3‑N305',
                    'RAM': '8GB',
                    'Storage': '128GB eMMC',
                    'Display': '12.2" Touch FHD',
                    'Battery': 'Up to 10 hours',
                    'OS': 'Chrome OS'
                }
            },
            {
                'name': 'Lenovo Chromebook Duet 11 Gen 9',
                'brand': 'Lenovo',
                'price': Decimal('299.99'),
                'description': 'Compact detachable Chromebook ideal for younger students',
                'image_url': 'https://via.placeholder.com/200x200?text=Lenovo+Chromebook+Duet+11',
                'specs': {
                    'Processor': 'MediaTek Helio CPU',
                    'RAM': '8GB',
                    'Storage': '128GB',
                    'Display': '11" Touch FHD',
                    'Battery': 'Up to 12 hours',
                    'OS': 'Chrome OS'
                }
            },
            {
                'name': 'HP Chromebook 14a',
                'brand': 'HP',
                'price': Decimal('229.99'),
                'description': 'Budget Chromebook with basic performance and long battery life for schoolwork',
                'image_url': 'https://via.placeholder.com/200x200?text=HP+Chromebook+14a',
                'specs': {
                    'Processor': 'Intel N200',
                    'RAM': '4GB',
                    'Storage': '64GB eMMC',
                    'Display': '14" HD',
                    'Battery': 'Up to 10 hours',
                    'OS': 'Chrome OS'
                }
            },
                        {
                'name': 'Acer Nitro 5 (RTX 3050)',
                'brand': 'Acer',
                'price': Decimal('779.99'),
                'description': 'Popular budget gaming laptop with RTX 3050 graphics and 144Hz display.',
                'image_url': 'https://via.placeholder.com/200x200?text=Acer+Nitro+5+RTX+3050',
                'specs': {
                    'Processor': 'Intel Core i5-12450H',
                    'RAM': '16GB DDR4',
                    'Storage': '512GB SSD',
                    'Display': '15.6" FHD 144Hz',
                    'Graphics': 'NVIDIA GeForce RTX 3050 4GB',
                    'Battery': 'Up to ~8 hours',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'HP Victus 15 (RTX 3050)',
                'brand': 'HP',
                'price': Decimal('669.99'),
                'description': 'Great entry‑level gaming laptop with RTX 3050 and solid overall performance.',
                'image_url': 'https://via.placeholder.com/200x200?text=HP+Victus+15+RTX+3050',
                'specs': {
                    'Processor': 'Intel Core i5-12450H',
                    'RAM': '16GB DDR4',
                    'Storage': '512GB SSD',
                    'Display': '15.6" FHD 144Hz',
                    'Graphics': 'NVIDIA GeForce RTX 3050 4GB',
                    'Battery': 'Up to ~7.5 hours',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'Lenovo IdeaPad Gaming 3',
                'brand': 'Lenovo',
                'price': Decimal('699.99'),
                'description': 'Balanced budget gaming laptop with Ryzen 5 and GTX/RTX graphics for 1080p gaming.',
                'image_url': 'https://via.placeholder.com/200x200?text=Lenovo+IdeaPad+Gaming+3',
                'specs': {
                    'Processor': 'AMD Ryzen 5 6600H',
                    'RAM': '8GB DDR5',
                    'Storage': '512GB SSD',
                    'Display': '15.6" FHD 120Hz',
                    'Graphics': 'NVIDIA GeForce RTX 3050 / GTX 1650',
                    'Battery': 'Up to ~7 hours',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'ASUS TUF Gaming A15',
                'brand': 'ASUS',
                'price': Decimal('742.99'),
                'description': 'Durable gaming laptop with high‑refresh display and capable GPU for budget gamers.',
                'image_url': 'https://via.placeholder.com/200x200?text=ASUS+TUF+Gaming+A15',
                'specs': {
                    'Processor': 'AMD Ryzen 7 7535HS',
                    'RAM': '8GB DDR5',
                    'Storage': '512GB SSD',
                    'Display': '15.6" FHD 144Hz',
                    'Graphics': 'NVIDIA GeForce RTX 3050 4GB',
                    'Battery': 'Up to ~8 hours',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'MSI GF63 Thin',
                'brand': 'MSI',
                'price': Decimal('689.99'),
                'description': 'Portable budget gaming laptop with decent GPU and slimmer chassis for easy mobility.',
                'image_url': 'https://via.placeholder.com/200x200?text=MSI+GF63+Thin',
                'specs': {
                    'Processor': 'Intel Core i5-12450H',
                    'RAM': '8GB DDR4',
                    'Storage': '512GB SSD',
                    'Display': '15.6" FHD 144Hz',
                    'Graphics': 'NVIDIA GeForce RTX 3050 4GB',
                    'Battery': 'Up to ~7 hours',
                    'OS': 'Windows 11'
                }
            },
                        {
                'name': 'Acer Nitro 5 (RTX 3050 Budget)',
                'brand': 'Acer',
                'price': Decimal('599.99'),
                'description': 'Entry‑level gaming laptop with RTX 3050 for solid 1080p gaming on a budget.',
                'image_url': 'https://via.placeholder.com/200x200?text=Acer+Nitro+5+RTX+3050',
                'specs': {
                    'Processor': 'Intel Core i5-12500H',
                    'RAM': '8GB DDR4',
                    'Storage': '512GB SSD',
                    'Display': '15.6" FHD 60Hz',
                    'Graphics': 'NVIDIA GeForce RTX 3050 4GB',
                    'Battery': 'Up to ~7 hours',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'Lenovo IdeaPad Gaming 3 (GTX 1650)',
                'brand': 'Lenovo',
                'price': Decimal('579.99'),
                'description': 'Budget gaming option with GTX 1650 — good for esports titles at medium settings.',
                'image_url': 'https://via.placeholder.com/200x200?text=Lenovo+IdeaPad+Gaming+3+1650',
                'specs': {
                    'Processor': 'AMD Ryzen 5 5600H',
                    'RAM': '8GB DDR4',
                    'Storage': '512GB SSD',
                    'Display': '15.6" FHD 60Hz',
                    'Graphics': 'NVIDIA GeForce GTX 1650 4GB',
                    'Battery': 'Up to ~6.5 hours',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'HP Victus 15 (Radeon RX 6550M)',
                'brand': 'HP',
                'price': Decimal('599.99'),
                'description': 'Affordable gaming laptop with RX 6550M for entry 1080p play and esports titles.',
                'image_url': 'https://via.placeholder.com/200x200?text=HP+Victus+15+6550M',
                'specs': {
                    'Processor': 'AMD Ryzen 5 7535HS',
                    'RAM': '8GB DDR5',
                    'Storage': '512GB SSD',
                    'Display': '15.6" FHD 144Hz',
                    'Graphics': 'AMD Radeon RX 6550M',
                    'Battery': 'Up to ~7 hours',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'MSI GF63 Thin (GTX 1650)',
                'brand': 'MSI',
                'price': Decimal('589.99'),
                'description': 'Slim budget gaming laptop with GTX 1650 — good for lighter modern gaming.',
                'image_url': 'https://via.placeholder.com/200x200?text=MSI+GF63+Thin+1650',
                'specs': {
                    'Processor': 'Intel Core i5-12450H',
                    'RAM': '8GB DDR4',
                    'Storage': '512GB SSD',
                    'Display': '15.6" FHD 60Hz',
                    'Graphics': 'NVIDIA GeForce GTX 1650 4GB',
                    'Battery': 'Up to ~6 hours',
                    'OS': 'Windows 11'
                }
            },
            {
                'name': 'Acer Aspire 5 Gaming (Integrated)',
                'brand': 'Acer',
                'price': Decimal('449.99'),
                'description': 'Affordable laptop with strong integrated graphics that handles popular esports titles and light gaming.',
                'image_url': 'https://via.placeholder.com/200x200?text=Acer+Aspire+5+Gaming',
                'specs': {
                    'Processor': 'AMD Ryzen 7 5700U',
                    'RAM': '8GB DDR4',
                    'Storage': '512GB SSD',
                    'Display': '15.6" FHD 60Hz',
                    'Graphics': 'AMD Radeon Vega 8 (Integrated)',
                    'Battery': 'Up to ~8 hours',
                    'OS': 'Windows 11'
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
