from typing import Optional
import asyncio
from pathlib import Path
from datetime import datetime
import json

import typer
from websockets.asyncio.client import connect

from notes_sync.clients.api import AuthenticatedClient, Client
from notes_sync.clients.api.api.account import (
    get_config_api_v1_config_get,
    put_config_api_v1_config_put,
)
from notes_sync.clients.api.api.authorization import auth_api_v1_oauth2_auth_post
from notes_sync.clients.api.models import (
    BodyAuthApiV1Oauth2AuthPost,
    ConfigLogsequenceEnable,
    ConfigPutRequest,
)
from notes_sync.config import get_settings

from .logsequence import Journal


app = typer.Typer()


def fill_settings(
    url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    path: Optional[Path] = None,
    date_format: Optional[str] = None,
    time_format: Optional[str] = None,
):
    settings = get_settings()
    if url is None:
        url = f"http://{settings.API_HOST}:{settings.API_PORT}"
    if username is None:
        username = settings.LOGSEQUENCE_USERNAME
    if password is None:
        password = settings.LOGSEQUENCE_PASSWORD
    if path is None:
        path = settings.LOGSEQUENCE_JOURNALS_PATH
    if date_format is None:
        date_format = settings.LOGSEQUENCE_FILE_FORMAT
    if time_format is None:
        time_format = settings.LOGSEQUENCE_TIME_FORMAT
    return {
        "url": url,
        "username": username,
        "password": password,
        "path": path,
        "date_format": date_format,
        "time_format": time_format,
    }


async def fetch_main(token: str, settings: dict, reconnection_timeout: int):
    while True:
        try:
            async with connect(
                get_settings().logsequence_uri(token), open_timeout=30
            ) as websocket:
                while True:
                    messages = await websocket.recv()
                    messages = json.loads(messages)["messages"]
                    now = datetime.now()
                    for message in messages:
                        journal = Journal(
                            settings["path"],
                            now,
                            settings["date_format"],
                            settings["time_format"],
                        )
                        journal.write_message(now, message["text"])
        except Exception:
            pass
        await asyncio.sleep(reconnection_timeout)


def get_token(settings, client: Client) -> str:
    response = auth_api_v1_oauth2_auth_post.sync(
        client=client,
        body=BodyAuthApiV1Oauth2AuthPost(
            username=settings["username"], password=settings["password"]
        ),
    )
    return response.access_token


@app.command()
def config_get(
    url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
):
    settings = fill_settings(url, username, password)
    client = Client(base_url=settings["url"])
    with client as client:
        access_token = get_token(settings, client)
    client = AuthenticatedClient(base_url=settings["url"], token=access_token)
    with client as client:
        response = get_config_api_v1_config_get.sync(client=client)
        print(response.config)


@app.command()
def config_update(
    logsequence_enable: bool,
    url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
):
    settings = fill_settings(url, username, password)
    client = Client(base_url=settings["url"])
    with client as client:
        access_token = get_token(settings, client)
    client = AuthenticatedClient(base_url=settings["url"], token=access_token)
    with client as client:
        response = put_config_api_v1_config_put.sync(
            client=client,
            body=ConfigPutRequest(
                config=[
                    ConfigLogsequenceEnable(
                        name="logsequence.enable", value=logsequence_enable
                    )
                ]
            ),
        )
        print(response)


@app.command()
def main(
    reconnection_timeout: int = 5,
    url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    path: Optional[Path] = None,
    date_format: Optional[str] = None,
    time_format: Optional[str] = None,
):
    settings = fill_settings(url, username, password, path, date_format, time_format)
    client = Client(base_url=settings["url"])
    with client as client:
        access_token = get_token(settings, client)
        asyncio.run(fetch_main(access_token, settings, reconnection_timeout))


if __name__ == "__main__":
    app()
