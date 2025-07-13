from app.extensions import db
from app.models import Donation
from tests.base import BaseTestCase
from tests.factories import UserFactory, DonorFactory, DonationFactory


class DonationsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        user = UserFactory(password="password")
        self.client.post(
            "/auth/login",
            data={"username": user.username, "password": "password"},
            follow_redirects=True,
        )

    def test_add_donation(self):
        donor = DonorFactory()
        response = self.client.post(
            f"/donation/donor/{donor.id}/add_donation",
            data={"amount": "100.00", "date": "2025-07-12", "type": "Online"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"100.00", response.data)
        donation = db.session.execute(
            db.select(Donation).filter_by(donor_id=donor.id)
        ).scalar_one_or_none()
        self.assertIsNotNone(donation)
        self.assertEqual(donation.amount, 100.00)

    def test_add_donation_invalid(self):
        donor = DonorFactory()
        response = self.client.post(
            f"/donation/donor/{donor.id}/add_donation",
            data={"amount": "", "date": "2025-07-12", "type": "Online"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This field is required.", response.data)

    def test_edit_donation(self):
        donation = DonationFactory()
        response = self.client.post(
            f"/donation/{donation.id}/edit",
            data={"amount": "150.00", "date": "2025-07-13", "type": "Check"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"150.00", response.data)
        updated_donation = db.session.get(Donation, donation.id)
        self.assertEqual(updated_donation.amount, 150.00)

    def test_delete_donation(self):
        donation = DonationFactory()
        response = self.client.post(
            f"/donation/{donation.id}/delete",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        deleted_donation = db.session.get(Donation, donation.id)
        self.assertIsNone(deleted_donation)

    def test_edit_nonexistent_donation(self):
        response = self.client.get("/donation/999/edit", follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_donation(self):
        response = self.client.post("/donation/999/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_edit_donation_get(self):
        donation = DonationFactory()
        response = self.client.get(f"/donation/{donation.id}/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit Donation", response.data)
