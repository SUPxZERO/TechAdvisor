from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SelectField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class RuleConditionForm(FlaskForm):
    """Sub-form for rule conditions"""
    class Meta:
        csrf = False  # Disable CSRF for sub-forms
    
    attribute = StringField('Attribute',
                          validators=[DataRequired(), Length(max=100)],
                          render_kw={'placeholder': 'e.g., budget, usage_type'})
    
    operator = SelectField('Operator',
                         choices=[
                             ('equals', 'Equals'),
                             ('not_equals', 'Not Equals'),
                             ('greater_than', 'Greater Than'),
                             ('less_than', 'Less Than'),
                             ('greater_equal', 'Greater or Equal'),
                             ('less_equal', 'Less or Equal'),
                             ('contains', 'Contains'),
                             ('in_range', 'In Range')
                         ],
                         validators=[DataRequired()])
    
    value = StringField('Value',
                       validators=[DataRequired(), Length(max=255)],
                       render_kw={'placeholder': 'e.g., gaming, 1000'})


class RuleForm(FlaskForm):
    """Form for creating and editing rules"""
    name = StringField('Rule Name',
                      validators=[DataRequired(), Length(min=3, max=200)],
                      render_kw={'placeholder': 'e.g., Gaming Laptop Recommendation'})
    
    description = TextAreaField('Description',
                               validators=[Optional(), Length(max=500)],
                               render_kw={'placeholder': 'Describe when this rule applies...', 'rows': 3})
    
    priority = IntegerField('Priority',
                          validators=[DataRequired(), NumberRange(min=1, max=100)],
                          render_kw={'placeholder': '1-100 (higher = more important)'})
    
    category_id = SelectField('Target Category',
                             coerce=int,
                             validators=[DataRequired()],
                             render_kw={'help': 'Category this rule recommends'})
    
    conclusion_type = SelectField('Conclusion Type',
                                 choices=[
                                     ('recommend_category', 'Recommend Category'),
                                     ('recommend_brand', 'Recommend Brand'),
                                     ('recommend_spec', 'Recommend Specification'),
                                     ('exclude_option', 'Exclude Option')
                                 ],
                                 validators=[DataRequired()])
    
    conclusion_value = StringField('Conclusion Value',
                                  validators=[Optional(), Length(max=255)],
                                  render_kw={'placeholder': 'e.g., laptop, gaming'})
    
    is_active = BooleanField('Active (enabled in recommendations)', default=True)
    
    submit = SubmitField('Save Rule')
    
    def __init__(self, *args, **kwargs):
        super(RuleForm, self).__init__(*args, **kwargs)
        # Populate category choices
        from app.models.product import Category
        self.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]


class SimpleRuleForm(FlaskForm):
    """Simplified rule form for quick rule creation"""
    name = StringField('Rule Name',
                      validators=[DataRequired(), Length(min=3, max=200)])
    
    description = TextAreaField('Description',
                               validators=[Optional(), Length(max=500)])
    
    priority = IntegerField('Priority (1-100)',
                          validators=[DataRequired(), NumberRange(min=1, max=100)],
                          default=50)
    
    is_active = BooleanField('Active', default=True)
    
    submit = SubmitField('Save Rule')
