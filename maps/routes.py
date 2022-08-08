"""Store all routes."""

import re
from datetime import datetime

import folium
from flask import render_template, request, flash, abort
from folium.features import LatLngPopup
from folium.plugins import Fullscreen, LocateControl, MarkerCluster

from maps import app
from maps.forms import LocationForm
from maps.ip import ip_white_list


@app.before_request
def ip_limit_access():
    """Limit access ip addresses to the app before every URL request."""
    if request.remote_addr not in ip_white_list:
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
    marker_cluster = MarkerCluster().add_to(current_map)
    # folium.LayerControl().add_to(current_map)

    # for testing purposes'
    # marker_locs = [[random.uniform(44, 52), random.uniform(22, 40)] for x in range(400)]
    # for pnt in marker_locs:
    #     folium.Marker(
    #         location=[pnt[0], pnt[1]],
    #         popup=f"pnt - {pnt[0]}, {pnt[1]}",
    #         icon=folium.Icon(color="red", icon="info-sign"),
    #         tooltip="tooltip",
    #     ).add_to(marker_cluster)

    if request.method == "POST" and form.validate_on_submit():
        location = form.coordinates.data
        color = form.color.data
        # comment = form.comment.data

        parsed_coordinates = parse_coordinates(coordinates=location)

        try:
            add_marker(
                current_map=marker_cluster,  # add markers on cluster layer
                location=[
                    parsed_coordinates[0],
                    parsed_coordinates[1],
                ],
                color=color,
                popup=datetime.now().strftime("%H:%M"),
            )
        except (ValueError, TypeError) as e:
            flash("Ошибка. Неудалось распознать координаты или они не верны.")
            print(e)
        except IndexError as e:
            flash("Ошибка. Не хватает координат.")
            print(e)

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
    folium.Marker(
        location=location,
        icon=folium.Icon(color=color, icon="exclamation-sign"),
        popup=popup,
        tooltip=popup,
    ).add_to(current_map)
