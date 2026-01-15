from app import db
from datetime import datetime

# Association table for Role-Permission Many-to-Many relationship
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

class Permission(db.Model):
    """Permission model for granular access control"""
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False) # Human readable name
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True) # Code identifier (e.g. 'product.create')
    description = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f'<Permission {self.slug}>'

class Role(db.Model):
    """Role model for grouping permissions"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    is_system = db.Column(db.Boolean, default=False) # System roles cannot be deleted (e.g. Admin)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    permissions = db.relationship('Permission', secondary=role_permissions, lazy='subquery',
        backref=db.backref('roles', lazy=True))
    users = db.relationship('User', backref='role_obj', lazy='dynamic')
    
    def has_permission(self, perm_slug):
        """Check if role has specific permission"""
        return any(p.slug == perm_slug for p in self.permissions)
        
    def __repr__(self):
        return f'<Role {self.name}>'
