"""Initialization of the app."""

import logging
import os

from flask import Flask
from flask_caching import Cache

from .apis import blueprint

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s %(levelname)s %(name)s : %(message)s"
)
app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "SimpleCache"})

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

app.register_blueprint(blueprint, url_prefix='/api/v1')

from maps import routes

from maps.apis import api_v1
