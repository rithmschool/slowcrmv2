from project.users.forms import UserForm
from project.users.forms import LoginForm
from flask import Blueprint, redirect, render_template, request, flash, url_for, session, g
from project.users.models import User
from project import db, bcrypt

from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint(
	'users',
	__name__,
	template_folder = 'templates'
)





