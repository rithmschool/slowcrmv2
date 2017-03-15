from project.users.forms import UserForm
from project.users.forms import LoginForm
from flask import Blueprint, redirect, render_template, request, flash, url_for, session, g
from project.models import Person
from project import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from project.persons.forms import PersonForm


persons_blueprint = Blueprint(
    'persons',
    __name__,
    template_folder = 'templates'
)


@persons_blueprint.route('/', methods=['GET', 'POST'])
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
    if request.method == 'PATCH':
        if form.validate():
            edit_person = Person.query.get(id)
            edit_person.email=request.form['email'],
            edit_person.phone=request.form['phone'],
            edit_person.name=request.form['name'],
            edit_person.title=request.form['title'],
            edit_person.description=request.form['description'],
            edit_person.slow_lp=form.data['slow_lp'],
            edit_person.archived=form.data['archived']
            db.session.add(edit_person)
            db.session.commit()
            flash("Succesfully edited profile")
            return redirect(url_for('persons.index'))
        flash('Please fill in all required fields')
        return render_template('person')
    persons = Person.query.filter_by(archived=False)
    return render_template('persons/index.html', persons=persons)

@persons_blueprint.route('/new')
def new():
    form = PersonForm(request.form)
    return render_template('persons/new.html', form=form)

@persons_blueprint.route('/<int:id>', methods=["GET","POST","PATCH"])
def show(id):
    person = Person.query.get(id)
    return render_template('persons/show.html', person=person)


@persons_blueprint.route('/<int:id>/edit', methods=["GET"])
def edit(id):
    edit_person = Person.query.get(id)
    form = PersonForm(obj = edit_person)
    return render_template('persons/edit.html', form=form, person=edit_person)
