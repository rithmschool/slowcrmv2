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
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    is_admin = db.Column(db.Boolean, nullable=False, default=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)



    def __init__(self, email, name, password, phone, is_admin, confirmed):
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.phone = phone
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_admin = is_admin
        self.confirmed = confirmed

    def __repr__(self):
        return "{},{},{},{},{},{},{},{}".format(self.email,self.name,self.password, self.phone,
            self.created_at, self.updated_at,self.is_admin,self.confirmed)

class Person(db.Model):
    __tablename__ = "persons"

    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.Text, nullable=True, unique=True)
    phone = db.Column(db.Integer, nullable=True)
    name = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    slow_lp = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now) 
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)


    def __init__(self, email, phone, name, title, description, slow_lp):
        self.email = email
        self.phone = phone
        self.name = name
        self.title = title
        self.description = description
        self.slow_lp = slow_lp
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __repr__(self):
        return "{},{},{},{},{},{},{}".format(self.email,self.phone,self.name,
            self.description,self.slow_lp,self.created_at,self.updated_at)
