from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, BooleanField

class PersonForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired()])
    phone = StringField('Phone', [validators.DataRequired()])
    name = StringField('Name', [validators.DataRequired()])
    title = StringField('Title' , [validators.Length(max=20)])
    description = StringField('Description')
    slow_lp = BooleanField('Slow_lp')
