from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user

import database
from auth import User

app = Flask(__name__)
app.secret_key = "wWfZsm9tAtjT8G5svySA7BfQtaua7qC9VrysKJMr8GEqvZ"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.verify(username, password):
            login_user(User(User.get_from_username(username)[0]))

        return redirect(url_for('home'))
    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        User.create(username, password)

        login_user(User(User.get_from_username(username)[0]))

        return "hi"
    else:
        return render_template("login.html")


@app.route("/goals")
@login_required
def goals():
    return render_template("goals.html")


@app.route("/")
def home():
    return render_template("home.html")
