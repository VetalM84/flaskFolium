"""API endpoints for the maps' app."""

from datetime import datetime

from flask import request
from flask_restx import Resource, fields, marshal_with

from maps import apis
from maps.routes import get_all_markers, to_date

report_model = apis.model(
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


@apis.route("/api/v1/markers/")
class Report(Resource):
    """Report resource from Report DB model."""

    @marshal_with(report_model)
    def get(self):
        """
        Retrieve all markers with date provided. If not date provided, return all markers by today.
        Use 2022-08-14 arg date format to get all markers from 14 August 2022.
        """
        date_filter_argument = request.args.get(
            "date", default=datetime.today().date(), type=to_date
        )
        return get_all_markers(request_date=date_filter_argument)
