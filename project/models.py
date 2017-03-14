from project import db, bcrypt
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.Text, nullable=True)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)



    def __init__(self, email, name, password, phone, created_at, updated_at, is_admin, confirmed):
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.phone = phone
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_admin = is_admin
        self.confirmed = confirmed

    def __repr__(self):
        return "user_id {} name {}".format(self.id, self.name)  



class EntryCompany(db.Model, UserMixin):
    __tablename__ = 'entry_companies'

    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id', ondelete="CASCADE"))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id', ondelete="CASCADE"))


    def __init__(self, entry_id, company_id):
        self.entry_id = entry_id
        self.company_id = company_id

    def __repr__(self):
        return "entryCompany_id {}".format(self.id)



class Entry(db.Model, UserMixin):

    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    archived = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    companies = db.relationship('Company', secondary=EntryCompany, backref='entry', lazy='dynamic')
    # peoples = db.relationship('People', secondary=EntryPeople, backref='entry', lazy='dynamic')


    def __init__(self, user_id, title, description, archived, created_at, updated_at):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.archived = archived


    def __repr__(self):
        return "entry_id {} title {}".format(self.id, self.title)  


