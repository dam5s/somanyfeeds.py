from dataclasses import dataclass

from fastapi import APIRouter


@dataclass
class HealthResponse:
    status: str


def router() -> APIRouter:
    api = APIRouter()

    @api.get("/health")
    def check_health() -> HealthResponse:
        return HealthResponse("ok")

    return api
