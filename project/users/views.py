from project.users.forms import UserForm, LoginForm, InviteForm, EditUserForm, ForgotPasswordForm, EditPasswordForm, RecoverPasswordForm
from flask import Blueprint, redirect, render_template, request, flash, url_for, session, g, jsonify
from project.models import User, Person, Entry, Company
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

@users_blueprint.route('/search', methods=['GET'])
def search():
    term = request.args.get('search')
    results = Entry.query.filter(Entry.content.ilike("%{}%".format(term)))
    count = results.count()
    return render_template('users/search.html', results=results, count=count)

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
        found_user.updated_at = datetime.now()
        db.session.add(found_user)
        db.session.commit()
        login_user(found_user)
        return render_template('users/update.html', form=UserForm(), user=found_user)

@users_blueprint.route('/<int:id>')
@login_required
def show(id):
    found_user = User.query.get_or_404(id)
    return render_template('users/show.html', user=found_user)

# for editing users that are not new
@users_blueprint.route('/<int:id>/edit', methods=['GET','PATCH'])
@login_required
def edit(id):
    if id == current_user.id:
        found_user = User.query.get(id)
        if request.method ==b"PATCH":
            form = EditUserForm(request.form)
            if form.validate():
                if bcrypt.check_password_hash(found_user.password, request.form['password']):
                    flash('You have successfully updated your user info!', 'success')
                    found_user.name = request.form['name']
                    found_user.email = request.form['email']
                    found_user.phone = request.form['phone']
                    db.session.add(found_user)
                    db.session.commit()
                    return redirect(url_for('users.show', id=found_user.id))
                flash('Password Incorrect', 'danger')
                return render_template('users/edit.html', form=EditUserForm(), user=found_user)   
            flash('Missing required information', 'danger')
        return render_template('users/edit.html', form=EditUserForm(), user=found_user)
    flash('Permission Denied')
    return redirect(url_for('users.home'))


@users_blueprint.route('/<int:id>/editpassword', methods=['GET','PATCH'])
@login_required
def edit_password(id):
    if id == current_user.id:
        found_user = User.query.get(id)
        if request.method == b"PATCH":
            form = EditPasswordForm(request.form)
            if form.validate():
                if bcrypt.check_password_hash(found_user.password, request.form['currentpassword']):
                    if request.form['newpassword'] == request.form['confirmpassword']:
                        found_user.password = bcrypt.generate_password_hash(request.form['newpassword']).decode('UTF-8')
                        db.session.add(found_user)
                        db.session.commit()
                        flash('Password updated')
                        return redirect(url_for('users.show', id=found_user.id))
                    flash('Passwords do not match')
                    return redirect(url_for('users.edit_password', form=EditPasswordForm(), id=found_user.id))
                flash('Current password is incorrect')
                return redirect(url_for('users.edit_password', form=EditPasswordForm(), id=found_user.id))
            return render_template('users/edit_password.html', form=EditPasswordForm(), user=found_user)           
        return render_template('users/edit_password.html', form=EditPasswordForm(), user=found_user)
    flash('Permission Denied')
    return redirect(url_for('users.home'))    


# Only for new invited users
@users_blueprint.route('/<int:id>/update', methods=['GET','PATCH'])
@login_required
def update(id):
    if id == current_user.id:
        found_user = User.query.get(id)
        if found_user.confirmed:
            flash('Your account has already been confirmed, please log in')
            return redirect(url_for('users.login'))
        if request.method ==b"PATCH":
            form = UserForm(request.form)
            if form.validate():
                if request.form['password'] == request.form['confirmpassword']:
                    flash('You have successfully updated your user info!', 'success')
                    found_user.name = request.form['name']
                    found_user.email = request.form['email']
                    found_user.phone = request.form['phone']
                    found_user.password = bcrypt.generate_password_hash(request.form['password']).decode('UTF-8')
                    found_user.confirmed = True
                    db.session.add(found_user)
                    db.session.commit()
                    return redirect(url_for('users.home'))
                flash('Passwords do not match. Please try again.', 'danger')
                return render_template('users/update.html', form=UserForm(), user=found_user)
        return render_template('users/update.html', form=UserForm(), user=found_user)
    flash('Permission Denied')
    return redirect(url_for('users.home'))

@users_blueprint.route('/passwordreset', methods=['GET','POST'])
def reset():
    if request.method == 'POST':
        form = ForgotPasswordForm(request.form)
        if form.validate():
            found_user = User.query.filter_by(email=request.form['email']).first()
            if found_user:
                flash('Email Sent!')
                token = generate_confirmation_token(found_user.email)
                confirm_url = url_for('users.password_recovery', token=token, _external=True)
                send_token("Reset your password on Slow CRM", "users/password_reset_email.html", found_user.name, found_user.email, confirm_url)
                return redirect(url_for('users.login'))
            flash('Email Not Found') 
    return render_template('users/forgot.html', form=ForgotPasswordForm())

@users_blueprint.route('/passwordreset/<token>', methods=['GET','PATCH'])
def password_recovery(token):
    if request.method ==b"PATCH":
        form = RecoverPasswordForm(request.form)
        if form.validate():
            found_user = User.query.filter_by(email=confirm_token(token)).first_or_404()
            if request.form['password'] == request.form['confirmpassword']:
                found_user.password = bcrypt.generate_password_hash(request.form['password']).decode('UTF-8')
                db.session.add(found_user)
                db.session.commit()
                flash('Password updated')
                return redirect(url_for('users.login'))
            flash('Passwords do not match')
        render_template('users/passwordreset/{}'.format(token))            
    try:
        email = confirm_token(token)
    except:
        flash('Your confirmation link has expired or is invalid, please reset again if needed.', 'danger')
        return redirect(url_for('users.login'))
    found_user = User.query.filter_by(email=email).first_or_404()
    return render_template('users/password_recover.html', form=RecoverPasswordForm(), user=found_user, token=token)


@users_blueprint.route('/entries', methods=['POST'])
@login_required
def entry():
    content = request.get_json().get('content')
    if content:
        try:
            pipes_dollars_tuples = get_pipes_dollars_tuples(content)
            entry = Entry(current_user.id, content)
            add_person_data_db(pipes_dollars_tuples[0], content, entry)
            add_company_data_db(pipes_dollars_tuples[1], content, entry)
            db.session.add(entry)
            db.session.commit()
        except ValueError as e:
            return json.dumps({
                    'message': str(e)
                }), 400

        return json.dumps({
             'data' : get_links(entry.content, pipes_dollars_tuples),
             'entry_id': entry.id
        }), 200
    else:
        raise ValueError('content is empty')


def get_pipes_dollars_tuples(content):
    all_pipe_idx = []
    all_dollar_idx = []
    for idx, char in enumerate(content):
        if char == '|':
            all_pipe_idx.append(idx)
        elif char == '$':
            all_dollar_idx.append(idx)
    check_correct_pipes_dollars(all_pipe_idx, all_dollar_idx)
    pipe_arrayof_tuples = list(zip(all_pipe_idx[::2], all_pipe_idx[1::2]))
    doller_arrayof_tuples = list(zip(all_dollar_idx[::2], all_dollar_idx[1::2]))
    return [pipe_arrayof_tuples, doller_arrayof_tuples]


def check_correct_pipes_dollars(pipes_idx_arr, dollar_idx_arr):
    if(len(pipes_idx_arr) % 2 != 0):
        raise ValueError('"|" is missing!')
    if(len(dollar_idx_arr) % 2 != 0):
        raise ValueError('"$" is missing!') 


def get_links(content, pipes_dollars_tuples):
    pipes_tuples_arr = pipes_dollars_tuples[0]
    dollars_tuples_arr = pipes_dollars_tuples[1]
    stripped_content = content.strip()
    links = ""
    idx = 0
    while idx < len(stripped_content):    
        if pipes_tuples_arr and idx in [pipes_tuples_arr[0][0]]:
            person_name = stripped_content[pipes_tuples_arr[0][0]+1: pipes_tuples_arr[0][1]]
            links = links + get_person_link(person_name)
            idx = idx + pipes_tuples_arr[0][1]+1
            pipes_tuples_arr.pop(0)
        elif dollars_tuples_arr and idx in [dollars_tuples_arr[0][0]]:
            company_name = stripped_content[dollars_tuples_arr[0][0]+1: dollars_tuples_arr[0][1]] 
            links = links + get_company_link(company_name)
            idx = idx + dollars_tuples_arr[0][1]+1
            dollars_tuples_arr.pop(0)
        else:
            links = links + stripped_content[idx] 
            idx = idx + 1 
    return links.strip()                

def get_person_link(person_name):
    person = Person.query.filter_by(name=person_name).first()
    return '<a href="/persons/{}">{}</a>'.format(person.id, person_name)

def get_company_link(company_name):
    company = Company.query.filter_by(name=company_name).first()
    return '<a href="/companies/{}">{}</a>'.format(company.id, company_name)


def add_person_data_db(pipes_tuples_arr, content, entry):
    for val in pipes_tuples_arr:
        person_name = content[val[0]+1 : val[1]]
        if(not Person.query.filter_by(name=person_name).first()):
            person = Person(person_name)
            db.session.add(person)
            db.session.commit()
            entry.persons.append(person)
            db.session.commit()
        else:
            entry.persons.append(Person.query.filter_by(name=person_name).first())


def add_company_data_db(dollars_tuples_arr, content, entry):
    for val in dollars_tuples_arr:
        company_name = content[val[0]+1 : val[1]]
        if(not Company.query.filter_by(name=company_name).first()):
            company = Company(company_name)
            db.session.add(company)
            db.session.commit()
            entry.companies.append(company)
            db.session.commit()
        else:
            entry.companies.append(Company.query.filter_by(name=company_name).first())    


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))
