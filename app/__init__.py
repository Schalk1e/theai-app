import json
import os

from flask import Flask


def init_app():
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = "610a2ee688cda9e724885e23cd2cfdee"

    with app.app_context():
        from . import routes

        return app
