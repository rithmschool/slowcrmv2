from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
login_manager = LoginManager(app)
db = SQLAlchemy(app)
if os.environ.get('ENV') == 'production':
	debug=False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or "postgres://localhost/slowcrmv2-db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
CsrfProtect(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.users.views import users_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')


from project.users.models import User

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)
