from flask import Blueprint, redirect, render_template, flash, url_for, request
from project import db
from project.models import Tag, Taggable, Entry, Person, Company
from flask_login import login_required

tags_blueprint = Blueprint(
    'tags',
    __name__,
    template_folder='templates'
    )

@tags_blueprint.route('/<int:id>', methods=['GET'])
def details(id):
    taggables = Taggable.query.filter(Taggable.tag_id==id).all()
    return render_template('tags/details.html', taggables=taggables, Entry=Entry, Company=Company, Person=Person)

@tags_blueprint.route('/', methods=['GET'])
def index():
    tags = Tag.query.order_by(Tag.text).all()
    return render_template('tags/index.html', tags=tags)
