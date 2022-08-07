"""Store all routes."""

from datetime import datetime

import folium
import re
from flask import render_template, request, flash
from folium.features import LatLngPopup
from folium.plugins import Fullscreen, LocateControl, Search

from maps import app
from maps.forms import LocationForm


@app.route("/about/")
def about():
    """About page."""
    return render_template("about.html")


@app.route("/", methods=("GET", "POST"))
def index():
    """Index page. Showing map with markers and form to add new marker."""
    form = LocationForm()
    start_location = (50.45, 30.52)
    current_map = folium.Map(location=start_location, zoom_start=6)

    # Map control buttons and plugins
    Fullscreen(position="topright", title="Полный экран", title_cancel="Выход").add_to(
        current_map
    )
    LocateControl(
        auto_start=False, position="topright", strings={"title": "Где я"}
    ).add_to(current_map)
    LatLngPopup().add_to(current_map)
    # Search().add_to(current_map)

    if request.method == "POST" and form.validate_on_submit():
        location = form.coordinates.data
        color = form.color.data
        # comment = form.comment.data

        parsed_coordinates = parse_coordinates(coordinates=location)

        add_marker(
            current_map=current_map,
            location=[
                parsed_coordinates[0],
                parsed_coordinates[1],
            ],
            color=color,
            popup=datetime.now().strftime("%H:%M"),
        )

    return render_template("index.html", form=form, maps=current_map._repr_html_())


def parse_coordinates(coordinates: str):
    """Parse coordinates gotten from html form. Return a tuple of coordinates."""
    coordinates_list = []
    for item in coordinates.strip():
        if item in (",", ".", " ") or item.isdigit():
            coordinates_list.append(item)
    coordinates_cleaned = (
        "".join(coordinates_list)
        .strip()
        .replace(", ", ",")
        .replace("  ", ",")
        .replace(" ", ",")
    )
    for item in coordinates_cleaned.split(","):
        if re.fullmatch(r"\d{2}\.\d{2,}", item) is None:
            flash("Ошибка. Неудалось распознать координаты или они не верны.")
            break
    print(coordinates_cleaned)
    print(float(coordinates_cleaned[0]))
    print(float(coordinates_cleaned[1]))
    return coordinates_cleaned.split(",")


def add_marker(
    current_map: object, location, color: str, popup: str
):
    """Add a marker to the map."""
    folium.Marker(
        location=location,
        icon=folium.Icon(color=color, icon="info-sign"),
        popup=popup,
        tooltip=popup,
    ).add_to(current_map)
