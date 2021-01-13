from flask import (
    Flask,
    render_template,
    session,
    redirect,
    request,
    url_for,
    flash,
    Response,
    make_response,
    Markup,
    jsonify,
)

from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
import pymongo
import os

app = Flask(__name__)
from user import routes

app.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY")
app.config["MONGO_URI"] = "mongodb://localhost:27017/CricBlog"


bcrypt = Bcrypt(app)

import user.models as user

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup/", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        temp = user.User()

        result = temp.signup()
        if not result[1]:
            flash(result[2], "danger")
            return render_template("signup.html", user=result[0])
        else:
            flash("Account added successfully", "success")
            return render_template("signup.html")
    else:

        return render_template("signup.html")


@app.route("/login/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        temp = user.User()

        result = temp.login()
        if not result[0]:
            flash(result[1], "danger")
        else:
            flash(result[1], "success")

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)