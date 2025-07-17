from tests.base import BaseTestCase
from tests.factories import UserFactory


class DashboardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        user = UserFactory(password="password")
        self.client.post(
            "/auth/login",
            data={"username": user.username, "password": "password"},
            follow_redirects=True,
        )

    def test_dashboard(self):
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)

    def test_address_autocomplete(self):
        from unittest.mock import patch

        mock_response = {
            "predictions": [
                {"description": "123 Main St, Anytown, USA"},
                {"description": "123 Main St, Othertown, USA"},
            ]
        }
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            response = self.client.get("/api/address-autocomplete?query=123 Main")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, mock_response["predictions"])