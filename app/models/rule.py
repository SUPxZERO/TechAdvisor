from app import db
from datetime import datetime


class Rule(db.Model):
    """Rule model for expert system inference rules"""
    __tablename__ = 'rules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    priority = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    conditions = db.relationship('RuleCondition', backref='rule', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Rule {self.name}>'
    
    def to_dict(self):
        """Convert rule to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category.name if self.category else None,
            'priority': self.priority,
            'is_active': self.is_active,
            'conditions': [condition.to_dict() for condition in self.conditions]
        }


class RuleCondition(db.Model):
    """Rule condition model for expert system logic"""
    __tablename__ = 'rule_conditions'
    
    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('rules.id'), nullable=False)
    condition_type = db.Column(db.String(50), nullable=False)  # budget, usage, brand, etc.
    condition_key = db.Column(db.String(100), nullable=False)
    operator = db.Column(db.String(20), nullable=False)  # ==, !=, <, >, <=, >=, in, contains
    condition_value = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<RuleCondition {self.condition_key} {self.operator} {self.condition_value}>'
    
    def to_dict(self):
        """Convert condition to dictionary"""
        return {
            'id': self.id,
            'condition_type': self.condition_type,
            'condition_key': self.condition_key,
            'operator': self.operator,
            'condition_value': self.condition_value
        }
