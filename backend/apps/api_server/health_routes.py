from dataclasses import dataclass

from fastapi import APIRouter

router = APIRouter()


@dataclass
class HealthResponse:
    status: str


@router.get("/api/health")
def check_health() -> HealthResponse:
    return HealthResponse("ok")
