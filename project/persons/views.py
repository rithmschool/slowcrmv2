from project.users.forms import UserForm
from flask import Blueprint, redirect, render_template, request, flash, url_for, session, g
from project.models import Person
from project import db
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from project.persons.forms import PersonForm


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
    persons = Person.query.filter_by(archived=False)
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
    if request.method == b'PATCH':
        if form.validate():
            person.email=request.form['email']
            person.phone=request.form['phone']
            person.name=request.form['name']
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
    return render_template('persons/show.html', person=person)


@persons_blueprint.route('/<int:id>/edit', methods=["GET","PATCH"])
@login_required
def edit(id):
    edit_person = Person.query.get(id)
    form = PersonForm(obj = edit_person)
    return render_template('persons/edit.html', form=form, person=edit_person)
