from flask import Flask
from flask import render_template, redirect, request, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from sqlalchemy.sql import text

def signup():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            return render_template("error.html", message="Passwords do not match. Please try again.")
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (name, password) VALUES (:name, :password)")
        db.session.execute(sql, {"name":username, "password":hash_value})
        db.session.commit()
        return redirect("/")

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE name=:name")
    result = db.session.execute(sql, {"name":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False


def logout():
    del session["user_id"]
    return redirect("/")