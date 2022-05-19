import json
import os
import subprocess

import flask
from flask import current_app as app

connect_str = os.environ["THEAI_STORAGE_CONNECTION_STRING"]


@app.route("/")
def message() -> str:
    text = "Hello, World!"

    return flask.render_template("index.html", text=text)
