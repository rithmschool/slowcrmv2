from flask import Blueprint, redirect, render_template, flash, url_for, request
from project import db
from project.models import Tag, Taggable, Entry, Person, Company, User
from flask_login import login_required
from project.companies.forms import TagForm
from project.users.views import get_links, get_pipes_dollars_tags_tuples


tags_blueprint = Blueprint(
    'tags',
    __name__,
    template_folder='templates'
    )

@tags_blueprint.route('/<int:id>', methods=['GET'])
@login_required
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

@tags_blueprint.route('/', methods=['GET','POST'])
@login_required
def index():
    tags = Tag.query.order_by(Tag.text).all()
    if request.method == 'POST':
        form = TagForm(request.form)
        if form.validate():
            tag_text = request.form['tag']
            tag_exists = Tag.query.filter_by(text=tag_text).first()
            if(not tag_exists):
                tag = Tag(tag_text)
                db.session.add(tag)
                db.session.commit()
                flash('"{}" added as a new tag'.format(tag_text))
                return redirect(url_for('tags.index', tags=tags))
            flash('"{}" not added since it already exists in your tags'.format(tag_text))
            return redirect(url_for('tags.index', tags=tags))   
        flash('Missing Form Data')
        return redirect(url_for('tags.new'))    
    return render_template('tags/index.html', tags=tags)

@tags_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    form = TagForm(request.form)
    term = ''
    if 'term' in request.args:
        term = request.args['term']
    return render_template('tags/new.html', form=form, term=term)    
