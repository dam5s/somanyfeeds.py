import unittest

from starlette.testclient import TestClient

from backend.apps.api_server.app import build_app


class TestHealthRoutes(unittest.TestCase):
    def test_check_health(self) -> None:
        app = build_app(message="")
        client = TestClient(app)

        response = client.get("/api/health")

        self.assertEqual(200, response.status_code)
        self.assertEqual({"status": "ok"}, response.json())


if __name__ == "__main__":
    unittest.main()
