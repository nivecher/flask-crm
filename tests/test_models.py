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

    def test_set_password(self):
        user = UserFactory.build()
        user.set_password("password")
        self.assertTrue(user.check_password("password"))
        self.assertFalse(user.check_password("notpassword"))

    def test_user_repr_no_username(self):
        user = UserFactory.build(username=None)
        self.assertEqual(repr(user), f"<User {user.email}>")

    def test_user_repr_no_username(self):
        user = UserFactory.build(username=None)
        self.assertEqual(repr(user), f"<User {user.email}>")

    def test_user_repr_no_username(self):
        user = UserFactory.build(username=None)
        self.assertEqual(repr(user), f"<User {user.email}>")

    def test_donation_repr_no_amount(self):
        donation = DonationFactory.build(amount=None)
        self.assertEqual(repr(donation), f"<Donation None>")
