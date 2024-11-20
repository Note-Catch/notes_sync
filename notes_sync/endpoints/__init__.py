from notes_sync.endpoints.health_check import api_router as health_check_router
from notes_sync.endpoints.oauth2 import api_router as oauth2_router

list_of_routes = [health_check_router, oauth2_router]


__all__ = ["list_of_routes"]
