import folium
from folium.plugins import Fullscreen, LocateControl
from folium.features import LatLngPopup
from flask import Flask, render_template
from forms import LocationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


@app.route('/about/')
def about():
    """About page."""
    return render_template('about.html')


@app.route('/')
def index():
    """Index page."""
    form = LocationForm()
    start_location = (49.98841410732452, 36.23353094883754)
    maps = folium.Map(location=start_location, zoom_start=12)
    Fullscreen(position="topright", title="Полный экран", title_cancel="Выход").add_to(maps)
    LatLngPopup().add_to(maps)
    LocateControl(auto_start=False, position="topright", strings={"title": "Где я"}).add_to(maps)

    # folium.Marker(
    #     location=(49.98841410732452, 36.23353094883754),
    #     icon=folium.Icon(color="red", icon="info-sign"),
    #     popup="popup",
    #     tooltip="tooltip",
    # ).add_to(maps)

    return render_template('index.html', form=form, maps=maps._repr_html_())


if __name__ == '__main__':
    app.run()
