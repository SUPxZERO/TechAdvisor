from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
from app.models.user import User
from app.models.role import Role


class UserForm(FlaskForm):
    """Form for adding/editing users"""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=50, message='Username must be 3-50 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Please enter a valid email address'),
        Length(max=100)
    ])
    password = PasswordField('Password', validators=[
        Optional(),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    role_id = SelectField('Role', coerce=int, validators=[DataRequired()])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save User')
    
    def __init__(self, original_user=None, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.original_user = original_user
        # Populate role choices
        self.role_id.choices = [(r.id, r.name) for r in Role.query.order_by(Role.name).all()]
    
    def validate_username(self, field):
        """Check if username is already taken"""
        user = User.query.filter_by(username=field.data).first()
        if user:
            # If editing, allow same username for current user
            if self.original_user and self.original_user.id == user.id:
                return
            raise ValidationError('Username already exists.')
    
    def validate_email(self, field):
        """Check if email is already taken"""
        user = User.query.filter_by(email=field.data).first()
        if user:
            # If editing, allow same email for current user
            if self.original_user and self.original_user.id == user.id:
                return
            raise ValidationError('Email already registered.')
