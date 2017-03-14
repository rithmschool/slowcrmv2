from project.users.forms import UserForm
from project.users.forms import LoginForm
from flask import Blueprint, redirect, render_template, request, flash, url_for, session, g
from project.users.models import User, Person
from project import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError


users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder = 'templates'
)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            found_user = User.query.filter_by(email = form.email.data).first()
            if found_user:
                authenticated_user = bcrypt.check_password_hash(found_user.password, request.form['password'])
                if authenticated_user:
                    login_user(found_user)
                    name = found_user.name
                    first_name = name[:name.find(' '):]
                    flash('Welcome, {}').format(first_name)
                    return redirect(url_for('users.home'))
        flash('Invalid Credentials')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)
