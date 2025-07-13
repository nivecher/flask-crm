from flask import current_app
from tests.base import BaseTestCase


class BasicsTestCase(BaseTestCase):
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])

    def test_404_error(self):
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"File Not Found", response.data)

