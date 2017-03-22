from flask import Blueprint, redirect, render_template, flash, url_for, request
from project import db
from project.companies.forms import CompanyForm, EditCompanyForm
from project.models import Company
from flask_login import login_required
from project.users.views import get_links, get_pipes_dollars_tuples

companies_blueprint = Blueprint(
    'companies',
    __name__,
    template_folder='templates'
    )

@companies_blueprint.route('/', methods=['GET','POST'])
@login_required
def index():
    companies = Company.query.filter_by(archived=False).order_by(Company.name)
    form = CompanyForm(request.form)
    if request.method == 'POST':
        if form.validate():
            new_company = Company(
            name=request.form['name'],
            description=request.form['description'],
            url=request.form['url'],
            logo_url=request.form['logo_url'],
            partner_lead=request.form['partner_lead'],
            ops_lead=request.form['ops_lead'],
            source=request.form['source'],
            round=request.form['round'],
            archived=form.data['archived']
            )
            db.session.add(new_company)
            db.session.commit()
            flash("Succesfully added new company")
            return redirect(url_for('companies.index'))
        return render_template('companies/new.html',form=form)
    return render_template('companies/index.html', companies=companies)

@companies_blueprint.route('/new')
@login_required
def new():
    form = CompanyForm(request.form)
    term = ''
    if 'term' in request.args:
        term = request.args['term']
    return render_template('companies/new.html', form=form, term=term)

@companies_blueprint.route('/<int:id>', methods=['GET','PATCH'])
@login_required
def show(id):
    company = Company.query.get(id)
    entries = Company.query.get(id).entries
    formatted_entries = [{
        'content': get_links(entry.content, get_pipes_dollars_tuples(entry.content)),
        'entry_id': entry.id,
        'created_at': entry.created_at,
        'updated_at': entry.updated_at
    } for entry in entries]
    if request.method == b'PATCH':
        form = EditCompanyForm(request.form)
        if form.validate():
            company.description=request.form['description']
            company.url=request.form['url']
            company.logo_url=request.form['logo_url']
            company.partner_lead=request.form['partner_lead']
            company.ops_lead=request.form['ops_lead']
            company.source=request.form['source']
            company.round=request.form['round']
            company.archived=form.archived.data
            db.session.add(company)
            db.session.commit()
            flash("Succesfully edited company")
            return redirect(url_for('companies.show', id=company.id))
        return render_template('companies/edit.html',form=form)
    return render_template('companies/show.html', company=company, entries=reversed(formatted_entries))

@companies_blueprint.route('/<int:id>/edit')
@login_required
def edit(id):
    company = Company.query.get(id)
    form = EditCompanyForm(obj=company)
    return render_template('companies/edit.html', form=form, company=company)
