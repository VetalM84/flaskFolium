"""Initialization of the app."""

import logging
import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s %(levelname)s %(name)s : %(message)s"
)
app = Flask(__name__)
apis = Api(app)
cache = Cache(app, config={"CACHE_TYPE": "SimpleCache"})

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgres://", "postgresql://", 1
    )
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from maps import routes
from maps.api.v1 import endpoints

db.create_all()
