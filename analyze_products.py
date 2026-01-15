from app import create_app, db
from app.models.product import Product, Category

app = create_app()
app.app_context().push()

print("=" * 60)
print("PRODUCT DATABASE ANALYSIS")
print("=" * 60)

# Smartphones
print("\n=== SMARTPHONE ANALYSIS ===")
phones = Product.query.join(Category).filter(Category.name == 'Smartphone').order_by(Product.price).all()
print(f"Count: {len(phones)}")
if phones:
    print(f"Price range: ${min(p.price for p in phones):.2f} - ${max(p.price for p in phones):.2f}")
    budget = sum(1 for p in phones if p.price < 500)
    mid = sum(1 for p in phones if 500 <= p.price < 800)
    flagship = sum(1 for p in phones if p.price >= 800)
    print(f"Budget (<$500): {budget}")
    print(f"Mid-range ($500-800): {mid}")
    print(f"Flagship ($800+): {flagship}")

# Laptops
print("\n=== LAPTOP ANALYSIS ===")
laptops = Product.query.join(Category).filter(Category.name == 'Laptop').order_by(Product.price).all()
print(f"Count: {len(laptops)}")
if laptops:
    print(f"Price range: ${min(p.price for p in laptops):.2f} - ${max(p.price for p in laptops):.2f}")
    budget_l = sum(1 for p in laptops if p.price < 700)
    mid_l = sum(1 for p in laptops if 700 <= p.price < 1200)
    premium_l = sum(1 for p in laptops if p.price >= 1200)
    print(f"Budget (<$700): {budget_l}")
    print(f"Mid-range ($700-1200): {mid_l}")
    print(f"Premium ($1200+): {premium_l}")

print(f"\n{'=' * 60}")
print(f"TOTAL PRODUCTS: {len(phones) + len(laptops)}")
print(f"Proposal Requirement: 50+ products")
if len(phones) + len(laptops) >= 50:
    print("✅ REQUIREMENT MET")
else:
    print(f"❌ NEED {50 - (len(phones) + len(laptops))} MORE PRODUCTS")
print("=" * 60)
