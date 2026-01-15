from flask import Blueprint, render_template, request, redirect, url_for
from app.models.product import Product, Brand, Category
from app.services.recommendation_service import RecommendationService
from app import db

user_bp = Blueprint('user', __name__)


@user_bp.route('/')
def home():
    """Home page"""
    return render_template('user/home.html')


@user_bp.route('/recommend', methods=['GET', 'POST'])
def recommend():
    """Recommendation questionnaire and results"""
    if request.method == 'POST':
        # Collect user inputs
        user_inputs = {
            'category': request.form.get('category'),
            'max_budget': request.form.get('budget'),
            'usage_type': request.form.get('usage_type'),
            'preferred_brand': request.form.get('brand', 'Any'),
            'requirements': request.form.getlist('requirements')
        }
        
        # Get recommendations
        rec_service = RecommendationService()
        recommendations = rec_service.get_recommendations(user_inputs, limit=3)
        
        return render_template('user/results.html', 
                             recommendations=recommendations,
                             user_inputs=user_inputs)
    
    # GET request - show questionnaire
    brands = Brand.query.all()
    categories = Category.query.all()
    return render_template('user/questionnaire.html', brands=brands, categories=categories)


@user_bp.route('/compare')
def compare():
    """Product comparison page"""
    product_id_1 = request.args.get('p1', type=int)
    product_id_2 = request.args.get('p2', type=int)
    
    if not product_id_1 or not product_id_2:
        return redirect(url_for('user.home'))
    
    product1 = Product.query.get_or_404(product_id_1)
    product2 = Product.query.get_or_404(product_id_2)
    
    return render_template('user/compare.html', product1=product1, product2=product2)
