from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
login_manager = LoginManager(app)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or "postgres://localhost/slowcrmv2-db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mail = Mail(app)


from project.users.models import User

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)
