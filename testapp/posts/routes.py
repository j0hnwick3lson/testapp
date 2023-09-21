from flask import (Blueprint,redirect,url_for,render_template,abort,request,flash)
from flask_login import current_user,login_required
from testapp.models import Post
from testapp import db
from testapp.posts.forms import Postform
posts=Blueprint('posts',__name__)


@posts.route("/post/new",methods=['POST','GET'])
@login_required
def new_post():
    form=Postform()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('main.home'))
    return render_template("create_post.html",title="New Post",form=form,legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)
    

@posts.route("/post/<int:post_id>/update",methods=['POST','GET'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form = Postform()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash("Your Post has been Updated!","success")
        return redirect(url_for("posts.post",post_id=post.id))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template("create_post.html",title="Update Post",form=form,legend='Update Post')


@posts.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted","success")
    return redirect(url_for("main.home"))

@posts.route("/latestpost")
def latestpost():
    posts = Post.query.filter_by().order_by(Post.date_posted.desc()).paginate(per_page=5)
    return render_template("latestposts.html",title="Latest",posts=posts)