from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User


class LoginForm(FlaskForm):
    """Login form for admin and staff users"""
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=3, max=50)],
                          render_kw={'placeholder': 'Enter your username'})
    
    password = PasswordField('Password', 
                            validators=[DataRequired()],
                            render_kw={'placeholder': 'Enter your password'})
    
    remember_me = BooleanField('Remember Me')
    
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    """Registration form for creating new admin/staff users"""
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=3, max=50)],
                          render_kw={'placeholder': 'Choose a username'})
    
    email = StringField('Email', 
                       validators=[DataRequired(), Email(), Length(max=100)],
                       render_kw={'placeholder': 'Enter email address'})
    
    password = PasswordField('Password', 
                            validators=[
                                DataRequired(), 
                                Length(min=8, message='Password must be at least 8 characters')
                            ],
                            render_kw={'placeholder': 'Create a strong password'})
    
    password_confirm = PasswordField('Confirm Password',
                                    validators=[
                                        DataRequired(),
                                        EqualTo('password', message='Passwords must match')
                                    ],
                                    render_kw={'placeholder': 'Confirm your password'})
    
    role = SelectField('Role',
                      choices=[('staff', 'Staff'), ('admin', 'Admin')],
                      validators=[DataRequired()])
    
    submit = SubmitField('Create User')
    
    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose another one.')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use another one.')
