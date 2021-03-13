from flask import Flask, request, render_template, redirect, url_for, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import hacklboro.database

from hacklboro.auth import User
from hacklboro.goals import get_goals, get_goals_as_json, create_goal, update_goal
from hacklboro.lights import get_companies
from hacklboro.utilities import row_list_to_json

app = Flask(__name__)
app.secret_key = "wWfZsm9tAtjT8G5svySA7BfQtaua7qC9VrysKJMr8GEqvZ"
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def page_not_found(e):
    """
    Custom error if the user goes on a missing page
    """
    return render_template('not-found.html'), 404


@app.errorhandler(401)
def unauthorized(e):
    """
    Custom error if the user goes on a page they're not allowed to access
    """
    return render_template('unauthorized.html'), 401


@login_manager.user_loader
def load_user(userid):
    """
    Loads the User object so that we know who we are serving
    """
    return User(userid)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login page for the website. GET request to see the page and POST request to log in.
    """

    # POST request requires Content-Type: application/x-www-form-urlencoded for the form to log in
    if request.method == "POST":
        username: str = request.form["username"]
        password: str = request.form["password"]

        if User.verify(username, password):
            login_user(User(User.get_from_username(username)[0]))
            return redirect(url_for('goals'))
        else:
            return render_template("login.html")
    else:
        if current_user.is_authenticated:
            return redirect(url_for('goals'))
        return render_template("login.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    Logout redirect to remove the user session
    """
    logout_user()
    return redirect(url_for('home'))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Signup page to create a user account
    """
    if request.method == "POST":
        username: str = request.form["username"]
        password: str = request.form["password"]

        User.create(username, password)

        login_user(User(User.get_from_username(username)[0]))

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/goals/data", methods=["GET", "POST", "PUT"])
@login_required
def goals_data():
    """
    API endpoint for interacting with the goals that the user has
    This is used by the frontend to create/update goals with JavaScript
    """
    form = request.form
    user_id = current_user.userid

    if request.method == "GET":
        # GET method for getting current goals
        return get_goals_as_json(user_id)
    elif request.method == "POST":
        # POST method for creating new goals
        percentage: float = 0
        name: str = form["name"]
        increasing: bool = True

        create_goal(user_id, percentage, name, increasing)

        return redirect("/goals")
    elif request.method == "PUT":
        # PUT method for updating current goals
        id: int = int(form["id"])
        percentage: float = form["percentage"]

        success = update_goal(id, int(user_id), percentage)
        if success:
            return redirect("/goals")
        abort(401)


@app.route("/goals")
@login_required
def goals():
    """
    Page displaying all of the user's goals
    This is not the same as the API endpoint for the goals
    """
    user_id = current_user.userid
    goals = get_goals(user_id)
    return render_template("goals.html", goals=goals)


@app.route("/traffic-lights")
def traffic_lights():
    """
    Page displaying data about companies and how good they are on a traffic light scale
    """
    companies = get_companies()
    return render_template("trafficlight.html", companies=companies)


@app.route("/")
def home():
    return render_template("home.html")
