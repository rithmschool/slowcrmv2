from project.users.forms import UserForm, LoginForm, InviteForm
from flask import Blueprint, redirect, render_template, request, flash, url_for, session, g, jsonify
from project.models import User, Person, Entry
from project import db, bcrypt, mail
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from flask_mail import Message 
from project.users.token import generate_confirmation_token, confirm_token
from datetime import datetime
from flask import json
from werkzeug.datastructures import ImmutableMultiDict # for converting JSON to ImmutableMultiDict 

def send_token(subject, html, name, email, confirm_url):
    msg = Message(subject, sender="noreply.slowcrm@gmail.com", recipients=[email])
    msg.html = render_template(html, name = name, confirm_url = confirm_url)
    mail.send(msg)

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder = 'templates'
)

@users_blueprint.route('/home', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return render_template('users/home.html')
    return redirect(url_for('users.login'))

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            found_user = User.query.filter_by(email = form.email.data).first()
            if found_user:
                authenticated_user = bcrypt.check_password_hash(found_user.password, request.form['password'])
                if authenticated_user:
                    login_user(found_user)
                    return redirect(url_for('users.home'))
        flash('Invalid Credentials')
        return render_template('users/login.html', form=form)
    return render_template('users/login.html', form=form)


@users_blueprint.route('/invite', methods=['POST'])
@login_required
def invite():
    # WTForms needs an ImmutableMultiDict - we have to convert a dict to that below
    form = InviteForm(ImmutableMultiDict(request.get_json()))
    if form.validate():
        email = request.get_json().get('email')
        name = request.get_json().get('name')
        token = generate_confirmation_token(email)
        confirm_url = url_for('users.confirm_email', token=token, _external=True)
        new_user = User(email,name,'temppass','',True,False)
        db.session.add(new_user)
        db.session.commit()
        send_token("You Have Been Invited To Join Slow CRM", "users/new_user.html", name, email, confirm_url)
        return jsonify('Invite Sent'), 200
    else: 
        return jsonify("Missing form info"), 422       

@users_blueprint.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('Your confirmation link has expired or is invalid, please ask admin to resend invite.', 'danger')
        return redirect(url_for('users.login'))
    found_user = User.query.filter_by(email=email).first_or_404()
    if found_user.confirmed:
        flash('Account already confirmed. Please login or reset password', 'success')
        return redirect(url_for('users.login'))
    else:   
        found_user.confirmed = True
        found_user.updated_at = datetime.now()
        db.session.add(found_user)
        db.session.commit()
        login_user(found_user)
        return render_template('users/edit.html', form=UserForm(), user=found_user)

@users_blueprint.route('/<int:id>/edit', methods=['GET','PATCH'])
@login_required
def edit(id):
    if id == current_user.id:
        found_user = User.query.get(id)
        if request.method ==b"PATCH":
            form = UserForm(request.form)
            if form.validate():
                if request.form['password'] == request.form['confirmpassword']:
                    flash('You have successfully updated your user info!', 'success')
                    found_user.name = request.form['name']
                    found_user.email = request.form['email']
                    found_user.phone = request.form['phone']
                    found_user.password = request.form['password']
                    db.session.add(found_user)
                    db.session.commit()
                    return redirect(url_for('users.home'))
                flash('Passwords do not match. Please try again.', 'danger')
                return render_template('users/edit.html', form=UserForm(), user=found_user)
            flash('Missing required information', 'danger')
        return render_template('users/edit.html', form=UserForm(), user=found_user)
    flash('Permission Denied')
    return redirect(url_for('users.home'))


@users_blueprint.route('/entries', methods=['GET', 'POST'])
@login_required
def entry():
    if(request.method == 'POST'):
        content = request.get_json().get('content')
        entry = Entry(current_user.id, content)
        db.session.add(entry)
        db.session.commit()
        return json.dumps({'entry_id': entry.id}), 200

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.home'))
