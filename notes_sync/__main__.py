import uvicorn
from fastapi import FastAPI

from notes_sync.config import DefaultSettings, get_settings
from notes_sync.endpoints import list_of_routes
from notes_sync.utils import get_hostname

settings = get_settings()


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    application = FastAPI(docs_url="/docs")
    bind_routes(application, settings)
    return application


app = get_app()


if __name__ == "__main__":
    uvicorn.run(
        "notes_sync.__main__:app",
        host=get_hostname(settings.APP_HOST),
        port=settings.APP_PORT,
        reload=True,
    )
