"""File for run the app."""

import os

from dotenv import load_dotenv

from maps import create_app

load_dotenv()

app = create_app(os.getenv("FLASK_CONFIG", "default"))
app.app_context().push()

if __name__ == "__main__":
    app.run()
