import unittest

from backend_tests.apps.api_server.testing_app_dependencies import build_test_client


class TestHealthRoutes(unittest.TestCase):
    def test_check_health(self):
        client = build_test_client()

        response = client.get("/api/health")

        self.assertEqual(200, response.status_code)
        self.assertEqual({"status": "ok"}, response.json())


if __name__ == "__main__":
    unittest.main()
