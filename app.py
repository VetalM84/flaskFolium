"""File for run the app."""

import os

from maps import create_app

app = create_app(os.getenv("FLASK_CONFIG", "default"))

app.run()
