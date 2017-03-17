from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, BooleanField

class PersonForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    email = StringField('Email', [validators.email()])
    phone = StringField('Phone', [validators.Length(max=13, min=10)])
    title = StringField('Title' , [validators.Length(max=20)])
    description = StringField('Description')
    slow_lp = BooleanField('Slow_lp')
    archived = BooleanField('Archived?')
