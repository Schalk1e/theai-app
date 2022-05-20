import datetime
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

    data = {
        "prompt": "Hipster AI startups are dumb because:",
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

    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            THEAI_APP_STORAGE_CONNECTION_STRING
        )
        container_name = "theaiapp"
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob="response.json"
        )
        blob_client.upload_blob(response)
    except Exception as e:
        error = e
        pass
