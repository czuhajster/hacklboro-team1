from flask import Flask, request, render_template
from flask_login import LoginManager

from hacklboro.goals import get_goals, get_goals_as_json, create_goal, update_goal
from hacklboro.utilities import row_list_to_json

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return {}


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO: Do login
        pass
    else:
        return render_template("login.html")


@app.route("/goals/data", methods=["GET", "POST", "PUT"])
def goals_data():
    form = request.form
    if request.method == "GET":
        # GET method for getting current goals
        user = form["user"]
        return get_goals_as_json(user)
    elif request.method == "POST":
        # POST method for creating new goals
        user: int = form["user"]
        percentage: float = form["percentage"]
        name: str = form["name"]
        increasing: bool = form["increasing"]

        create_goal(user, percentage, name, increasing)

        return 200
    elif request.method == "PUT":
        # PUT method for updating current goals
        id: int = form["id"]
        percentage: float = form["percentage"]

        update_goal(id, percentage)

        return 200


@app.route("/goals")
def goals():
    return render_template("goals.html")


@app.route("/")
def home():
    return render_template("home.html")
