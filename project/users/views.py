from flask import Blueprint, request, render_template, url_for, redirect, flash
from project.users.models import User
from project import db, bcrypt
from project.users.forms import InviteUserForm

from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint(
	'users',
	__name__,
	template_folder = 'templates'
)


