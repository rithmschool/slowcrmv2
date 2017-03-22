from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, validators

class CompanyForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired()])
    description = StringField('Description')
    url = StringField('URL')
    logo_url = StringField('Logo URL')
    partner_lead = StringField('Partner Lead')
    ops_lead = StringField('Operations Lead')
    source = StringField('Source')
    round = StringField('Round')
    archived = BooleanField('Archived?')


class EditCompanyForm(FlaskForm):
    description = StringField('Description')
    url = StringField('URL')
    logo_url = StringField('Logo URL')
    partner_lead = StringField('Partner Lead')
    ops_lead = StringField('Operations Lead')
    source = StringField('Source')
    round = StringField('Round')
    archived = BooleanField('Archived?')    
