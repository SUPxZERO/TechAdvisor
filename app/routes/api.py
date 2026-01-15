from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models.product import Product, Brand, Category
from app.models.rule import Rule
from app import db

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/products')
def get_products():
    """Get all active products"""
    category = request.args.get('category')
    brand = request.args.get('brand')
    
    query = Product.query.filter_by(is_active=True)
    
    if category:
        cat = Category.query.filter_by(name=category).first()
        if cat:
            query = query.filter_by(category_id=cat.id)
    
    if brand:
        br = Brand.query.filter_by(name=brand).first()
        if br:
            query = query.filter_by(brand_id=br.id)
    
    products = query.all()
    return jsonify([product.to_dict() for product in products])


@api_bp.route('/products/<int:product_id>')
def get_product(product_id):
    """Get single product by ID"""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())


@api_bp.route('/brands')
def get_brands():
    """Get all brands"""
    brands = Brand.query.all()
    return jsonify([{'id': b.id, 'name': b.name, 'logo_url': b.logo_url} for b in brands])


@api_bp.route('/categories')
def get_categories():
    """Get all categories"""
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'description': c.description} for c in categories])
