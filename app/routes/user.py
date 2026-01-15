from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.product import Product, Brand, Category
from app.services.recommendation_service import RecommendationService
from app.services.comparison_service import ComparisonService
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
        # Get category from form data (e.g., 'smartphone' or 'laptop')
        category_value = form.category.data  # This is a string like 'smartphone' or 'laptop'
        
        # Look up the category in the database by name
        category = Category.query.filter(db.func.lower(Category.name) == category_value.lower()).first()
        
        # Collect user inputs
        user_inputs = {
            'category': category_value.lower(),  # Use the form value as category name
            'category_id': category.id if category else None,  # Get the actual ID from database
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
    """Compare multiple products side-by-side"""
    from flask import flash
    
    # Get product IDs from query string
    product_ids = request.args.get('ids', '')
    
    if not product_ids:
        flash('Please select products to compare.', 'warning')
        return redirect(url_for('user.home'))
    
    # Parse comma-separated IDs
    try:
        ids = [int(id.strip()) for id in product_ids.split(',') if id.strip()]
    except ValueError:
        flash('Invalid product IDs.', 'error')
        return redirect(url_for('user.home'))
    
    # Validate number of products (2-4)
    if len(ids) < 2:
        flash('Please select at least 2 products to compare.', 'warning')
        return redirect(url_for('user.home'))
    if len(ids) > 4:
        flash('You can compare up to 4 products at a time.', 'warning')
        ids = ids[:4]
    
    # Fetch products with their specifications
    products = Product.query.filter(Product.id.in_(ids)).all()
    
    if not products:
        flash('No products found.', 'error')
        return redirect(url_for('user.home'))
    
    # Build comparison data
    comparison_data = []
    all_spec_keys = set()
    
    for product in products:
        specs = {spec.spec_key: spec.spec_value for spec in product.specifications}
        all_spec_keys.update(specs.keys())
        
        comparison_data.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand.name if product.brand else 'N/A',
            'category': product.category.name if product.category else 'N/A',
            'price': float(product.price),
            'image_url': product.image_url or '/static/images/placeholder.png',
            'description': product.description or '',
            'specifications': specs
        })
    
    # Sort specification keys for consistent display
    sorted_spec_keys = sorted(all_spec_keys)
    
    return render_template('user/compare.html',
                         products=comparison_data,
                         spec_keys=sorted_spec_keys)


@user_bp.route('/compare-analysis')
def compare_analysis():
    """Pros & Cons comparison for exactly 2 products"""
    from flask import flash
    
    # Get product IDs from query string
    product_ids = request.args.get('ids', '')
    
    if not product_ids:
        flash('Please select products to compare.', 'warning')
        return redirect(url_for('user.home'))
    
    # Parse comma-separated IDs
    try:
        ids = [int(id.strip()) for id in product_ids.split(',') if id.strip()]
    except ValueError:
        flash('Invalid product IDs.', 'error')
        return redirect(url_for('user.home'))
    
    # Validate exactly 2 products
    if len(ids) != 2:
        flash('Please select exactly 2 products for Pros & Cons analysis.', 'warning')
        return redirect(url_for('user.home'))
    
    # Fetch products
    products = Product.query.filter(Product.id.in_(ids)).all()
    
    if len(products) != 2:
        flash('One or more selected products could not be found.', 'error')
        return redirect(url_for('user.home'))
    
    # Get user preferences from session
    user_preferences = session.get('last_preferences', {})
    
    # Perform analysis
    comp_service = ComparisonService()
    # pass products in the order they were requested if possible, strictly speaking the query result order isn't guaranteed relative to ID list order without explicit ordering
    # but for comparison it doesn't matter much which is p1 and p2 initially
    analysis_data = comp_service.compare_two_products(products[0], products[1], user_preferences)
    
    return render_template('user/comparison_analysis.html', **analysis_data)


@user_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """Display detailed view of a single product"""
    from flask import flash
    
    # Fetch product with all relationships
    product = Product.query.get_or_404(product_id)
    
    # Get specifications as a dictionary
    specs = {spec.spec_key: spec.spec_value for spec in product.specifications}
    
    # Group specifications by category for better display
    spec_categories = {
        'Performance': ['Processor', 'RAM', 'Graphics', 'Storage', 'SSD'],
        'Display': ['Display', 'Screen', 'Resolution'],
        'Camera': ['Camera', 'Front Camera', 'Video'],
        'Battery & Power': ['Battery', 'Charging', 'Power'],
        'System': ['OS', 'Operating System'],
        'Physical': ['Weight', 'Dimensions', 'Build']
    }
    
    # Categorize specs
    categorized_specs = {}
    uncategorized_specs = {}
    
    for key, value in specs.items():
        categorized = False
        for category, keywords in spec_categories.items():
            if any(keyword.lower() in key.lower() for keyword in keywords):
                if category not in categorized_specs:
                    categorized_specs[category] = {}
                categorized_specs[category][key] = value
                categorized = True
                break
        if not categorized:
            uncategorized_specs[key] = value
    
    # Add uncategorized to "Other" category if exists
    if uncategorized_specs:
        categorized_specs['Other'] = uncategorized_specs
    
    return render_template('user/product_detail.html',
                         product=product,
                         specs=specs,
                         categorized_specs=categorized_specs)

