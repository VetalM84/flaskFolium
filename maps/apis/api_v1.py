"""API endpoints for the maps' app."""

from flask import request
from flask_restx import Resource, fields, marshal_with

from maps.apis import api
from maps.routes import get_all_markers, to_date, add_report_to_db

get_model = api.model(
    "Report",
    {
        "id": fields.Integer,
        "latitude": fields.Float,
        "longitude": fields.Float,
        "color": fields.String,
        "comment": fields.String,
        "created_at": fields.DateTime(dt_format="rfc822"),
    },
)

post_model = api.model(
    "Report",
    {
        "latitude": fields.Float,
        "longitude": fields.Float,
        "color": fields.String,
        "comment": fields.String(required=False),
    },
)


@api.route("/markers/<string:date>/", methods=["GET"])
class Report(Resource):
    """Report resource from Report DB model."""

    @marshal_with(get_model)
    def get(self, date):
        """
        Retrieve all markers with date provided.
        Use 2022-08-14 arg date format to get all markers from 14 August 2022.
        """
        return get_all_markers(request_date=to_date(date))


@api.route("/markers/", methods=["POST", "PUT"])
class AddReport(Resource):
    """Add Report resource to DB model."""

    @api.doc(responses={201: "Created", 400: "Validation error"})
    @api.expect(post_model)
    @marshal_with(post_model)
    def put(self):
        """POST or PUT method for adding marker to DB."""
        add_report_to_db(
            latitude=request.json["latitude"],
            longitude=request.json["longitude"],
            color=request.json["color"],
            comment=request.json["comment"],
        )
        return request.json, 201
