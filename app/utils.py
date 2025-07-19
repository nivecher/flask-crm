from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from flask import current_app
import phonenumbers
from wtforms.validators import ValidationError
from app.models import User, Donor
from app.extensions import db


from typing import Any


def validate_phone(form: Any, field: Any) -> None:
    """Validate a phone number."""
    if field.data:
        try:
            p = phonenumbers.parse(field.data)
            if not phonenumbers.is_valid_number(p):
                raise ValidationError("Invalid phone number.")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError("Invalid phone number.")


def validate_user_email(form: Any, field: Any) -> None:
    """Validate an email address."""
    # For updates, allow the user to keep their own email
    if (
        hasattr(form, "instance")
        and form.instance
        and form.instance.email == field.data
    ):
        return

    user = db.session.scalar(db.select(User).filter_by(email=field.data))
    if user is not None:
        raise ValidationError("This email is already registered.")


def validate_donor_email(form: Any, field: Any) -> None:
    """Validate a donor's email address."""
    # For updates, allow the donor to keep their own email
    if hasattr(form, "obj") and form.obj and form.obj.email == field.data:
        return

    donor = db.session.scalar(db.select(Donor).filter_by(email=field.data))
    if donor is not None:
        raise ValidationError("This email is already registered.")


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
