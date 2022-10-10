"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag


app = Flask(__name__, static_url_path="", static_folder="static")

app.config['SECRET_KEY']="12345"
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/")
def welcome_page():
    return render_template("welcome.html")

@app.route("/home")
def home():
    posts = Post.query.all()
    users = User.query.all()
    return render_template("home.html", posts=posts, users=users)

@app.route("/users")
def list_users():
    """List users"""

    users = User.query.all()
    return render_template("list_users.html", users=users)

@app.route("/users/new")
def show_add_form():
    """Show add new user form"""
    return render_template("create_user.html")


@app.route("/users/new", methods=["POST"])
def create_user():
    """Create a new user and redirect to list."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None
    
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def user_profile(user_id):
    """Show the user profile"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user.id).all() 
    return render_template("show_profile.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit")
def show_edit_form(user_id):
    """Show edit user form"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edit user information"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User is deleted!")

    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("create_post.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):

    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    post = Post(title=title, content=content, user_id=user.id, tags=tags)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/users/<int:user_id>/posts/<int:post_id>")
def show_post(user_id, post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(user_id)

    return render_template("show_post.html", user=user, post=post)

@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    
    return render_template("edit_post.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Edit user information"""
    
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post.tags = tags

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Delete post"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route("/posts")
def show_all_posts():
    """Show all the posts"""

    posts = Post.query.all() 
    return render_template("list_posts.html", posts=posts)


@app.route("/tags")
def list_tags():
    """List existing tags"""

    tags = Tag.query.all()
    return render_template("list_tag.html", tags=tags)


@app.route("/tags/new")
def show_create_tags():
    """Show create a tag page"""

    return render_template("create_tag.html")


@app.route("/tags/new", methods=["POST"])
def create_tags():
    """Create a new tag"""

    name = request.form['name']

    tag = Tag(name = name)
    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """Show tag page"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag=tag)

@app.route("/tags/<int:tag_id>/edit")
def show_edit_tags(tag_id):
    """Show edit tag page"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tags(tag_id):
    """Edit tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
                
    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete")
def delete_tags(tag_id):
    """Delete tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")

