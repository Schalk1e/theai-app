import datetime
import json
import logging
import os

import azure.functions as func
from azure.storage.blob import BlobServiceClient
from requests import Session

BASE_URL = os.environ["BASE_URL"]
TOKEN = os.environ["TOKEN"]
THEAI_APP_STORAGE_CONNECTION_STRING = os.environ[
    "THEAI_APP_STORAGE_CONNECTION_STRING"
]


def main(gpt3: func.TimerRequest) -> None:

    session = Session()
    session.headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }

    prompt = "Hipster AI startups are dumb because:"

    data = {
        "prompt": prompt,
        "temperature": 0,
        "max_tokens": 10,
    }

    r = session.request("POST", BASE_URL)

    # Manual for now.
    response = {
        "id": "cmpl-GERzeJQ4lvqPk8SkZu4XMIuR",
        "object": "text_completion",
        "created": 1586839808,
        "model": "text-davinci:002",
        "choices": [
            {
                "text": "they never work.",
                "index": 0,
                "logprobs": "null",
                "finish_reason": "length",
            }
        ],
    }

    response_data = json.dumps(response)
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
