"""API serve package."""

from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint('api', __name__)
api = Api(
    app=blueprint,
    doc="/api/v1/doc/",
    version="1.0",
    title="Maps API",
    description="Maps API",
    default="Markers",
    default_label="Markers",
)
