from flask import current_app
from tests.base import BaseTestCase


class BasicsTestCase(BaseTestCase):
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])
