from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or "postgres://localhost/slowcrmv2-db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT')

login_manager = LoginManager(app)
CSRFProtect(app)
db = SQLAlchemy(app)

if os.environ.get('ENV') == 'production':
    debug = False
else:
    debug = True

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

bcrypt = Bcrypt(app)
mail = Mail(app)

from project.models import User

from project.users.views import users_blueprint
from project.persons.views import persons_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(persons_blueprint, url_prefix='/persons')

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

@app.route('/')
def root():
	return "Welcome to the Root of the Source!"

from IPython import embed; embed()