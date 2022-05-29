import datetime
import json
import logging
import os
import random

import azure.functions as func
from azure.storage.blob import BlobServiceClient
from requests import Session

from ..config.prompts import PROMPTS

BASE_URL = os.environ["BASE_URL"]
TOKEN = os.environ["TOKEN"]
THEAI_APP_STORAGE_CONNECTION_STRING = os.environ[
    "THEAI_APP_STORAGE_CONNECTION_STRING"
]


def build_data_string(prompt, temperature, max_tokens) -> str:
    return f'{{"prompt": "{prompt}", "temperature": {temperature}, "max_tokens": {max_tokens}}}'


def main(gpt3: func.TimerRequest) -> None:

    session = Session()
    session.headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }

    prompt = random.choice(PROMPTS)

    data = build_data_string(prompt, 0, 20)

    r = session.post(BASE_URL, data=data)
    r.raise_for_status()

    response_data = json.dumps(r.json())
    prompt_data = json.dumps(prompt)

    try:

        blob_service_client = BlobServiceClient.from_connection_string(
            THEAI_APP_STORAGE_CONNECTION_STRING
        )
        container_name = "theaiapp"
        blobs = [response_data, prompt_data]
        names = ["response.json", "prompt.json"]

        for blob, name in zip(blobs, names):
            blob_client = blob_service_client.get_blob_client(
                container=container_name, blob=name
            )
            blob_client.upload_blob(blob, overwrite=True)

    except Exception as e:
        error = e
        pass
