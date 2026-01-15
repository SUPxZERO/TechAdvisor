from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length


class RecommendationForm(FlaskForm):
    """Form for collecting user preferences for product recommendations"""
    
    category = SelectField('What are you looking for?',
                          choices=[
                              ('smartphone', 'Smartphone'),
                              ('laptop', 'Laptop')
                          ],
                          validators=[DataRequired()])
    
    budget = IntegerField('What is your budget? (USD)',
                         validators=[DataRequired(), NumberRange(min=100, max=10000)],
                         render_kw={'placeholder': 'e.g., 1000'})
    
    usage_type = SelectField('Primary Usage',
                            choices=[
                                ('gaming', 'Gaming'),
                                ('work', 'Professional/Business'),
                                ('study', 'Education/Study'),
                                ('general', 'General/Everyday Use'),
                                ('creative', 'Content Creation')
                            ],
                            validators=[DataRequired()])
    
    preferred_brand = StringField('Preferred Brand (Optional)',
                                 validators=[Optional(), Length(max=50)],
                                 render_kw={'placeholder': 'e.g., Apple, Samsung, Dell'})
    
    additional_notes = TextAreaField('Any specific requirements?',
                                    validators=[Optional(), Length(max=500)],
                                    render_kw={'placeholder': 'e.g., Need long battery life, prefer lightweight...', 'rows': 3})
    
    submit = SubmitField('Get Recommendations')
