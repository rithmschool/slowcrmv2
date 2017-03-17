from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, BooleanField

class PersonForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=2, max=25)])
    email = StringField('Email', [validators.email()])
    phone = StringField('Phone', [validators.Length(min=10, max=20)])
    title = StringField('Title' , [validators.Length(max=20)])
    description = StringField('Description')
    slow_lp = BooleanField('Slow_lp')
    archived = BooleanField('Archived?')
