"""Initialization of the app."""

import logging
import os

from flask import Flask
from flask_caching import Cache
from flask_restx import Api

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s %(levelname)s %(name)s : %(message)s"
)
app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "SimpleCache"})

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

from maps import routes

apis = Api(
    app=app,
    doc="/api/v1/doc/",
    version="1.0",
    title="Maps API",
    description="Maps API",
    default="Markers",
    default_label="Markers",
)
from maps.api.v1 import routes
