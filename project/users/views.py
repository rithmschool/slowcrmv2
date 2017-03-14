from project.users.forms import UserForm
from project.users.forms import LoginForm
from flask import Blueprint, redirect, render_template, request, flash, url_for, session, g
from project.users.models import User, Person
from project import db, bcrypt, mail
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from flask_mail import Message 
from project.users.token import generate_confirmation_token, confirm_token
from datetime import datetime

def send_token(subject, html, name, email, confirm_url):
    msg = Message(subject, sender="noreply.slowcrm@gmail.com", recipients=[email])
    msg.html = render_template(html, name = name, confirm_url = confirm_url)
    mail.send(msg)



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

@login_required
@users_blueprint.route('/invite', methods=['POST'])
def invite():
    form = UserForm(request.form)
    if form.validate():
        email = request.form.get('email')
        name = request.form.get('name')
        token = generate_confirmation_token(email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        new_user = User(email,name,'temppass','',True,False)
        db.session.add(new_user)
        db.session.commit()
        send_token("You Have Been Invited To Join Slow CRM", "users.new_user.html", name, email, confirm_url)
        return "Invite Sent"
    else:
        flash('The form is incomplete') 
        return "Missing form data"   

@users_blueprint.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('Your confirmation link has expired or is invalid, please ask admin to resend invite.', 'danger')
        return redirect(url_for('users.login'))
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login or reset password', 'success')
        return redirect(url_for('users.login'))
    else:   
        user.confirmed = True
        user.updated_at = datetime.now()
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return render_template('users/edit.html', form=UserForm(), user=user)

@login_required
@users_blueprint.route('/<int:id>/edit', methods=['GET']) 
def edit(id):  
    found_user = User.query.get(current_user.id)   
    render_template('users/edit.html', form=UserForm(), user=found_user) 



