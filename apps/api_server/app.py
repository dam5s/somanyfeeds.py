from fastapi import FastAPI

from apps.api_server import hello_routes

def build_app() -> FastAPI:
    api = FastAPI()
    api.include_router(hello_routes.router)
    return api

app = build_app()
