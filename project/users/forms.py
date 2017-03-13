from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField

class UserForm(FlaskForm):
	email = StringField('Email', [validators.DataRequired()])
	name = StringField('Name', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired()])
	phone = StringField('Phone', [validators.DataRequired()])
	


class LoginForm(FlaskForm):
	email = StringField('Email', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired()])



