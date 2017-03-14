from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, BooleanField, TextAreaField

class UserForm(FlaskForm):
	email = StringField('Email', [validators.DataRequired()])
	name = StringField('Name', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired()])
	phone = StringField('Phone', [validators.DataRequired()])
	


class LoginForm(FlaskForm):
	email = StringField('Email', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired()])





class PersonForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired()])
    phone = StringField('Phone', [validators.DataRequired()])
    name = StringField('Name', [validators.DataRequired()])
    title = StringField('Title' , [validators.Length(max=20)])
    description = StringField('Description')
    slow_lp = BooleanField('Slow_lp')


class EntryForm(FlaskForm):
    post_message = TextAreaField('Send an update to partners $company |person and a *tag')
