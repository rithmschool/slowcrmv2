from flask import Blueprint, render_template
from project.models import Tag, Taggable, Entry, Person, Company

tags_blueprint = Blueprint(
    'tags',
    __name__,
    template_folder='templates'
    )

@tags_blueprint.route('/<int:id>', methods=['GET'])
def details(id):
    taggables = Taggable.query.filter(Taggable.tag_id==id).all()
    tag_name = Tag.query.get(id)
    return render_template('tags/details.html', tag_name=tag_name, taggables=taggables, Entry=Entry, Company=Company, Person=Person)

@tags_blueprint.route('/', methods=['GET'])
def index():
    tags = Tag.query.order_by(Tag.text).all()
    return render_template('tags/index.html', tags=tags)
