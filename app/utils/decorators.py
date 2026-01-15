from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user

def permission_required(permission_slug):
    """Decorator to check for specific permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
                
            if not current_user.has_permission(permission_slug):
                flash(f'Permission denied: You need "{permission_slug}" to access this page.', 'error')
                # If referrer exists, go back, else dashboard
                return redirect(url_for('admin.dashboard'))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Legacy admin required decorator - eventually replace with permissions"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.has_role('Admin'): # Use has_role for stricter check? Or has_permission('admin_access')
             # For legacy compatibility, check explicit Role OR 'admin_access' perm if we had it.
             # But init_rbac gave Admin all permissions.
             # Let's keep checking Role for "Super Admin" areas for now.
            if not current_user.has_role('Admin'):
                 flash('Admin access required', 'error')
                 return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
    return decorated_function

def staff_required(f):
    """Legacy staff required - maps to basic access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Allow if Admin OR Staff
        if not current_user.is_authenticated:
             return redirect(url_for('auth.login'))
             
        # Check if user has ANY staff-like permission or role
        if current_user.has_role('Admin') or current_user.has_role('Staff'):
            return f(*args, **kwargs)
            
        flash('Staff access required', 'error')
        return redirect(url_for('auth.login'))
    return decorated_function
