from flask_app import app # this line allows us to use the app to create routes
from flask import render_template, redirect, session

@app.route("/")
def home():
    if session.get("user_id"):
        return redirect("/dashboard")
    return render_template("index.html")
