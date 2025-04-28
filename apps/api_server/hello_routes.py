from dataclasses import dataclass

from fastapi import APIRouter

router = APIRouter()

@dataclass
class HelloResponse:
    message: str

@router.get("/api/hello")
def say_hello() -> HelloResponse:
    return HelloResponse("Hello, World!")
