from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, BooleanField

class PersonForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    email = StringField('Email')
    phone = StringField('Phone')
    title = StringField('Title')
    description = StringField('Description')
    slow_lp = BooleanField('Slow_lp')
    archived = BooleanField('Archived?')
