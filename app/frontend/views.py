
from flask import (
    Blueprint, render_template
)
frontend = Blueprint('frontend', __name__, static_folder='../static')


@frontend.route("/")
def index():
    return render_template("index.html")


@frontend.route("/questions")
def questions():
    return render_template("questions.html")


@frontend.route("/thanks")
def thanks():
    return render_template("thanks.html")
