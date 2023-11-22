from flask import Flask
from flask import render_template, redirect, request, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from sqlalchemy.sql import text
import secrets
from datetime import datetime

#Function for registration functionality
def register(username, password, password2, visibility):
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        if password != password2:
            return False
        hash_value = generate_password_hash(password)
        try:
            sql = text("INSERT INTO users (username, password, privacy) VALUES (:username, :password, :visibility)")
            db.session.execute(sql, {"username":username, "password":hash_value, "visibility":visibility})
            db.session.commit()
        except:
            return False
        return True

#Function allows registered users to log in, creating an user session. CSRF session is also created for security.
def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    res = db.session.execute(sql, {"username":username})
    user = res.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

#Function deletes user session
def logout():
    del session["user_id"]
    del session["csrf_token"]
    return redirect("/")

#Function returns current user session user's id
def user_id():
    return session.get("user_id", 0)

#Function return current user session users's username
def username():
    user_id = session.get("user_id", 0)
    sql = text("SELECT username FROM users WHERE users.id=:user_id")
    username = db.session.execute(sql, {"user_id":user_id}).fetchone()
    return username

#Function returns username for given user id
def get_username(user_id):
    sql = text("SELECT U.username FROM Users U WHERE U.id = :user_id")
    res = db.session.execute(sql, {"user_id":user_id})
    return res.fetchone()

#Function returns all non-deleted topics posted by the user
def get_user_topics(user_id):
    sql = text("SELECT DISTINCT T.title, T.message, T.id, C.name, C.id FROM Topics T, Categories C, deletedtopics D WHERE T.user_id = :user_id AND T.id NOT IN (SELECT topicid FROM deletedtopics WHERE topicid IS NOT NULL) AND T.categoryid = C.id ORDER BY T.id DESC")
    res = db.session.execute(sql, {"user_id":user_id})
    return res.fetchall()

#Function return all topis postes by user, even deleted ones
def admin_get_user_topics(user_id):
    sql = text("SELECT T.title, T.message, T.id, C.name, C.id FROM Topics T, Categories C WHERE T.user_id = :user_id AND T.categoryid = C.id ORDER BY T.id DESC")
    res = db.session.execute(sql, {"user_id":user_id})
    return res.fetchall()

#Function returns boolean value for whether or not a given user's profile is private
def get_profile_visibility(user_id):
    sql = text("SELECT U.privacy FROM Users U WHERE U.id = :user_id")
    res = db.session.execute(sql, {"user_id":user_id}).fetchone()
    if res[0] == 0:
        return True
    elif res[0] == 1:
        return False
    else:
        return "breaks"

#Function returns boolean value for whether or not a given user is an admin user
def get_admin_status(user_id):
    sql = text("SELECT A.user_id FROM Admins A WHERE :user_id IN (SELECT user_id from admins)")
    res = db.session.execute(sql, {"user_id":user_id}).fetchone()
    if res == None:
        return False
    else:
        return True
    
#Function to check if an user is allowed to post.
def get_can_post(user_id):
    sql = text("SELECT B.banactive FROM bans B WHERE B.user_id = :user_id ORDER BY B.id DESC")
    res = db.session.execute(sql, {"user_id":user_id}).fetchone()
    try:
        if bool(res[0]) == False:
            return True
        elif bool(res[0]) == True:
            return False
    except:
        return True

#Function for admins to ban users from posting
def admin_ban_user(user_id):
    sql = text("INSERT INTO bans (user_id, bandate, banend, banactive) VALUES (:user_id, NOW(), :banend, true)")
    db.session.execute(sql, {"user_id": user_id, "banend":datetime(2999,1,1,0,0,0)})
    db.session.commit()
    return True

#Function for admins to unban users from posting
def admin_unban_user(user_id):
    sql = text("UPDATE bans SET banactive = false WHERE user_id = :user_id")
    db.session.execute(sql, {"user_id": user_id})
    db.session.commit()
    return True