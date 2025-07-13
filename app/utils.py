from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from flask import current_app


def validate_address(address: str) -> bool:
    """Validate an address using the Google Geocoding API."""
    api_key = current_app.config["GOOGLE_API_KEY"]
    if not api_key:
        # If no API key is configured, we'll assume the address is valid
        return True
    geolocator = GoogleV3(api_key=api_key)
    try:
        location = geolocator.geocode(address)
        return location is not None
    except (GeocoderTimedOut, GeocoderServiceError):
        return False
