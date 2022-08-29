"""File for run the app."""

import os

from maps import create_app, db

app = create_app(os.getenv("FLASK_CONFIG") or "default")


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)


app.run()
