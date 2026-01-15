from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DecimalField, BooleanField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError
from app.models.product import Brand, Category


class ProductForm(FlaskForm):
    """Form for creating and editing products"""
    name = StringField('Product Name', 
                      validators=[DataRequired(), Length(min=3, max=255)],
                      render_kw={'placeholder': 'e.g., iPhone 15 Pro Max 256GB'})
    
    brand_id = SelectField('Brand', 
                          coerce=int,
                          validators=[DataRequired()])
    
    category_id = SelectField('Category', 
                             coerce=int,
                             validators=[DataRequired()])
    
    price = DecimalField('Price (USD)', 
                        validators=[DataRequired(), NumberRange(min=0, max=99999.99)],
                        render_kw={'placeholder': '999.99', 'step': '0.01'})
    
    description = TextAreaField('Description',
                               validators=[Optional(), Length(max=1000)],
                               render_kw={'placeholder': 'Detailed product description...', 'rows': 4})
    
    image_url = StringField('Image URL',
                           validators=[Optional(), Length(max=500)],
                           render_kw={'placeholder': 'https://example.com/image.jpg'})
    
    is_active = BooleanField('Active (visible to users)', default=True)
    
    submit = SubmitField('Save Product')
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Populate brand choices
        self.brand_id.choices = [(b.id, b.name) for b in Brand.query.order_by(Brand.name).all()]
        # Populate category choices
        self.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]


class SpecificationForm(FlaskForm):
    """Sub-form for product specifications"""
    spec_key = StringField('Specification Name',
                          validators=[DataRequired(), Length(max=100)],
                          render_kw={'placeholder': 'e.g., Processor'})
    
    spec_value = StringField('Value',
                            validators=[DataRequired(), Length(max=255)],
                            render_kw={'placeholder': 'e.g., A17 Pro Chip'})


class ProductWithSpecsForm(ProductForm):
    """Extended product form with specifications"""
    # Specifications will be handled separately in the view
    pass


class BrandForm(FlaskForm):
    """Form for creating and editing brands"""
    name = StringField('Brand Name',
                      validators=[DataRequired(), Length(min=2, max=100)],
                      render_kw={'placeholder': 'e.g., Apple'})
    
    logo_url = StringField('Logo URL',
                          validators=[Optional(), Length(max=255)],
                          render_kw={'placeholder': 'https://example.com/logo.png'})
    
    submit = SubmitField('Save Brand')
    
    def validate_name(self, name):
        """Check if brand name already exists"""
        brand = Brand.query.filter_by(name=name.data).first()
        if brand and (not hasattr(self, 'brand_id') or brand.id != self.brand_id):
            raise ValidationError('Brand name already exists.')
