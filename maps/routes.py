"""Store all routes."""

import re
from datetime import datetime

import folium
import pytz
from flask import render_template, request, flash, abort
from folium.features import LatLngPopup
from folium.plugins import Fullscreen, LocateControl, MarkerCluster

from maps import app, db
from maps.forms import LocationForm
from maps.ip import ip_white_list
from maps.models import Report


@app.before_request
def ip_limit_access():
    """Limit access ip addresses to the app before every URL request."""
    if not request.remote_addr.startswith(ip_white_list):
        print("Blocked: ", request.remote_addr)
        abort(403)


@app.route("/about/")
def about():
    """About page."""
    return render_template("about.html")


@app.route("/", methods=("GET", "POST"))
def index():
    """Index page. Showing map with markers and form to add new marker."""
    form = LocationForm()
    start_location = (50.45, 30.52)  # Ukraine
    current_map = folium.Map(location=start_location, zoom_start=6)

    # Map control buttons and plugins
    Fullscreen(position="topright", title="Полный экран", title_cancel="Выход").add_to(
        current_map
    )
    LocateControl(
        auto_start=False, position="topright", strings={"title": "Где я"}
    ).add_to(current_map)
    LatLngPopup().add_to(current_map)
    marker_cluster = MarkerCluster().add_to(current_map)
    # folium.LayerControl().add_to(current_map)

    # Add all markers to the map if request method is GET
    for marker in get_all_markers():
        tz_time = marker.created_at + pytz.timezone("Europe/Kiev").utcoffset(
            datetime.now()
        )

        add_marker(
            current_map=marker_cluster,
            location=(marker.latitude, marker.longitude),
            color=marker.color,
            popup=tz_time.strftime("%H:%M"),
        )

    if request.method == "POST" and form.validate_on_submit():
        location = form.coordinates.data
        color = form.color.data
        # comment = form.comment.data

        parsed_coordinates = parse_coordinates(coordinates=location)

        # save to DB
        add_report_to_db(
            latitude=parsed_coordinates[0],
            longitude=parsed_coordinates[1],
            color=color,
        )

        # add marker to the map
        add_marker(
            current_map=marker_cluster,  # add markers on cluster layer
            location=[
                parsed_coordinates[0],
                parsed_coordinates[1],
            ],
            color=color,
            popup=datetime.now().strftime("%H:%M"),
        )

    return render_template("index.html", form=form, maps=current_map._repr_html_())


def parse_coordinates(coordinates: str):
    """Parse coordinates gotten from html form. Return a list of coordinates."""
    coordinates_cleaned = "".join(
        e for e in coordinates.strip() if e.isdigit() or e in (",", ".", " ")
    )
    coordinates_cleaned = (
        coordinates_cleaned.strip()
        .replace(", ", ",")
        .replace("  ", ",")
        .replace(" ", ",")
    )
    for item in coordinates_cleaned.split(","):
        if re.fullmatch(r"\d{2}\.\d{2,}", item) is None:
            # flash("Ошибка. Неудалось распознать координаты или они не верны.")
            return False
    print(coordinates_cleaned)
    return coordinates_cleaned.split(",")


def add_marker(current_map: object, location, color: str, popup: str):
    """Add a marker to the map."""
    try:
        folium.CircleMarker(
            location=location,
            # icon=folium.Icon(color=color, icon="exclamation-sign"),
            popup=popup,
            tooltip=popup,
            radius=9,
            fill_color=color,
            color="gray",
            fill_opacity=0.6,
        ).add_to(current_map)
    except (ValueError, TypeError) as e:
        flash("Ошибка. Неудалось распознать координаты или они не верны.")
        print(e)
    except IndexError as e:
        flash("Ошибка. Не хватает координат.")
        print(e)


def get_all_markers():
    """Retrieve all records from DB with date == today."""
    today_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    return Report.query.filter(Report.created_at >= today_datetime).all()


def add_report_to_db(
    latitude,
    longitude,
    color: str,
    comment: str = None,
):
    """Add a new report to the DB."""
    try:
        report = Report(
            latitude=float(latitude),
            longitude=float(longitude),
            color=color,
            comment=comment,
            ip=request.remote_addr,
        )
        db.session.add(report)
        db.session.commit()
    except IndexError as e:
        flash("Ошибка. Не хватает координат.")
        print(e)
    except Exception as e:
        flash("Ошибка. Не удалось добавить точку в БД.")
        print(e)
