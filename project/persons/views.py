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


@persons_blueprint.route('/persons', methods=['GET, POST'])
def person_index():
    form = PersonForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_person = Person(
            email=request.form['email'],
            phone=request.form['phone'],
            name=request.form['name'],
            title=request.form['title'],
            description=request.form['description'],
            slow_lp=request.form['slow_lp']
                )
            db.session.add(new_person)
            db.session.commit()
            flash("Succesfully added new person")
            return redirect(url_for('users.index'))
        flash('Please fill in all required fields')
        return render_template('login.html', form=form)
