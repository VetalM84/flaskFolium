"""API endpoints for the maps' app."""

from datetime import datetime

from flask import request, jsonify
from flask_restful import Resource

from maps import apis
from maps.routes import get_all_markers, to_date


class Report(Resource):
    """Report resource from Report DB model."""

    def get(self):
        """
        Retrieve all markers with date provided. If not date provided, return all markers by today.
        Use 2022-08-14 arg date format to get all markers from 14 August 2022.
        """
        date_filter_argument = request.args.get(
            "date", default=datetime.today().date(), type=to_date
        )
        return jsonify(get_all_markers(date=date_filter_argument))


apis.add_resource(Report, "/api/v1/markers/")
