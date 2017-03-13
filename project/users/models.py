from project import db, bcrypt
from flask_login import UserMixin


class User(db.Model, UserMixin):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True)
	username = db.Column(db.Text, unique=True)
	password = db.Column(db.String)
	phone = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)
	isAdmin = db.Column(db.Boolean)



def __init__(self, email, username, password):
	self.email = email
	self.username = username
	self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

