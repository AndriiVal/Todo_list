from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from webapp.models import Users

class LoginForm(FlaskForm):
    username = StringField('Login', validators=[Length(min=1, max=30)])
    password = PasswordField('Password', validators=[DataRequired('The entered data is not correct')])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired('The entered data is not correct')])
    password = PasswordField('Password', validators=[DataRequired('The entered data is not correct')])
    password2 = PasswordField('Repeat password', validators=[DataRequired('The entered data is not correct'), EqualTo('password',message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if Users.query.filter_by(username=username.data).first():
            raise ValidationError('Username already in use.')
