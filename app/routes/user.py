from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.product import Product, Brand, Category
from app.services.recommendation_service import RecommendationService
from app.forms.recommendation_forms import RecommendationForm
from app import db

user_bp = Blueprint('user', __name__)


@user_bp.route('/')
def home():
    """Home page"""
    return render_template('user/home.html')


@user_bp.route('/recommend', methods=['GET', 'POST'])
def recommend():
    """Recommendation questionnaire and results"""
    form = RecommendationForm()
    
    if form.validate_on_submit():
        # Get category name from ID
        category_id = form.category.data
        category = Category.query.get(category_id)
        category_name = category.name.lower() if category else None
        
        # Collect user inputs
        user_inputs = {
            'category': category_name,  # Convert ID to lowercase name
            'category_id': category_id,  # Keep ID for product filtering
            'budget': form.budget.data,
            'usage_type': form.usage_type.data,
            'preferred_brand': form.preferred_brand.data if form.preferred_brand.data else None
        }
        
        # Get recommendations
        rec_service = RecommendationService()
        recommendations = rec_service.get_recommendations(user_inputs, limit=9)
        
        # Store in session
        session['last_preferences'] = user_inputs
        
        return render_template('user/results.html',
                             products=recommendations.get('products', []),
                             message=recommendations.get('message', ''),
                             total_matches=recommendations.get('total_matches', 0),
                             fired_rules=recommendations.get('fired_rules', 0))
    
    # GET request - show questionnaire
    return render_template('user/questionnaire.html', form=form)


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
