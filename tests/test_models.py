from tests.base import BaseTestCase
from tests.factories import UserFactory, DonorFactory, DonationFactory


class ModelsTestCase(BaseTestCase):
    def test_user_repr(self):
        user = UserFactory.build(username="testuser")
        self.assertEqual(repr(user), "<User testuser>")

    def test_donor_repr(self):
        donor = DonorFactory.build(name="Test Donor")
        self.assertEqual(repr(donor), "<Donor Test Donor>")

    def test_donation_repr(self):
        donation = DonationFactory.build(amount=100.00)
        self.assertEqual(repr(donation), "<Donation $100.00>")
