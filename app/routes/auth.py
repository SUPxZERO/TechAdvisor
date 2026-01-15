from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.forms.auth_forms import LoginForm, RegisterForm
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            if user.is_active:
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                flash(f'Welcome back, {user.username}!', 'success')
                return redirect(next_page or url_for('admin.dashboard'))
            else:
                flash('Account is deactivated. Contact administrator.', 'error')
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('user.home'))


@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    """Register new admin/staff user (admin only)"""
    if not current_user.has_role('admin'):
        flash('Only administrators can create new users.', 'error')
        return redirect(url_for('admin.dashboard'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'User {user.username} created successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('auth/register.html', form=form)
