from flask import Blueprint, redirect, render_template, flash, url_for, request
from project import db
from project.models import Tag, Taggable, Entry
from flask_login import login_required

tags_blueprint = Blueprint(
    'tags',
    __name__,
    template_folder='templates'
    )

@tags_blueprint.route('/<int:id>', methods=['GET'])
def details(id):
    taggables = Taggable.query.filter_by(id=id)
    return render_template('tags/details.html', taggables=taggables, Entry=Entry)
