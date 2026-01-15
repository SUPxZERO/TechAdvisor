from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional

class BrandForm(FlaskForm):
    """Form to add/edit brands"""
    name = StringField('Brand Name', validators=[DataRequired(), Length(max=100)])
    logo_url = StringField('Logo URL', validators=[Optional(), URL(), Length(max=255)])
    submit = SubmitField('Save Brand')
