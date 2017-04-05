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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=db.func.now())
    is_admin = db.Column(db.Boolean, nullable=False, default=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    entries = db.relationship('Entry', backref='user', lazy='dynamic')

    def __init__(self, email, name, password, phone, is_admin, confirmed, created_at=datetime.now(), updated_at=datetime.now()):
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.phone = phone
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_admin = is_admin
        self.confirmed = confirmed

    def __repr__(self):
        return "{},{},{},{},{},{},{},{}".format(
            self.email,self.name,
            self.password,
            self.phone,
            self.created_at, self.updated_at,self.is_admin,self.confirmed
        )

entry_persons = db.Table('entries_persons',
    db.Column('entry_id', db.Integer, db.ForeignKey("entries.id")),
    db.Column('person_id', db.Integer, db.ForeignKey("persons.id"))
)

class Person(db.Model):
    taggable_type = 'person'
    __tablename__ = "persons"

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String, nullable=True)
    name = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    slow_lp = db.Column(db.Boolean)
    archived = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now,
        onupdate=db.func.now())

    def __init__(self, name, email="", phone="", title="", description="", slow_lp=False, archived=False):
        self.email = email
        self.phone = phone
        self.name = name
        self.title = title
        self.description = description
        self.slow_lp = slow_lp
        self.archived = archived
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __repr__(self):
        return "{},{},{},{},{},{},{},Created:{}, Updated:{}".format(
            self.id,
            self.archived,
            self.email,
            self.phone,
            self.name,
            self.description,
            self.slow_lp,
            self.created_at,
            self.updated_at
        )

entry_companies = db.Table('entries_companies',
    db.Column('entry_id', db.Integer, db.ForeignKey("entries.id")),
    db.Column('company_id', db.Integer, db.ForeignKey("companies.id"))
)

class Company(db.Model):
    taggable_type = 'company'
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=True)
    logo_url = db.Column(db.Text, nullable=True)
    partner_lead = db.Column(db.Text, nullable=True)
    ops_lead = db.Column(db.Text, nullable=True)
    source = db.Column(db.Text, nullable=True)
    round = db.Column(db.Text, nullable=True)
    archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now,
        onupdate=db.func.now())

    def __init__(self, name, description="", url="", logo_url="", partner_lead="", ops_lead="", source="", round="", archived=False):
        self.name = name
        self.description = description
        self.url = url
        self.logo_url = logo_url
        self.partner_lead = partner_lead
        self.ops_lead = ops_lead
        self.source = source
        self.round = round
        self.archived = archived
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __repr__(self):
        return "{},{},{},{},{},{},{},{},Created:{}, Updated:{}".format(
            self.archived,
            self.id,
            self.name,
            self.description,
            self.url,
            self.logo_url,
            self.partner_lead,
            self.ops_lead,
            self.created_at,
            self.updated_at
        )

class Entry(db.Model, UserMixin):
    taggable_type = 'entry'
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    content = db.Column(db.String, nullable=False)
    archived = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=db.func.now())
    companies = db.relationship('Company', secondary=entry_companies, backref=db.backref('entries'), lazy='dynamic')
    persons = db.relationship('Person', secondary=entry_persons, backref=db.backref('entries'), lazy='dynamic')

    def __init__(self, user_id, content, archived=False):
        self.user_id = user_id
        self.content = content
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.archived = archived

    def __repr__(self):
        return "id {} content {}".format(self.id, self.content)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    archived = db.Column(db.Boolean, default=False)

    def __init__(self, text, archived=False):
        self.text = text
        self.archived = archived

class Taggable(db.Model):
    __tablename__ = 'taggable'

    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'))
    taggable_id = db.Column(db.Integer)
    taggable_type = db.Column(db.String)
    tags = db.relationship('Tag', backref=db.backref('taggable'))

    def __init__(self, taggable_id, tag_id, taggable_type):
        self.tag_id = tag_id
        self.taggable_id = taggable_id
        self.taggable_type = taggable_type
