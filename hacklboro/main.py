from flask import Flask, request, render_template, redirect, url_for, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import hacklboro.database

from hacklboro.auth import User
from hacklboro.goals import get_goals, get_goals_as_json, create_goal, update_goal
from hacklboro.utilities import row_list_to_json

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
        username: str = request.form["username"]
        password: str = request.form["password"]

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
        username: str = request.form["username"]
        password: str = request.form["password"]

        User.create(username, password)

        login_user(User(User.get_from_username(username)[0]))

        return "hi"
    else:
        return render_template("login.html")


@app.route("/goals/data", methods=["GET", "POST", "PUT"])
@login_required
def goals_data():
    form = request.form
    user_id = current_user.userid

    if request.method == "GET":
        # GET method for getting current goals
        return get_goals_as_json(user_id)
    elif request.method == "POST":
        # POST method for creating new goals
        percentage: float = form["percentage"]
        name: str = form["name"]
        increasing: bool = form["increasing"]

        create_goal(user_id, percentage, name, increasing)

        return "OK"
    elif request.method == "PUT":
        # PUT method for updating current goals
        id: int = form["id"]
        percentage: float = form["percentage"]

        success = update_goal(id, user_id, percentage)
        if success:
            return "OK"
        abort(401)


@app.route("/goals")
@login_required
def goals():
    return render_template("goals.html")


@app.route("/traffic-lights")
def traffic_lights():
    return render_template("trafficlight.html")


@app.route("/")
def home():
    return render_template("goals.html")
