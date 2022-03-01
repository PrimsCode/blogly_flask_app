"""Blogly application."""

from flask import Flask, render_template, request, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


app = Flask(__name__, static_url_path="", static_folder="static")

app.config['SECRET_KEY']="12345"
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/")
def redirect():
    return redirect("/users")

@app.route("/users")
def list_users():
    """List users"""

    users = User.query.all()
    return render_template("index.html", users=users)

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

@app.route("users/<int:user_id>")
def user_profile(user_id):
    """Show the user profile"""

    user = User.query.get_or_404(user_id)
    return render_template("profile.html", user=user)

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

@app.route("users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")