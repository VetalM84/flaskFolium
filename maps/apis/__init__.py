"""API serve package."""

from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint("api_blueprint", __name__)
api = Api(
    app=api_blueprint,
    doc="/doc/",
    version="1.0",
    title="Maps API",
    description="Maps API",
    default="Markers",
    default_label="Markers",
)
