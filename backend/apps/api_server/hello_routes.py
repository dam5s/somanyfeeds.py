from dataclasses import dataclass

from fastapi import APIRouter


@dataclass
class HelloResponse:
    message: str


def router() -> APIRouter:
    api = APIRouter()

    @api.get("/hello")
    def say_hello() -> HelloResponse:
        return HelloResponse("Hello, World!")

    return api
