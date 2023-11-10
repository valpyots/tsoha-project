from app import app
from flask import render_template, redirect, request
from werkzeug.security import check_password_hash, generate_password_hash
import messages, users

@app.route("/")
def index():
    list = messages.get_list()
    return render_template("index.html", count=len(list), messages=list, username = users.username())


@app.route("/signup", methods=["GET", "POST"])
def signup():
    users.signup()
    return render_template("/register.html", username = users.username())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="User not found. Check username and password.")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if messages.send(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Posting failed")
