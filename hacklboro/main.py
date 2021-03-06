from flask import Flask, request, render_template, redirect, url_for, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

import hacklboro.database

from hacklboro.auth import User
from hacklboro.goals import get_goals, get_goals_as_json, create_goal, update_goal
from hacklboro.lights import get_companies
from hacklboro.utilities import row_list_to_json

import random

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


@app.route("/goals/data", methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def goals_data():
    """
    API endpoint for interacting with the goals that the user has
    This is used by the frontend to create/update/delete goals with JavaScript
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
    elif request.method == "DELETE":
        id: int = int(form["id"])
        success = hacklboro.goals.delete_goal(id, int(user_id))

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


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    """
    Page displaying the calculator for transport and CO2 emissions
    """
    # Post request shows the calculation
    if request.method == "POST":
        random_facts = [
            "Coal burning globally emits 14.7 billion tonnes of CO2 each year.",
            "Oil burning globally emits 12.4 billion tonnes of CO2 each year.",
            "Gas burning globally emits 7.5 billion tonnes of CO2 each year.",
            "China emits 10 billion tonnes of CO2 each year.",
            "USA emits 5 billion tonnes of CO2 each year.",
            "800 million people are at risk due to climate change impacts.",
            "800,000 hectares of mangroves are lost each year. These mangroves are vital for storing carbon dioxide.",
        ]

        geolocator = Nominatim(user_agent="melon")

        emissions: float = 0
        transport = request.form["transport"]

        start = geolocator.geocode(request.form["start"])
        finish = geolocator.geocode(request.form["finish"])

        miles = geodesic((start.latitude, start.longitude), (finish.latitude, finish.longitude)).miles

        if transport == "car":
            average_car_emissions_per_km: float = 0.1224
            average_car_emissions_per_mile: float = average_car_emissions_per_km * 1.60934

            emissions = miles * average_car_emissions_per_mile
        elif transport == "plane":
            average_plane_emissions_per_km: float = 0.154
            average_plane_emissions_per_mile: float = average_plane_emissions_per_km * 1.60934

            emissions = miles * average_plane_emissions_per_mile
        elif transport == "bus":
            average_bus_emissions_per_km: float = 0.09
            average_bus_emissions_per_mile: float = average_bus_emissions_per_km * 1.60934

            emissions = miles * average_bus_emissions_per_mile
        elif transport == "train":
            average_train_emissions_per_km: float = 0.05
            average_train_emissions_per_mile: float = average_train_emissions_per_km * 1.60934

            emissions = miles * average_train_emissions_per_mile
        elif transport == "cruise":
            average_cruise_emissions_per_km: float = 0.254
            average_cruise_emissions_per_mile: float = average_cruise_emissions_per_km * 1.60934

            emissions = miles * average_cruise_emissions_per_mile

        return render_template("calculator-result.html", emissions=f"{emissions:.2f}", distance=f"{miles:.2f}",
                               fact=random.choice(random_facts))

    # GET request shows the calculator for user input
    return render_template("calculator.html")


@app.route("/")
def home():
    return render_template("home.html")
