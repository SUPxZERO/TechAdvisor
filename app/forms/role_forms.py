from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models.role import Permission

class RoleForm(FlaskForm):
    """Form to add/edit roles"""
    name = StringField('Role Name', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description', validators=[Length(max=255)])
    is_system = BooleanField('System Role', default=False, render_kw={'readonly': True})
    
    # Permissions will be handled via a custom field or list in the template, 
    # but we can verify them in the route or use SelectMultipleField if we want simple multiselect.
    # For better UX, we usually iterate checkboxes in template. 
    # But SelectMultipleField is easier for standard validation.
    # permissions = SelectMultipleField('Permissions', coerce=int)

    submit = SubmitField('Save Role')
