from flask import Flask      # request and redirect are needed on 'POST' routes; session keeps track the amount of times the page has been visited; session is an empty dictionary
from flask_app import app       #Importing app variable from __init__.py
from flask_app.controllers import todo_controller, user_controller  #Import all controllers in controllers folder


if __name__ == "__main__":
    app.run(debug = True)
# This code is needed to run your environment and be in an active state when you run this file.
