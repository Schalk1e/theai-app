import json
import os
import subprocess
from http.client import CONTINUE

import flask
from azure.storage.blob import BlobServiceClient
from flask import current_app as app

THEAI_APP_STORAGE_CONNECTION_STRING = os.environ[
    "THEAI_APP_STORAGE_CONNECTION_STRING"
]
CONTAINER = "theaiapp"


@app.route("/")
def message() -> str:

    container_client = BlobServiceClient.from_connection_string(
        THEAI_APP_STORAGE_CONNECTION_STRING
    ).get_container_client(CONTAINER)

    r = []
    for name in ["prompt.json", "response.json"]:
        blob_client = container_client.get_blob_client(name)
        res = json.loads(
            blob_client.download_blob()
            .readall()
            .decode("utf8")
            .replace("'", '"')
        )
        r.append(res)

    return flask.render_template(
        "index.html", text=r[0] + " " + r[1]["choices"][0]["text"]
    )
