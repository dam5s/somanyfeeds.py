from typing import Optional

from fastapi.testclient import TestClient

from backend.apps.api_server.app import build_app
from backend.apps.api_server.app_dependencies import AppDependencies


def build_test_client(
    dependencies: Optional[AppDependencies] = None,
) -> TestClient:
    dependencies = dependencies or AppDependencies.defaults()

    # pyrefly: ignore
    return TestClient(build_app(dependencies))
