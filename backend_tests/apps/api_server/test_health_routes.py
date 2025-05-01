import unittest

from starlette.testclient import TestClient

from backend.apps.api_server.app import build_app
from backend_tests.apps.api_server.testing_app_dependencies import build_testing_app_dependencies


class TestHealthRoutes(unittest.TestCase):
    def test_check_health(self) -> None:
        app = build_app(build_testing_app_dependencies())
        client = TestClient(app)

        response = client.get("/api/health")

        self.assertEqual(200, response.status_code)
        self.assertEqual({"status": "ok"}, response.json())


if __name__ == "__main__":
    unittest.main()
