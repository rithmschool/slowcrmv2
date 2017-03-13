from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField

class UserForm(FlaskForm):
	username = StringField('Username', [validators.DataRequired()])
	password = PasswordField('password', [validators.DataRequired()])
	email = StringField('Email', [validators.DataRequired()])
	phone = StringField('Phone', [validators.DataRequired()])
	


class LoginForm(FlaskForm):
	username = StringField('Username', [validators.DataRequired()])
	password = PasswordField('password', [validators.DataRequired()])



