from tests.base import BaseTestCase
from app.models import User, Donor, Donation
from decimal import Decimal
from datetime import datetime


class ModelsTestCase(BaseTestCase):
    def test_user_repr(self):
        user = User(username="testuser", email="test@example.com")
        self.assertEqual(repr(user), "<User testuser>")

    def test_donor_repr(self):
        donor = Donor(name="Test Donor", email="test.donor@example.com")
        self.assertEqual(repr(donor), "<Donor Test Donor>")

    def test_donation_repr(self):
        donation = Donation(amount=Decimal("100.00"), date=datetime.utcnow())
        self.assertEqual(repr(donation), "<Donation $100.00>")
