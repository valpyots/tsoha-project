from app import app
from flask import render_template, redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import messages, users

@app.route("/")
def index():
    list = messages.get_list()
    return render_template("index.html", count=len(list), topics=list, username = users.username())


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("/register.html", username = users.username())
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if users.signup(username, password, password2):
            return render_template("index.html", message="Registration succesful. You can now login.")
        else:
            return render_template("error.html", message="Registration failed.")

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

@app.route("/newtopic", methods=["POST"])
def newtopic():
    #category = request.form["category"] 
    title = request.form["title"]
    message = request.form["message"]
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html", message="Forbidden")
    if messages.newtopic(title, message):
        return redirect("/")
    else:
        return render_template("error.html", message="Failed to post new topic")

@app.route("/respond/<int:topic>", methods=["GET", "POST"])
def respond(topic):
    list = messages.get_responses(topic)
    title = messages.get_topic_title(topic)
    startmessage = messages.get_topic_message(topic)
    startuser = messages.get_topic_user(topic)
    if request.method == "GET":
        return render_template("respond.html", topic=topic, messages=list, title=title, startuser = startuser, startmessage=startmessage, username=users.username())
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            return render_template("error.html", message="Forbidden")
        else:
            content = request.form["content"]
            if messages.respond(content, topic):
                return redirect("/respond/" + str(topic))
            else:
                return render_template("error.html", message="Failed to post response")

@app.route("/help", methods=["GET"])
def help():
    return render_template("help.html")

@app.route("/hidetopic/<int:topic>", methods=["POST"])
def hidetopic(topic):
    if session["user_id"] == messages.get_topic_user(topic)[0]:
        messages.hide_topic(topic)
        return redirect("/")
    else:
        return render_template("error.html", message="You do not have permission to delete this topic")