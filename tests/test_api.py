from tests.base import BaseTestCase
from tests.factories import UserFactory


class APITestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        user = UserFactory(password="password")
        self.client.post(
            "/auth/login",
            data={"username": user.username, "password": "password"},
            follow_redirects=True,
        )

    def test_address_autocomplete(self) -> None:
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

    def test_address_autocomplete_no_api_key(self) -> None:
        self.app.config["GOOGLE_API_KEY"] = None
        response = self.client.get("/api/address-autocomplete?query=123 Main")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json, {"error": "Address validation is not configured."}
        )

    def test_address_autocomplete_no_query(self) -> None:
        response = self.client.get("/api/address-autocomplete")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_place_details(self) -> None:
        from unittest.mock import patch

        mock_response = {
            "result": {
                "formatted_address": "123 Main St, Anytown, USA",
                "address_components": [],
            }
        }
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            response = self.client.get("/api/place-details?place_id=123")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, mock_response["result"])

    def test_place_details_no_api_key(self) -> None:
        self.app.config["GOOGLE_API_KEY"] = None
        response = self.client.get("/api/place-details?place_id=123")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json, {"error": "Address validation is not configured."}
        )

    def test_place_details_no_place_id(self) -> None:
        response = self.client.get("/api/place-details")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Missing place_id"})

    def test_place_details_api_fails(self) -> None:
        from unittest.mock import patch

        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 500
            response = self.client.get("/api/place-details?place_id=123")
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json, {"error": "Failed to fetch place details"})

    def test_address_autocomplete_api_fails(self) -> None:
        from unittest.mock import patch

        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 500
            response = self.client.get("/api/address-autocomplete?query=123 Main")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [])
