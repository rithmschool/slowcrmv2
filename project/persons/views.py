from project.users.forms import UserForm
from flask import Blueprint, redirect, render_template, request, flash, url_for, session, g
from project.models import Person, Tag, Taggable
from project import db
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from project.persons.forms import PersonForm, EditPersonForm
from project.companies.forms import TagForm
from project.users.views import get_links, get_pipes_dollars_tags_tuples


persons_blueprint = Blueprint(
    'persons',
    __name__,
    template_folder = 'templates'
)

@persons_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():

    form = PersonForm(request.form)
    if request.method == 'POST':
        if form.validate():
            new_person = Person(
            email=request.form['email'],
            phone=request.form['phone'],
            name=request.form['name'],
            title=request.form['title'],
            description=request.form['description'],
            slow_lp=form.data['slow_lp'],
            archived=form.data['archived'])
            db.session.add(new_person)
            db.session.commit()
            flash("Succesfully added new person")
            return redirect(url_for('persons.index'))
        flash('Please fill in all required fields')
        return render_template('persons/new.html',form=form)
    persons = Person.query.filter_by(archived=False).order_by(Person.name)
    return render_template('persons/index.html', persons=persons)

@persons_blueprint.route('/new')
@login_required
def new():
    form = PersonForm(request.form)
    term = ''
    if 'term' in request.args:
        term = request.args['term']
    return render_template('persons/new.html', form=form, term=term)

@persons_blueprint.route('/<int:id>', methods=["GET","POST","PATCH"])
@login_required
def show(id):
    person = Person.query.get(id)
    form = PersonForm(request.form)
    entries = Person.query.get_or_404(id).entries
    taggables = Taggable.query.filter_by(taggable_id=id, taggable_type='person').all()
    formatted_entries = [{
        'content': get_links(entry.content, get_pipes_dollars_tags_tuples(entry.content)),
        'entry_id': entry.id,
        'created_at': entry.created_at,
        'updated_at': entry.updated_at
    } for entry in entries]
    if request.method == b'PATCH':
        form=EditPersonForm(request.form)
        if form.validate():
            person.email=request.form['email']
            person.phone=request.form['phone']
            person.title=request.form['title']
            person.description=request.form['description']
            person.slow_lp=form.slow_lp.data
            person.archived=form.archived.data
            db.session.add(person)
            db.session.commit()
            flash("Succesfully edited profile")
            return redirect(url_for('persons.show', id=person.id))
        flash('Please fill in all required fields')
        return render_template('persons/edit.html',form=form,person=person)
    return render_template('persons/show.html', person=person, form=TagForm(), entries=reversed(formatted_entries), taggables=taggables, Tag=Tag)


@persons_blueprint.route('/<int:id>/edit', methods=["GET","PATCH"])
@login_required
def edit(id):
    edit_person = Person.query.get(id)
    form = EditPersonForm(obj = edit_person)
    return render_template('persons/edit.html', form=form, person=edit_person)

@persons_blueprint.route('/<int:id>/tags', methods=['POST'])
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
            taggable = Taggable(id, tag.id, 'person')
            db.session.add(taggable)
            db.session.commit()
            return redirect(url_for('persons.show', id=id))
        else:
            tag_check = Taggable.query.filter_by(tag_id=tag_exists.id,taggable_id=id,taggable_type='person').first()
            if (not tag_check):
                tag = Tag.query.filter_by(text=tag_text).first()
                taggable = Taggable(id, tag.id, 'person')
                db.session.add(taggable)
                db.session.commit()
                return redirect(url_for('persons.show', id=id))
            else:
                flash("This person is already tagged with '{}'".format(tag_text))
                return redirect(url_for('persons.show', id=id))

