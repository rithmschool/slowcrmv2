from flask import Blueprint, redirect, render_template, flash, url_for, request
from project import db
from project.models import Tag, Taggable, Entry
from flask_login import login_required
from project.companies.forms import TagForm

tags_blueprint = Blueprint(
    'tags',
    __name__,
    template_folder='templates'
    )

@tags_blueprint.route('/<int:id>', methods=['GET'])
@login_required
def details(id):
    taggables = Taggable.query.filter(Taggable.tag_id==id).all()
    return render_template('tags/details.html', taggables=taggables, Entry=Entry)

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
