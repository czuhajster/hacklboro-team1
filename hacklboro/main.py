from flask import Flask, request, render_template
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO: Do login
        pass
    else:
        return render_template("login.html")


@app.route("/goals")
def goals():
    return render_template("goals.html")


@app.route("/")
def home():
    return render_template("home.html")
