"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)

# Use once to setup the database using the models
# with app.app_context():
#     db.create_all()

app.config['SECRET_KEY'] = "Secret Secret Secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.route("/")
def root_route():
    """ Homepage"""
    return redirect("/users")


@app.route("/users")
def users_route():
    """  List of Users"""
    users = User.query.order_by(User.last_name).all()

    return render_template("home.html", users = users)

@app.route("/users/new", methods=["GET"])
def create_user_form():
    """ Create a new User"""

    return render_template("new_user.html")


@app.route("/users/new", methods=["POST"])
def create_user_db():
    """ Create a new User"""
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or '/static/img/default.jpg')

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_details(user_id):

    user = User.query.get_or_404(user_id)

    return render_template("user_detail.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user_details_form(user_id):
    
    user = User.query.get_or_404(user_id)

    return render_template("user_detail_edit_form.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_details(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form['image_url'] or '/static/img/default.jpg'

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
