from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import User, AuditLog
from app.models.product import Product, Brand, Category, Specification
from app.models.rule import Rule, RuleCondition
from app.models.role import Role, Permission
from app.forms.product_forms import ProductForm, BrandForm
from app.forms.rule_forms import RuleForm
from app.forms.role_forms import RoleForm
from app.forms.brand_forms import BrandForm
from app.forms.user_forms import UserForm
from app import db
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


from app.utils.decorators import permission_required, admin_required, staff_required

# Decorators moved to app/utils/decorators.py



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
@permission_required('product.view')
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
@permission_required('product.create')
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
            table_name='products',
            record_id=product.id,
            details=f'Created product: {product.name}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'Product "{product.name}" created successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/product_form.html', form=form, product=None)


@admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('product.edit')
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
            table_name='products',
            record_id=product.id,
            details=f'Updated product: {product.name}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'Product "{product.name}" updated successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/product_form.html', form=form, product=product)


@admin_bp.route('/products/<int:product_id>/delete', methods=['POST', 'GET'])
@login_required
@permission_required('product.delete')
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
        table_name='products',
        record_id=product.id,
        details=f'Deleted product: {product_name}'
    )
    db.session.add(audit_log)
    
    db.session.delete(product)
    db.session.commit()
    
    flash(f'Product "{product_name}" deleted successfully!', 'success')
    return redirect(url_for('admin.products'))


@admin_bp.route('/rules')
@login_required
@permission_required('rule.view')
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
@permission_required('rule.manage')
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
            table_name='rules',
            record_id=rule.id,
            details=f'Created rule: {rule.name}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'Rule "{rule.name}" created successfully!', 'success')
        return redirect(url_for('admin.rules'))
    
    return render_template('admin/rule_form.html', form=form, rule=None)


@admin_bp.route('/rules/<int:rule_id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('rule.manage')
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
            table_name='rules',
            record_id=rule.id,
            details=f'Updated rule: {rule.name}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'Rule "{rule.name}" updated successfully!', 'success')
        return redirect(url_for('admin.rules'))
    
    return render_template('admin/rule_form.html', form=form, rule=rule)


@admin_bp.route('/rules/<int:rule_id>/delete', methods=['POST', 'GET'])
@login_required
@permission_required('rule.manage')
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
        table_name='rules',
        record_id=rule.id,
        details=f'Deleted rule: {rule_name}'
    )
    db.session.add(audit_log)
    
    db.session.delete(rule)
    db.session.commit()
    
    flash(f'Rule "{rule_name}" deleted successfully!', 'success')
    return redirect(url_for('admin.rules'))


@admin_bp.route('/users')
@login_required
@permission_required('user.view')
def users():
    """User management (admin only)"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) | 
            (User.email.ilike(f'%{search}%'))
        )
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@permission_required('user.create')
def user_add():
    """Add new user"""
    form = UserForm()
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role_id=form.role_id.data,
            is_active=form.is_active.data
        )
        user.set_password(form.password.data)
        
        # Set legacy role based on role_id
        role = Role.query.get(form.role_id.data)
        if role:
            user.role = role.name.lower()
        
        db.session.add(user)
        db.session.commit()
        
        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='create',
            table_name='users',
            record_id=user.id,
            details=f'Created user: {user.username}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'User "{user.username}" created successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/user_form.html', form=form, user=None)


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('user.edit')
def user_edit(user_id):
    """Edit existing user"""
    user = User.query.get_or_404(user_id)
    form = UserForm(original_user=user, obj=user)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role_id = form.role_id.data
        user.is_active = form.is_active.data
        
        # Update password only if provided
        if form.password.data:
            user.set_password(form.password.data)
        
        # Update legacy role
        role = Role.query.get(form.role_id.data)
        if role:
            user.role = role.name.lower()
        
        db.session.commit()
        
        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='update',
            table_name='users',
            record_id=user.id,
            details=f'Updated user: {user.username}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'User "{user.username}" updated successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/user_form.html', form=form, user=user)


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@permission_required('user.delete')
def user_delete(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    
    # Prevent self-deletion
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin.users'))
    
    username = user.username
    
    # Log the action before deleting
    audit_log = AuditLog(
        user_id=current_user.id,
        action='delete',
        table_name='users',
        record_id=user.id,
        details=f'Deleted user: {username}'
    )
    db.session.add(audit_log)
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User "{username}" deleted successfully!', 'success')
    return redirect(url_for('admin.users'))


# Role Management Routes

@admin_bp.route('/roles')
@login_required
@permission_required('role.view')
def roles():
    """Role management"""
    roles = Role.query.order_by(Role.id).all()
    return render_template('admin/roles.html', roles=roles)


@admin_bp.route('/roles/add', methods=['GET', 'POST'])
@login_required
@permission_required('role.manage')
def role_add():
    """Add new role"""
    form = RoleForm()
    permissions = Permission.query.order_by(Permission.slug).all()
    
    if form.validate_on_submit():
        role = Role(
            name=form.name.data,
            description=form.description.data,
            is_system=False # Custom roles are not system
        )
        
        # Handle permissions
        selected_perms = request.form.getlist('permissions')
        if selected_perms:
            role.permissions = Permission.query.filter(Permission.id.in_(selected_perms)).all()
            
        db.session.add(role)
        db.session.commit()
        
        # Log
        audit_log = AuditLog(
            user_id=current_user.id,
            action='create',
            table_name='roles',
            record_id=role.id,
            details=f'Created role: {role.name}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'Role "{role.name}" created successfully!', 'success')
        return redirect(url_for('admin.roles'))
        
    return render_template('admin/role_form.html', form=form, role=None, permissions=permissions)


@admin_bp.route('/roles/<int:role_id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('role.manage')
def role_edit(role_id):
    """Edit existing role"""
    role = Role.query.get_or_404(role_id)
    form = RoleForm(obj=role)
    permissions = Permission.query.order_by(Permission.slug).all()
    
    if form.validate_on_submit():
        # Prevent editing name of system roles? Maybe allow description but warn on name.
        if role.is_system and role.name != form.name.data:
            flash('Cannot change name of system roles.', 'error')
            return render_template('admin/role_form.html', form=form, role=role, permissions=permissions)
            
        role.name = form.name.data
        role.description = form.description.data
        
        # Handle permissions
        selected_perms = request.form.getlist('permissions')
        # System roles might prevent removing critical permissions, but admin should be careful
        role.permissions = Permission.query.filter(Permission.id.in_(selected_perms)).all()
        
        db.session.commit()
        
        # Log
        audit_log = AuditLog(
            user_id=current_user.id,
            action='update',
            table_name='roles',
            record_id=role.id,
            details=f'Updated role: {role.name}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'Role "{role.name}" updated successfully!', 'success')
        return redirect(url_for('admin.roles'))
        
    return render_template('admin/role_form.html', form=form, role=role, permissions=permissions)


@admin_bp.route('/roles/<int:role_id>/delete', methods=['POST'])
@login_required
@permission_required('role.manage')
def role_delete(role_id):
    """Delete role"""
    role = Role.query.get_or_404(role_id)
    
    if role.is_system:
        flash('Cannot delete system role.', 'error')
        return redirect(url_for('admin.roles'))
        
    if role.users.count() > 0:
        flash('Cannot delete role assigned to users. Reassign them first.', 'error')
        return redirect(url_for('admin.roles'))
        
    role_name = role.name
    db.session.delete(role)
    db.session.commit()
    
    # Log
    audit_log = AuditLog(
        user_id=current_user.id,
        action='delete',
        table_name='roles',
        record_id=role.id,
        details=f'Deleted role: {role_name}'
    )
    db.session.add(audit_log)
    db.session.commit()
    
    flash(f'Role "{role_name}" deleted successfully!', 'success')
    return redirect(url_for('admin.roles'))


# Brand Management Routes

@admin_bp.route('/brands')
@login_required
@permission_required('brand.view')
def brands():
    """Brand management"""
    brands = Brand.query.order_by(Brand.name).all()
    return render_template('admin/brands.html', brands=brands)


@admin_bp.route('/brands/add', methods=['GET', 'POST'])
@login_required
@permission_required('brand.manage')
def brand_add():
    """Add new brand"""
    form = BrandForm()
    
    if form.validate_on_submit():
        brand = Brand(
            name=form.name.data,
            logo_url=form.logo_url.data
        )
        db.session.add(brand)
        db.session.commit()
        
        # Log
        audit_log = AuditLog(
            user_id=current_user.id,
            action='create',
            table_name='brands',
            record_id=brand.id,
            details=f'Created brand: {brand.name}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'Brand "{brand.name}" created successfully!', 'success')
        return redirect(url_for('admin.brands'))
        
    return render_template('admin/brand_form.html', form=form, brand=None)


@admin_bp.route('/brands/<int:brand_id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('brand.manage')
def brand_edit(brand_id):
    """Edit existing brand"""
    brand = Brand.query.get_or_404(brand_id)
    form = BrandForm(obj=brand)
    
    if form.validate_on_submit():
        brand.name = form.name.data
        brand.logo_url = form.logo_url.data
        db.session.commit()
        
        # Log
        audit_log = AuditLog(
            user_id=current_user.id,
            action='update',
            table_name='brands',
            record_id=brand.id,
            details=f'Updated brand: {brand.name}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'Brand "{brand.name}" updated successfully!', 'success')
        return redirect(url_for('admin.brands'))
        
    return render_template('admin/brand_form.html', form=form, brand=brand)


@admin_bp.route('/brands/<int:brand_id>/delete', methods=['POST'])
@login_required
@permission_required('brand.manage')
def brand_delete(brand_id):
    """Delete brand"""
    brand = Brand.query.get_or_404(brand_id)
    
    # Check if brand is attached to products
    if brand.products.count() > 0:
        flash(f'Cannot delete brand "{brand.name}" because it is associated with products.', 'error')
        return redirect(url_for('admin.brands'))
        
    brand_name = brand.name
    db.session.delete(brand)
    db.session.commit()
    
    # Log
    audit_log = AuditLog(
        user_id=current_user.id,
        action='delete',
        table_name='brands',
        record_id=brand.id,
        details=f'Deleted brand: {brand_name}'
    )
    db.session.add(audit_log)
    db.session.commit()
    
    flash(f'Brand "{brand_name}" deleted successfully!', 'success')
    return redirect(url_for('admin.brands'))


# ============================================================================
# STATUS MANAGEMENT ROUTES - Enable/Disable Products, Users, and Rules
# ============================================================================

@admin_bp.route('/products/<int:product_id>/toggle-status', methods=['POST', 'GET'])
@login_required
@permission_required('product.edit')
def product_toggle_status(product_id):
    """Toggle product active/inactive status"""
    product = Product.query.get_or_404(product_id)
    
    # Toggle the status
    product.is_active = not product.is_active
    db.session.commit()
    
    # Log the action
    status_text = 'activated' if product.is_active else 'deactivated'
    audit_log = AuditLog(
        user_id=current_user.id,
        action='status_update',
        table_name='products',
        record_id=product.id,
        details=f'{status_text.capitalize()} product: {product.name}'
    )
    db.session.add(audit_log)
    db.session.commit()
    
    status_text = 'activated' if product.is_active else 'deactivated'
    flash(f'Product "{product.name}" has been {status_text}!', 'success')
    
    # Return to referrer or products page
    return redirect(request.referrer or url_for('admin.products'))


@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST', 'GET'])
@login_required
@permission_required('user.edit')
def user_toggle_status(user_id):
    """Toggle user active/inactive status"""
    user = User.query.get_or_404(user_id)
    
    # Prevent deactivating current user
    if user.id == current_user.id:
        flash('You cannot deactivate your own account.', 'error')
        return redirect(request.referrer or url_for('admin.users'))
    
    # Toggle the status
    user.is_active = not user.is_active
    db.session.commit()
    
    # Log the action
    status_text = 'activated' if user.is_active else 'deactivated'
    audit_log = AuditLog(
        user_id=current_user.id,
        action='status_update',
        table_name='users',
        record_id=user.id,
        details=f'{status_text.capitalize()} user: {user.username}'
    )
    db.session.add(audit_log)
    db.session.commit()
    
    status_text = 'activated' if user.is_active else 'deactivated'
    flash(f'User "{user.username}" has been {status_text}!', 'success')
    
    # Return to referrer or users page
    return redirect(request.referrer or url_for('admin.users'))


@admin_bp.route('/rules/<int:rule_id>/toggle-status', methods=['POST', 'GET'])
@login_required
@permission_required('rule.manage')
def rule_toggle_status(rule_id):
    """Toggle rule active/inactive status"""
    rule = Rule.query.get_or_404(rule_id)
    
    # Toggle the status
    rule.is_active = not rule.is_active
    db.session.commit()
    
    # Log the action
    status_text = 'activated' if rule.is_active else 'deactivated'
    audit_log = AuditLog(
        user_id=current_user.id,
        action='status_update',
        table_name='rules',
        record_id=rule.id,
        details=f'{status_text.capitalize()} rule: {rule.name}'
    )
    db.session.add(audit_log)
    db.session.commit()
    
    status_text = 'activated' if rule.is_active else 'deactivated'
    flash(f'Rule "{rule.name}" has been {status_text}!', 'success')
    
    # Return to referrer or rules page
    return redirect(request.referrer or url_for('admin.rules'))
