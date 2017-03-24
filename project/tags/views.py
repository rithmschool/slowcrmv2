from flask import Blueprint, render_template
from project.models import Tag, Taggable, Entry, Person, Company
from project.users.views import get_links, get_pipes_dollars_tags_tuples

tags_blueprint = Blueprint(
    'tags',
    __name__,
    template_folder='templates'
    )

@tags_blueprint.route('/<int:id>', methods=['GET'])
def details(id):
    taggables = Taggable.query.filter(Taggable.tag_id==id).all()
    tag_name = Tag.query.get(id)
    tagged_entries = [ 
    get_links(Entry.query.get(tagged.id).content,
        get_pipes_dollars_tags_tuples(Entry.query.get(tagged.id).content)
        ) for tagged in taggables if tagged.taggable_type == "entry"]

    from IPython import embed; embed()
    # formatted_entries = [Entry.query.get(entry.id).content for entry in taggables if entry.taggable_type=="entry"]
    return render_template('tags/details.html', tag_name=tag_name, taggables=taggables, tagged_entries=tagged_entries, 
        Company=Company, Person=Person)

@tags_blueprint.route('/', methods=['GET'])
def index():
    tags = Tag.query.order_by(Tag.text).all()
    return render_template('tags/index.html', tags=tags)
