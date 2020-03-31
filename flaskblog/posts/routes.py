from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        if form.link.data:
            post.link = form.link.data
        db.session.add(post)
        db.session.commit()
        flash('הפוסט שלך נוצר!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='פוסט חדש', form=form, legend='יצירת פוסט')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.link.data:
            post.link = form.link.data
        db.session.commit()
        flash('הפוסט שלך עודכן!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.link.data = post.link
    return render_template('create_post.html', title='עדכון פוסט', form=form, legend='עדכון פוסט')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('הפוסט שלך נמחק!', 'success')
    return redirect(url_for('main.home'))
