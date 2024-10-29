import uvicorn
from fastapi import FastAPI

from notes_sync.logger import Logger
from notes_sync.utils import get_settings

app = FastAPI()


def start():
    settings = get_settings()
    Logger.info(f"Listening on {settings.APP_HOST}:{settings.APP_PORT}")
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)


def main():
    start()


if __name__ == "__main__":
    main()
