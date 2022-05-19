import json
import os

from flask import Flask


# deploy 1
def init_app():
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = "secretkey"  # Change this.

    with app.app_context():
        from . import routes

        return app
