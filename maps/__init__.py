"""Initialization of the app."""

import logging

from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})


def create_app(config_name):

    logging.basicConfig(
        level=logging.WARNING, format="%(asctime)s %(levelname)s %(name)s : %(message)s"
    )

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    cache.init_app(app)

    from maps import routes
    from maps.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .apis import api_blueprint
    from maps.apis import api_v1

    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    return app
