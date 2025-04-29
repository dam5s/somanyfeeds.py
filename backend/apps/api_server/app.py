from fastapi import FastAPI

from backend.apps.api_server import hello_routes, health_routes


def build_app() -> FastAPI:
    api = FastAPI()
    api.include_router(hello_routes.router(), prefix="/api")
    api.include_router(health_routes.router(), prefix="/api")
    return api


app = build_app()
