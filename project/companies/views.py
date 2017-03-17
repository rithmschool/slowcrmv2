from flask import Blueprint, redirect, render_template, flash, url_for, request
from project import db
from project.companies.forms import CompanyForm
from project.models import Company
from flask_login import login_required

companies_blueprint = Blueprint(
    'companies',
    __name__,
    template_folder='templates'
    )

@companies_blueprint.route('/', methods=['GET','POST'])
def index():
    companies = Company.query.filter_by(archived=False)
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
def new():
    form = CompanyForm(request.form)
    return render_template('companies/new.html', form=form)

@companies_blueprint.route('/<int:id>', methods=['GET','PATCH'])
def show(id):
    company = Company.query.get(id)
    form = CompanyForm(request.form)
    if request.method == b'PATCH':
        if form.validate():
            company.name=request.form['name']
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
        return render_template('companies/new.html',form=form)
    return render_template('companies/show.html', company=company)

@companies_blueprint.route('/<int:id>/edit')
def edit(id):
    company = Company.query.get(id)
    form = CompanyForm(obj=company)
    return render_template('companies/edit.html', form=form, company=company)
