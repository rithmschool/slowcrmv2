from flask import Blueprint, render_template
from project.models import Tag, Taggable, Entry, Person, Company, User
from project.users.views import get_links, get_pipes_dollars_tags_tuples

tags_blueprint = Blueprint(
    'tags',
    __name__,
    template_folder='templates'
    )

@tags_blueprint.route('/<int:id>', methods=['GET'])
def details(id):
    # taggables = Taggable.query.filter(Taggable.tag_id==id).all()
    tag_name = Tag.query.get(id)
    formatted_entries = [{
        "content": get_links(Entry.query.get(tagged_entry.taggable_id).content,
        get_pipes_dollars_tags_tuples(Entry.query.get(tagged_entry.taggable_id).content) 
        ),
        "user_id": User.query.get((Entry.query.get(tagged_entry.taggable_id).user_id)).id,
        "user_name": User.query.get((Entry.query.get(tagged_entry.taggable_id).user_id)).name
        } for tagged_entry in Taggable.query.filter_by(tag_id=id, taggable_type="entry")]

    formatted_companies = [{
        "company_name": Company.query.get(company.taggable_id).name,
        "company_id": Company.query.get(company.taggable_id).id,
        "tags": [Tag.query.get(tag.tag_id) for tag in Taggable.query.filter_by(taggable_id=Company.query.get(company.taggable_id).id, taggable_type="company")]
        } for company in Taggable.query.filter_by(tag_id=id, taggable_type="company")]

    formatted_persons = [{
        "person_name": Person.query.get(person.taggable_id).name,
        "person_id": Person.query.get(person.taggable_id).id,
         "tags": [Tag.query.get(tag.tag_id) for tag in Taggable.query.filter_by(taggable_id=Person.query.get(person.taggable_id).id, taggable_type="person")]
        } for person in Taggable.query.filter_by(tag_id=id, taggable_type="person")]
    return render_template('tags/details.html', tag_name=tag_name, formatted_entries=formatted_entries, formatted_companies=formatted_companies, formatted_persons=formatted_persons)

@tags_blueprint.route('/', methods=['GET'])
def index():
    tags = Tag.query.order_by(Tag.text).all()
    return render_template('tags/index.html', tags=tags)
