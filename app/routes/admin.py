from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import User, AuditLog
from app.models.product import Product, Brand, Category, Specification
from app.models.rule import Rule, RuleCondition
from app.forms.product_forms import ProductForm, BrandForm
from app.forms.rule_forms import RuleForm
from app import db
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def staff_required(f):
    """Decorator to require staff or admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'staff']:
            flash('Staff access required', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@login_required
@staff_required
def dashboard():
    """Admin dashboard"""
    # Get statistics
    total_products = Product.query.filter_by(is_active=True).count()
    total_brands = Brand.query.count()
    total_rules = Rule.query.filter_by(is_active=True).count()
    total_users = User.query.filter_by(is_active=True).count()
    
    return render_template('admin/dashboard.html',
                         total_products=total_products,
                         total_brands=total_brands,
                         total_rules=total_rules,
                         total_users=total_users)


@admin_bp.route('/products')
@login_required
@staff_required
def products():
    """Product listing with search and filters"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category_id = request.args.get('category', type=int)
    brand_id = request.args.get('brand', type=int)
    
    query = Product.query
    
    # Apply search filter
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    
    # Apply category filter
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Apply brand filter
    if brand_id:
        query = query.filter_by(brand_id=brand_id)
    
    # Paginate results
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Get all categories and brands for filters
    categories = Category.query.order_by(Category.name).all()
    brands = Brand.query.order_by(Brand.name).all()
    
    return render_template('admin/products.html',
                         products=products,
                         categories=categories,
                         brands=brands)


@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@staff_required
def product_add():
    """Add new product"""
    form = ProductForm()
    
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            brand_id=form.brand_id.data,
            category_id=form.category_id.data,
            price=form.price.data,
            description=form.description.data,
            image_url=form.image_url.data,
            is_active=form.is_active.data
        )
        
        db.session.add(product)
        db.session.commit()
        
        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='create',
            entity_type='Product',
            entity_id=product.id,
            details=f'Created product: {product.name}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'Product "{product.name}" created successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/product_form.html', form=form, product=None)


@admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@staff_required
def product_edit(product_id):
    """Edit existing product"""
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.brand_id = form.brand_id.data
        product.category_id = form.category_id.data
        product.price = form.price.data
        product.description = form.description.data
        product.image_url = form.image_url.data
        product.is_active = form.is_active.data
        
        # Handle specifications
        Specification.query.filter_by(product_id=product.id).delete()
        
        spec_index = 0
        while True:
            spec_key = request.form.get(f'spec_key_{spec_index}')
            spec_value = request.form.get(f'spec_value_{spec_index}')
            
            if spec_key is None:
                break
            
            if spec_key and spec_value:
                spec = Specification(
                    product_id=product.id,
                    spec_key=spec_key,
                    spec_value=spec_value
                )
                db.session.add(spec)
            
            spec_index += 1
        
        db.session.commit()
        
        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='update',
            entity_type='Product',
            entity_id=product.id,
            details=f'Updated product: {product.name}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'Product "{product.name}" updated successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/product_form.html', form=form, product=product)


@admin_bp.route('/products/<int:product_id>/delete', methods=['POST', 'GET'])
@login_required
@staff_required
def product_delete(product_id):
    """Delete product"""
    product = Product.query.get_or_404(product_id)
    product_name = product.name
    
    # Delete related specifications
    Specification.query.filter_by(product_id=product.id).delete()
    
    # Log the action before deleting
    audit_log = AuditLog(
        user_id=current_user.id,
        action='delete',
        entity_type='Product',
        entity_id=product.id,
        details=f'Deleted product: {product_name}'
    )
    db.session.add(audit_log)
    
    db.session.delete(product)
    db.session.commit()
    
    flash(f'Product "{product_name}" deleted successfully!', 'success')
    return redirect(url_for('admin.products'))


@admin_bp.route('/rules')
@login_required
@staff_required
def rules():
    """Rule management with search and filters"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    query = Rule.query
    
    # Apply search filter
    if search:
        query = query.filter(Rule.name.ilike(f'%{search}%'))
    
    # Apply status filter
    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)
    
    # Paginate results
    rules = query.order_by(Rule.priority.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/rules.html', rules=rules)


@admin_bp.route('/rules/add', methods=['GET', 'POST'])
@login_required
@staff_required
def rule_add():
    """Add new rule"""
    form = RuleForm()
    
    if form.validate_on_submit():
        rule = Rule(
            name=form.name.data,
            description=form.description.data,
            priority=form.priority.data,
            category_id=form.category_id.data,
            is_active=form.is_active.data
        )
        
        db.session.add(rule)
        db.session.commit()
        
        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='create',
            entity_type='Rule',
            entity_id=rule.id,
            details=f'Created rule: {rule.name}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'Rule "{rule.name}" created successfully!', 'success')
        return redirect(url_for('admin.rules'))
    
    return render_template('admin/rule_form.html', form=form, rule=None)


@admin_bp.route('/rules/<int:rule_id>/edit', methods=['GET', 'POST'])
@login_required
@staff_required
def rule_edit(rule_id):
    """Edit existing rule"""
    rule = Rule.query.get_or_404(rule_id)
    form = RuleForm(obj=rule)
    
    if form.validate_on_submit():
        rule.name = form.name.data
        rule.description = form.description.data
        rule.priority = form.priority.data
        rule.category_id = form.category_id.data
        rule.is_active = form.is_active.data
        
        # Handle conditions
        RuleCondition.query.filter_by(rule_id=rule.id).delete()
        
        cond_index = 0
        while True:
            cond_key = request.form.get(f'cond_key_{cond_index}')
            cond_operator = request.form.get(f'cond_operator_{cond_index}')
            cond_value = request.form.get(f'cond_value_{cond_index}')
            
            if cond_key is None:
                break
            
            if cond_key and cond_operator and cond_value:
                condition = RuleCondition(
                    rule_id=rule.id,
                    condition_type='user_input',
                    condition_key=cond_key,
                    operator=cond_operator,
                    condition_value=cond_value
                )
                db.session.add(condition)
            
            cond_index += 1
        
        db.session.commit()
        
        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='update',
            entity_type='Rule',
            entity_id=rule.id,
            details=f'Updated rule: {rule.name}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'Rule "{rule.name}" updated successfully!', 'success')
        return redirect(url_for('admin.rules'))
    
    return render_template('admin/rule_form.html', form=form, rule=rule)


@admin_bp.route('/rules/<int:rule_id>/delete', methods=['POST', 'GET'])
@login_required
@staff_required
def rule_delete(rule_id):
    """Delete rule"""
    rule = Rule.query.get_or_404(rule_id)
    rule_name = rule.name
    
    # Delete related conditions
    RuleCondition.query.filter_by(rule_id=rule.id).delete()
    
    # Log the action before deleting
    audit_log = AuditLog(
        user_id=current_user.id,
        action='delete',
        entity_type='Rule',
        entity_id=rule.id,
        details=f'Deleted rule: {rule_name}'
    )
    db.session.add(audit_log)
    
    db.session.delete(rule)
    db.session.commit()
    
    flash(f'Rule "{rule_name}" deleted successfully!', 'success')
    return redirect(url_for('admin.rules'))


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """User management (admin only)"""
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/users.html', users=users)
