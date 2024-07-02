from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    
    def validate_username(self, username_to_check): # the name of the function must be written like validate_<field> for the built in functions of flaskforms to work
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different username')
    
    def validate_email(self, email_to_check): # the name of the function must be written like validate_<field> for the built in functions of flaskforms to work
        email = User.query.filter_by(email_address=email_to_check.data).first()
        if email:
            raise ValidationError('Email address already exists. Please choose a different email address')
    
    username = StringField('User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField('Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password:', validators=[Length(6), DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField('Create Account')
    
class LoginForm(FlaskForm):
    username = StringField('User Name:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField('Purchase Item')

class SellItemForm(FlaskForm):
    submit = SubmitField('Sell Item')