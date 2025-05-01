import unittest

from starlette.testclient import TestClient

from backend_tests.apps.api_server.testing_app import build_testing_app


class TestHealthRoutes(unittest.TestCase):
    def test_check_health(self) -> None:
        app = build_testing_app()
        client = TestClient(app)

        response = client.get("/api/health")

        self.assertEqual(200, response.status_code)
        self.assertEqual({"status": "ok"}, response.json())


if __name__ == "__main__":
    unittest.main()
