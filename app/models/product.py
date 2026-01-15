from app import db
from datetime import datetime


class Brand(db.Model):
    """Brand model for product manufacturers"""
    __tablename__ = 'brands'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    logo_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    products = db.relationship('Product', backref='brand', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Brand {self.name}>'


class Category(db.Model):
    """Category model for product types (smartphone, laptop)"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic')
    rules = db.relationship('Rule', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    """Product model for smartphones and laptops"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    specifications = db.relationship('Specification', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand.name if self.brand else None,
            'category': self.category.name if self.category else None,
            'price': float(self.price),
            'image_url': self.image_url,
            'description': self.description,
            'specifications': {spec.spec_key: spec.spec_value for spec in self.specifications}
        }


class Specification(db.Model):
    """Specification model for product technical details"""
    __tablename__ = 'specifications'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    spec_key = db.Column(db.String(100), nullable=False)
    spec_value = db.Column(db.Text, nullable=False)
    
    # Composite index for faster lookups
    __table_args__ = (
        db.Index('idx_product_spec', 'product_id', 'spec_key'),
    )
    
    def __repr__(self):
        return f'<Specification {self.spec_key}: {self.spec_value}>'
