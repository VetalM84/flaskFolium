"""API endpoints for the maps app."""
from datetime import datetime

from flask import request, jsonify

from maps import app
from maps.routes import get_all_markers, to_date


@app.route("/api/v1/markers/", methods=["GET"])
def get_markers():
    """Retrieve all markers with date provided. If not date provided, return all markers by today."""
    date_filter_argument = request.args.get(
        "date", default=datetime.today().date(), type=to_date
    )
    return jsonify(get_all_markers(date=date_filter_argument))
