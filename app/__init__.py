import json
import os

from flask import Flask

SECRET = os.environ["SECRET_KEY"]


def init_app():
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = SECRET

    with app.app_context():
        from . import routes

        return app
