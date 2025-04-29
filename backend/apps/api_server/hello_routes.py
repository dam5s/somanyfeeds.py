from dataclasses import dataclass

from fastapi import APIRouter


@dataclass
class HelloResponse:
    message: str


def router(message: str) -> APIRouter:
    api = APIRouter()

    @api.get("/hello")
    def say_hello() -> HelloResponse:
        return HelloResponse(message)

    return api
