"""Store all routes."""

import folium
from flask import render_template
from folium.features import LatLngPopup
from folium.plugins import Fullscreen, LocateControl

from maps import app
from maps.forms import LocationForm


@app.route('/about/')
def about():
    """About page."""
    return render_template('about.html')


@app.route('/', methods=('GET', 'POST'))
def index():
    """Index page. Showing map with markers and form to add new marker."""
    form = LocationForm()
    start_location = (49.98841410732452, 36.23353094883754)
    m = folium.Map(location=start_location, zoom_start=12)
    Fullscreen(position="topright", title="Полный экран", title_cancel="Выход").add_to(m)
    LatLngPopup().add_to(m)
    LocateControl(auto_start=False, position="topright", strings={"title": "Где я"}).add_to(m)

    if form.validate_on_submit():
        location = form.coordinates.data.split(',')
        color = form.color.data
        comment = form.comment.data

        add_marker(
            m=m,
            location=(float(location[0]), float(location[1])),  # location=[45.5, -122.3]
            color=color,
            popup=comment,
        )

    return render_template('index.html', form=form, maps=m._repr_html_())


def add_marker(m, location, color, popup):
    """Add marker to map."""
    folium.Marker(
        location=location,
        icon=folium.Icon(color=color, icon="info-sign"),
        popup=popup,
        tooltip=popup,
    ).add_to(m)
