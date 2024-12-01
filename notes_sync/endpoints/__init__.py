from notes_sync.endpoints.config import api_router as config_router
from notes_sync.endpoints.health_check import api_router as health_check_router
from notes_sync.endpoints.messages import api_router as messages_router
from notes_sync.endpoints.oauth2 import api_router as oauth2_router

list_of_routes = [config_router, health_check_router, messages_router, oauth2_router]


__all__ = ["list_of_routes"]
