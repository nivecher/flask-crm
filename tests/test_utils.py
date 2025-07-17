from tests.base import BaseTestCase
from app.utils import validate_address, validate_phone, validate_user_email
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


class UtilsTestCase(BaseTestCase):
    def test_validate_address_no_api_key(self):
        self.app.config["GOOGLE_API_KEY"] = None
        self.assertTrue(validate_address("123 Main St"))

    def test_validate_address_geocoder_timeout(self):
        from unittest.mock import patch

        with patch("app.utils.GoogleV3.geocode", side_effect=GeocoderTimedOut):
            self.assertFalse(validate_address("123 Main St"))

    def test_validate_address_geocoder_service_error(self):
        from unittest.mock import patch

        with patch("app.utils.GoogleV3.geocode", side_effect=GeocoderServiceError):
            self.assertFalse(validate_address("123 Main St"))

    def test_validate_address_valid(self):
        from unittest.mock import patch

        with patch("app.utils.GoogleV3.geocode", return_value=True):
            self.assertTrue(validate_address("123 Main St"))

    def test_validate_address_invalid(self):
        from unittest.mock import patch

        with patch("app.utils.GoogleV3.geocode", return_value=None):
            self.assertFalse(validate_address("123 Main St"))

    def test_validate_user_email_user_not_found(self):
        from unittest.mock import MagicMock

        field = MagicMock()
        field.data = "test@example.com"
        validate_user_email(None, field)

    def test_validate_user_email_user_not_found(self):
        from unittest.mock import MagicMock

        field = MagicMock()
        field.data = "test@example.com"
        validate_user_email(None, field)

    def test_validate_user_email_user_not_found(self):
        from unittest.mock import MagicMock

        field = MagicMock()
        field.data = "test@example.com"
        validate_user_email(None, field)

    
