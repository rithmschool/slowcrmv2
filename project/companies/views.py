from flask import Blueprint, redirect, render_template, flash, url_for, request
from project import db
from project.companies.forms import CompanyForm, EditCompanyForm, TagForm
from project.models import Company, Tag, Taggable, Followable
from flask_login import login_required, current_user
from project.users.views import get_links, get_pipes_dollars_tags_tuples
from sqlalchemy import asc
from flask import json


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
    taggables = Taggable.query.filter_by(taggable_id=id, taggable_type='company').all()
    followable = bool(Followable.query.filter_by(followable_id=id, user_id=current_user.id).first())
    formatted_entries = [{
        'content': get_links(entry.content, get_pipes_dollars_tags_tuples(entry.content)),
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
    return render_template('companies/show.html', company=company, form = TagForm(), entries=reversed(formatted_entries),
                           taggables=taggables, Tag=Tag, followable=followable)

@companies_blueprint.route('/<int:id>/edit')
@login_required
def edit(id):
    company = Company.query.get(id)
    form = EditCompanyForm(obj=company)
    return render_template('companies/edit.html', form=form, company=company)

@companies_blueprint.route('/<int:id>/archive')
@login_required
def archive(id):
    company = Company.query.get(id)
    if company.archived == False:
        company.archived = True
    else:
        company.archived = False
    db.session.add(company)
    db.session.commit()
    return redirect(url_for('companies.index'))

@companies_blueprint.route('/<int:id>/tags', methods=['POST'])
@login_required
def add_tag(id):
    form = TagForm(request.form)
    if form.validate():
        tag_text = request.form['tag']
        tag_exists = Tag.query.filter_by(text=tag_text).first()
        if(not tag_exists):
            tag = Tag(tag_text)
            db.session.add(tag)
            db.session.commit()
            taggable = Taggable(id, tag.id, 'company')
            db.session.add(taggable)
            db.session.commit()
            return redirect(url_for('companies.show', id=id))
        else:
            tag_check = Taggable.query.filter_by(tag_id=tag_exists.id,taggable_id=id,taggable_type='company').first()
            if (not tag_check):
                tag = Tag.query.filter_by(text=tag_text).first()
                taggable = Taggable(id, tag.id, 'company')
                db.session.add(taggable)
                db.session.commit()
                return redirect(url_for('companies.show', id=id))
            else:
                flash("This company is already tagged with '{}'".format(tag_text))
                return redirect(url_for('companies.show', id=id))

@companies_blueprint.route('/archived', methods=['GET'])
@login_required
def show_archived():
    companies = Company.query.filter_by(archived=True).order_by(Company.name)
    return render_template('companies/archived.html', companies=companies)

@companies_blueprint.route('/<int:id>/follow', methods=['GET'])
@login_required
def follow(id):
    user_id = current_user.id
    followable = Followable.query.filter_by(followable_id=id, user_id=current_user.id).first()
    if not bool(followable):
        followable = Followable(id, user_id, 'company')
        db.session.add(followable)
        db.session.commit()
    else:
        db.session.delete(followable)
        db.session.commit()
    return redirect(url_for('companies.show', id=id))
