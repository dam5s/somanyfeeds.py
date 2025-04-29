import unittest

from starlette.testclient import TestClient

from backend.apps.api_server.app import build_api


class TestHelloRoutes(unittest.TestCase):
    def test_say_hello(self) -> None:
        app = build_api()
        client = TestClient(app)

        response = client.get("/api/hello")

        self.assertEqual(200, response.status_code)
        self.assertEqual({'message': 'Hello, World!'}, response.json())


if __name__ == '__main__':
    unittest.main()
