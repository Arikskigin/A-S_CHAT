from flask import render_template, url_for, redirect, request, session, jsonify, flash, Blueprint
from Web_Chat.application.local_database import DataBase

view = Blueprint("views", __name__)

# GLOBAL CONSTANTS
NAME_KEY = 'name'
MSG_LIMIT = 30


# VIEWS


@view.route("/login", methods=["POST", "GET"])
def login():
    """
    :exception POST
    :return: None
    """
    if request.method == "POST":  # if user input a name
        name = request.form["inputName"]
        if len(name) >= 2:
            session[NAME_KEY] = name
            flash(f'You were successfully logged in as {name}.')
            return redirect(url_for("views.home"))
        else:
            flash(" Your name must be longer than 1 character.")

    return render_template("login.html", **{"session": "session"})


@view.route("/logout")
def logout():
    """
    logout for user by removing session(pop)
    :return: None
    """
    session.pop(NAME_KEY, None)
    flash("You were logged out.")
    return redirect(url_for("views.login"))


@view.route("/")
@view.route("/home")
def home():
    """
    if logged in-display home page
    :return: None
    """
    if NAME_KEY not in session:
        return redirect(url_for("views.login"))

    return render_template("index.html", **{"session": session})


@view.route("/history")
def history():
    if NAME_KEY not in session:
        flash("Please login first")
        return redirect(url_for("views.login"))

    json_messages = get_history(session[NAME_KEY])
    print(json_messages)
    return render_template("history.html", **{"history": json_messages})


@view.route("/get_name")
def get_name():
    """
    :return: a json object storing name of logged in user
    """
    data_name = {"name": ""}
    if NAME_KEY in session:
        data_name = {"name": session[NAME_KEY]}
    return jsonify(data_name)


@view.route("/get_messages")
def get_messages():
    """
    :return: all messages stored in database
    """
    DB = DataBase()
    messages = DB.get_all_messages(MSG_LIMIT)
    messages_format = remove_seconds_from_messages(messages)

    return jsonify(messages_format)


@view.route("/get_history")
def get_history(your_name):
    """
    :param your_name:
    :return: all messages by name
    """
    DB = DataBase()
    messages = DB.get_messages_by_name(your_name)
    messages_format = remove_seconds_from_messages(messages)

    return messages_format


# UTILITIES
def remove_seconds_from_messages(messages):
    """
    func to remove secs from messages
    :param messages:

    :return: list
    """
    list_messages = []
    for msg in messages:
        message = msg
        message["time"] = remove_seconds(message["time"])
        list_messages.append(message)

    return list_messages


def remove_seconds(message):

    return message.split(".")[0][:-3]