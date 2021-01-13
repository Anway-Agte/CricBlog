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
from app import mongo, bcrypt
import uuid
import re
import random


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
            "preferences": [],
            "posts": [],
            "token": random.randint(11111, 99999),
            "verified": False,
        }
        if user["email"] == "":

            return [user, False, "Please enter an email address"]

        elif user["username"] == "":

            return [user, False, "Please enter a username"]

        elif user["password"] == "":

            return [user, False, "Please enter a password"]

        elif user["password"] != user["cpassword"]:

            return [user, False, "Both the passwords should match"]

        elif mongo.db.users.find_one({"username": user["username"]}):

            return [user, False, "This username has already been taken"]

        elif mongo.db.users.find_one({"email": user["email"]}):

            return [user, False, "An account with this email address already exists"]

        elif not re.match(pattern, user["password"]):

            return [
                user,
                False,
                "Your password must contain :  1) 6-20 characters  2) Atleast one digit  3) Atleast one uppercase and lowercase symbol  4) One special character",
            ]

        else:
            del user["cpassword"]

            hashed_pw = bcrypt.generate_password_hash(user["password"]).decode("utf-8")

            user["password"] = hashed_pw

            print(user)

            mongo.db.users.insert_one(user)

            return [user, True]

    def login(self):

        credentials = {
            "email": request.form.get("email"),
            "password": request.form.get("password"),
        }
        if credentials["email"] == "":

            return [False, "Please enter an email address"]

        elif credentials["password"] == "":

            return [False, "Please enter a password"]

        else:
            user = mongo.db.users.find_one({"email": credentials["email"]})

            if not user:

                return [
                    False,
                    "The email you have entered is invalid . Please sign up before logging in",
                ]

            elif bcrypt.check_password_hash(user["password"], credentials["password"]):

                session["logged_in"] = True

                session["_id"] = user["_id"]

                if request.form.get("remember") == "on":

                    session.permanent = True

                return [True, "Logged in successfully!"]

            else:

                return [False, "Wrong password please try again ."]
