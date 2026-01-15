from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    """User model for admin and staff accounts"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'staff'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # RBAC Fields
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True) # Nullable for migration
    
    # Relationships
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    # role_obj relationship is defined in Role model (backref)
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def current_role(self):
        """Get role name (handle legacy enum vs new relation)"""
        if self.role_obj:
            return self.role_obj.name
        # Fallback to legacy role column if role_id is not set
        return self.role

    def has_role(self, role_name):
        """Check if user has specific role"""
        # Check new RBAC system first
        if self.role_obj:
            return self.role_obj.name == role_name
        # Fallback to legacy
        return self.role == role_name
        
    def has_permission(self, perm_slug):
        """Check if user has specific permission"""
        if not self.role_obj:
            # Legacy fallback: admin gets everything, staff gets limited
            if self.role == 'admin':
                return True
            if self.role == 'staff':
                # Define legacy staff permissions map if needed, or just return False for critical stuff
                # For now, let's assume legacy staff has basic access logic handled by decorators
                return False 
            return False
            
        return self.role_obj.has_permission(perm_slug)
    
    def __repr__(self):
        return f'<User {self.username}>'


class AuditLog(db.Model):
    """Audit log for tracking system changes"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    table_name = db.Column(db.String(50), nullable=True)
    record_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<AuditLog {self.action} by User {self.user_id}>'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))
