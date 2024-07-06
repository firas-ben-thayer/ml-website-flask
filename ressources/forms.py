from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Optional
from ressources.models import User, Exercise

class CreateUserForm(FlaskForm):
    username = StringField('User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField('Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    authority = SelectField('Authority:', choices=[('0', 'Admin'), ('1', 'Teacher'), ('2', 'Student')], validators=[DataRequired()])
    create = SubmitField('Create User')

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different username')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email_address=email_to_check.data).first()
        if email:
            raise ValidationError('Email address already exists. Please choose a different email address')

class EditUserForm(FlaskForm):
    username = StringField('User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField('Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password:', validators=[Optional(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[Optional(), EqualTo('password1')])
    authority = SelectField('Authority:', choices=[('0', 'Admin'), ('1', 'Teacher'), ('2', 'Student')], validators=[DataRequired()])
    edit = SubmitField('Update User')

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(EditUserForm, self).__init__(*args, **kwargs)

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user and user.id != self.current_user.id:
            raise ValidationError('Username already exists. Please choose a different username')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email_address=email_to_check.data).first()
        if email and email.id != self.current_user.id:
            raise ValidationError('Email address already exists. Please choose a different email address')

    
class LoginForm(FlaskForm):
    username = StringField('User Name:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class ExerciseForm(FlaskForm):
    def validate_exercise_name(self, name_to_check):
        exercise = Exercise.query.filter_by(name=name_to_check.data).first()
        if exercise:
            raise ValidationError('Exercise name already exists. Please choose another name')
    
    exercise_name = StringField('Exercise name:', validators=[Length(min=2, max=30), DataRequired()])
    subject = StringField('Subject:', validators=[Length(min=2, max=60), DataRequired()])
    description = StringField('Description:', validators=[Length(min=2, max=1024), DataRequired()])
    content = TextAreaField('Content', validators=[Length(min=2), DataRequired()])
    create = SubmitField('Create Exercise')
    edit = SubmitField('Update Exercise')
