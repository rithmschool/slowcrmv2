from project.users.forms import UserForm, LoginForm, InviteForm
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

@users_blueprint.route('/<int:id>/edit', methods=['GET','POST'])
@login_required
def edit(id):  
    found_user = User.query.get(current_user.id)   
    render_template('users/edit.html', form=UserForm(), user=found_user) 


@users_blueprint.route('/entries', methods=['POST'])
@login_required
def entry():
    content = request.get_json().get('content')
    if content:
        persons_companies_tuples = get_persons_companies(content)
        entry = Entry(current_user.id, content)
        add_person_data_db(persons_companies_tuples[0], content, entry)
        add_company_data_db(persons_companies_tuples[1], content, entry)
        db.session.add(entry)
        db.session.commit()
        # return json.dumps({'entry_id': entry.id}), 200
        return json.dumps({
             'data' : get_links(entry.content)
        })
    else:
        raise ValueError('content is empty')


def get_persons_companies(content):
    all_pipe_idx = [i for i,x in enumerate(content) if x == '|']
    pipe_arrayof_tuples = list(zip(all_pipe_idx[::2], all_pipe_idx[1::2]))
    all_dollar_idx = [i for i,x in enumerate(content) if x == '$']
    doller_arrayof_tuples = list(zip(all_dollar_idx[::2], all_dollar_idx[1::2]))
    return [pipe_arrayof_tuples, doller_arrayof_tuples]


def get_links(content):
    stripped_content = content.strip()
    arr = stripped_content.split(" ")
    links = ""
    for val in arr:
        if val[0] == '|' and val[-1] == '|':
            if val[1:-1]:
                links = links + get_person_link(val[1:-1])
        elif val[0] == '$' and val[-1] == '$':
            if val[1:-1]:
                links = links + get_company_link(val[1:-1])
        else:
            links = links + val 
    return links                

def get_person_link(person_name):
    person = Person.query.filter_by(name=person_name).first()
    return '<a href="/persons/{}">{}</a>'.format(person.id, person_name)

def get_company_link(company_name):
    company = Company.query.filter_by(name=company_name).first()
    return '<a href="/companies/{}">{}</a>'.format(company.id, company_name)


def add_person_data_db(persons_arr, content, entry):
    for val in persons_arr:
        person_name = content[val[0]+1 : val[1]]
        if(not Person.query.filter_by(name=person_name).first()):
            person = Person(person_name)
            db.session.add(person)
            db.session.commit()
            entry.persons.append(person)
            db.session.commit()
        else:
            entry.persons.append(Person.query.filter_by(name=person_name).first())

def add_company_data_db(companies_arr, content, entry):
    for val in companies_arr:
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
    return redirect(url_for('users.home'))
