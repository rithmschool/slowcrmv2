from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, BooleanField, TextAreaField

class UserForm(FlaskForm):
    email = StringField('Email', [validators.email()])
    name = StringField('Name', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    confirmpassword = PasswordField('Confirm Password', [validators.DataRequired()])
    phone = StringField('Phone', [validators.DataRequired()])

class InviteForm(FlaskForm):
    email = StringField('Email', [validators.email()])
    name = StringField('Name', [validators.DataRequired()])

class LoginForm(FlaskForm):
	email = StringField('Email', [validators.email()])
	password = PasswordField('Password', [validators.DataRequired()])

class PersonForm(FlaskForm):
    email = StringField('Email', [validators.email()])
    phone = StringField('Phone', [validators.DataRequired()])
    name = StringField('Name', [validators.DataRequired()])
    title = StringField('Title' , [validators.Length(max=20)])
    description = StringField('Description')
    slow_lp = BooleanField('Slow_lp')


class EditUserForm(FlaskForm):
    email = StringField('Email', [validators.email()])
    name = StringField('Name', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    phone = StringField('Phone', [validators.DataRequired()])    

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', [validators.email()])

class RecoverPasswordForm(FlaskForm):
    password = PasswordField('Password', [validators.DataRequired()])
    confirmpassword = PasswordField('Confirm Password', [validators.DataRequired()])

class EditPasswordForm(FlaskForm):
    newpassword = PasswordField('New Password', [validators.DataRequired()])
    confirmpassword = PasswordField('Confirm New Password', [validators.DataRequired()])
    currentpassword = PasswordField('Current Password', [validators.DataRequired()])

