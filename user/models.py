from flask import (
    Flask,
    render_template,
    session,
    redirect,
    request,
    url_for,
    flash,
    Response,
    jsonify,
)
from app import mongo
import uuid
import re


class User:
    def signup(self):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pattern = re.compile(reg)
        user = {
            "_id": uuid.uuid4().hex,
            "email": request.form.get("email"),
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "cpassword": request.form.get("cpassword"),
        }
        if user["email"] == "":

            return [False, "Please enter an email address"]

        elif user["username"] == "":

            return [False, "Please enter a username"]

        elif user["password"] == "":

            return [False, "Please enter a password"]

        elif user["password"] != user["cpassword"]:

            return [False, "Both the passwords should match"]

        elif mongo.db.users.find_one({"username": user["username"]}):

            return [False, "This username has already been taken"]

        elif mongo.db.users.find_one({"email": user["email"]}):

            return [False, "An account with this email address already exists"]

        elif not re.match(pattern, user["password"]):

            return [
                False,
                "Your password must contain :  1) 6-20 characters  2) Atleast one digit  3) Atleast one uppercase and lowercase symbol  4) One special character",
            ]

        else:

            mongo.db.users.insert_one(user)

            return [True, "This seems correct"]
