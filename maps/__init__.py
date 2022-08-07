"""Initialization of the app."""

import os

from flask import Flask

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

from maps import routes
