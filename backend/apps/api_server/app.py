from os import environ

from fastapi import FastAPI

from backend.apps.api_server import hello_routes, health_routes

def build_app_from_env() -> FastAPI:
    return build_app(
        message=environ.get("MESSAGE", "Hello, World!"),
    )

def build_app(message: str) -> FastAPI:
    api = FastAPI()
    api.include_router(hello_routes.router(message), prefix="/api")
    api.include_router(health_routes.router(), prefix="/api")
    return api
