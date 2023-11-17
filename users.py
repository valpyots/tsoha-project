from flask import Flask
from flask import render_template, redirect, request, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from sqlalchemy.sql import text
import secrets

def signup(username, password, password2, visibility):
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        if password != password2:
            return False
        hash_value = generate_password_hash(password)
        try:
            sql = text("INSERT INTO users (username, password, profileVisible, canPost, isAdmin) VALUES (:username, :password, :profileVisible, true, false)")
            db.session.execute(sql, {"username":username, "password":hash_value, "profileVisible":visibility})
            db.session.commit()
        except:
            return False
        return True

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False


def logout():
    del session["user_id"]
    return redirect("/")

def user_id():
    return session.get("user_id", 0)

def username():
    user_id = session.get("user_id", 0)
    sql = text("SELECT username FROM users WHERE users.id=:user_id")
    username = db.session.execute(sql, {"user_id":user_id}).fetchone()
    return username

def get_username(user_id):
    sql = text("SELECT U.username FROM Users U WHERE U.id = :user_id")
    res = db.session.execute(sql, {"user_id":user_id}).fetchone()
    return res

def get_user_topics(user_id):
    sql = text("SELECT T.title, T.message, T.id FROM Topics T WHERE T.user_id = :user_id AND T.visible = true")
    res = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return res

def admin_get_user_topics(user_id):
    sql = text("SELECT T.title, T.message, T.id FROM Topics T WHERE T.user_id = :user_id")
    res = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return res

def get_profile_visibility(user_id):
    sql = text("SELECT U.profileVisible FROM Users U WHERE U.id = :user_id")
    res = db.session.execute(sql, {"user_id":user_id}).fetchone()
    try:
        return bool(res[0])
    except:
        return False