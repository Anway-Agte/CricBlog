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
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
import pymongo
import os

app = Flask(__name__)
from user import routes

app.secret_key = (
    "\xea\xf5|k\xb8\x02+\xba\x18\x90\x80v\xcb?\xab\xab\x8d\x86\x92\xe5\xff\xbe"
)
app.config["MONGO_URI"] = "mongodb://localhost:27017/CricBlog"


bcrypt = Bcrypt(app)
socketio = SocketIO(app)
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

    if "logged_in" in session:
        return redirect(url_for("forum"))

    if request.method == "POST":
        temp = user.User()

        result = temp.login()
        if not result[0]:
            flash(result[1], "danger")
            return redirect(url_for("login"))
        else:

            return redirect(url_for("forum"))

    return render_template("login.html")


@app.route("/forum/", methods=["GET", "POST"])
def forum():

    data = user.User().find_user()

    posts = list(user.User().find_posts())

    return render_template("forum.html", data=data, posts=posts[::-1])


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    session.clear()

    return redirect(url_for("index"))


@app.route("/create/", methods=["GET", "POST"])
def create():

    data = user.User().find_user()

    preferences = user.User().get_preferences()

    return render_template("create.html", data=data, preferences=preferences)


@app.route("/publish/", methods=["POST"])
def publish():

    result = user.User().publish()

    if not result[0]:
        flash(result[2], "danger")

        return redirect(url_for("create"))

    else:
        flash(result[1], "success")

        return redirect(url_for("create"))


@app.route("/post/<post_id>", methods=["GET", "POST"])
def post(post_id):

    post = user.User().find_post(post_id)

    replies = list(user.User().find_replies(post_id))

    return render_template("blog-post.html", post=post, replies=replies[::-1])


@app.route("/like-unlike/<post_id>", methods=["POST"])
def like_unlike(post_id):

    if post_id:
        res = user.User().like_unlike(post_id)

    return (res, 200)


@app.route("/reply/<post_id>", methods=["POST"])
def reply(post_id):

    result = user.User().reply(post_id)

    print(result)

    return redirect(url_for("post", post_id=post_id))


@app.route("/profile/", methods=["GET", "POST"])
def profile():
    profile = user.User().find_user()

    preferences = user.User().get_preferences()

    print(preferences)

    return render_template(
        "profile.html",
        data=profile,
        country_tags=preferences[:10],
        league_tags=preferences[10:],
    )


@app.route("/add_preferences", methods=["GET", "POST"])
def add_preferences():
    print(user.User().add_preferences())

    return "Hello World"


@app.route("/update_preferences/", methods=["GET", "POST"])
def updatePreferences():

    result = user.User().updatePreference()

    if result[0]:

        flash(result[1], "success")

    else:

        flash(result[1], "warning")

    return redirect(url_for("profile"))


if __name__ == "__main__":

    app.run(debug=True)