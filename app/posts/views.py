from flask import render_template, redirect, url_for, flash, request, session

from app import db
from . import post_bp
from .forms import PostForm
from .models import Post, Tag
from ..users.models import User


@post_bp.route('/', strict_slashes=False)
def all_posts():
    stmt = (db.select(Post)
            .where(Post.is_active.is_(True))
            .order_by(Post.posted.desc()))
    posts = db.session.scalars(stmt).all()
    return render_template('posts.html', posts=posts, title='Пости')


@post_bp.route('/create', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    authors = db.session.scalars(db.select(User)).all()
    form.author_id.choices = [(author.id, author.username) for author in authors]

    tags = db.session.scalars(db.select(Tag)).all()
    form.tags.choices = [(tag.id, tag.name) for tag in tags]

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data,
            user_id=form.author_id.data,
        )
        selected_tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all()
        post.tags = selected_tags
        db.session.add(post)
        db.session.commit()
        flash(f"Post '{post.title}' has been added.", 'success')
        return redirect(url_for('posts.all_posts'))
    if request.method == 'POST':
        flash('Enter the correct data in the form!', 'danger')
    return render_template('add_post.html', form=form,
                           title='Новий пост', heading='Create a New Post')


@post_bp.route('/<int:id>')
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template('detail_post.html', post=post, title=post.title)


@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    authors = db.session.scalars(db.select(User)).all()
    form.author_id.choices = [(author.id, author.username) for author in authors]

    tags = db.session.scalars(db.select(Tag)).all()
    form.tags.choices = [(tag.id, tag.name) for tag in tags]

    if request.method == 'GET':
        form.publish_date.data = post.posted  
        form.author_id.data = post.user_id
        form.tags.data = [tag.id for tag in post.tags]
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.category = form.category.data
        post.posted = form.publish_date.data
        post.user_id = form.author_id.data
        post.tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all()
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('posts.detail_post', id=post.id))
    return render_template('add_post.html', form=form,
                           title='Редагування', heading='Edit Post')


@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', 'danger')
        return redirect(url_for('posts.all_posts'))
    return render_template('delete_confirm.html', post=post,
                           title='Підтвердження видалення')