"""Store all routes."""

import re
from datetime import datetime

import folium
import pytz
from flask import render_template, request, flash
from folium.features import LatLngPopup
from folium.plugins import Fullscreen, LocateControl
from jinja2 import Template
from sqlalchemy import func

from maps import app, db, cache
from maps.forms import LocationForm
from maps.models import Report


@app.route("/about/")
@cache.cached(timeout=3600)
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

    # Rewrite the default popup text to use custom popup with only coordinates
    popup = LatLngPopup()
    popup._template = Template(
        """
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.popup();
                function latLngPop(e) {
                    {{this.get_name()}}
                        .setLatLng(e.latlng)
                        .setContent(e.latlng.lat.toFixed(4) + ", " + e.latlng.lng.toFixed(4))
                        .openOn({{this._parent.get_name()}});
                        parent.document.getElementById("coordinates").value = 
                        e.latlng.lat.toFixed(4) + "," + e.latlng.lng.toFixed(4);
                    }
                {{this._parent.get_name()}}.on('click', latLngPop);
            {% endmacro %}
            """
    )
    popup.add_to(current_map)

    # marker_cluster = MarkerCluster().add_to(current_map)
    # folium.LayerControl().add_to(current_map)

    filter_date = request.args.get(
        "date", default=datetime.today().date(), type=to_date
    )

    # Add all markers to the map if request method is GET
    for marker in get_all_markers(date=filter_date):
        tz_time = marker.created_at + pytz.timezone("Europe/Kiev").utcoffset(
            datetime.now()
        )

        add_marker(
            current_map=current_map,
            location=(marker.latitude, marker.longitude),
            color=marker.color,
            popup=marker.comment if marker.comment else tz_time.strftime("%H:%M"),
            tooltip=tz_time.strftime("%H:%M"),
        )

    if request.method == "POST" and form.validate_on_submit():
        location = form.coordinates.data
        color = form.color.data
        comment = form.comment.data

        parsed_coordinates = parse_coordinates(coordinates=location)

        # save to DB
        add_report_to_db(
            latitude=parsed_coordinates[0],
            longitude=parsed_coordinates[1],
            color=color,
            comment=comment,
        )

        # add marker to the map
        add_marker(
            current_map=current_map,
            location=[
                parsed_coordinates[0],
                parsed_coordinates[1],
            ],
            color=color,
            popup=comment if comment else datetime.now().strftime("%H:%M"),
            tooltip=datetime.now().strftime("%H:%M"),
        )

    return render_template(
        "index.html",
        form=form,
        date=datetime.today().strftime("%d.%m"),
        yesterday=filter_date.strftime("%d.%m.%Y"),
        maps=current_map._repr_html_(),
    )


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


def add_marker(current_map: object, location, color: str, popup: str, tooltip: str):
    """Add a marker to the map."""
    try:
        folium.CircleMarker(
            location=location,
            # icon=folium.Icon(color=color, icon="exclamation-sign"),
            popup=popup,
            tooltip=tooltip,
            radius=7,
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


# @cache.cached(timeout=30, key_prefix="all_markers")
def get_all_markers(date):
    """Retrieve all records from DB filtering by date added."""
    return Report.query.filter(func.date(Report.created_at) == date).all()


def add_report_to_db(latitude, longitude, color: str, comment: str):
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


def to_date(date_string):
    """Convert string from url argument named 'date' to date object."""
    return datetime.strptime(date_string, "%Y-%m-%d").date()
