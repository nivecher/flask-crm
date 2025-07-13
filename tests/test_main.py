from app.extensions import db
from app.models import Donor, Donation
from app.auth.services import create_user
from tests.base import BaseTestCase


class MainTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a user and log in
        create_user("testuser", "test@example.com", "password")
        self.client.post(
            "/auth/login",
            data={"username": "testuser", "password": "password"},
            follow_redirects=True,
        )

    def test_add_donor(self):
        response = self.client.post(
            "/donor/new",
            data={
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890",
                "address": "123 Main St",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Donors", response.data)
        donor = db.session.execute(
            db.select(Donor).filter_by(email="john.doe@example.com")
        ).scalar_one_or_none()
        self.assertIsNotNone(donor)
        self.assertEqual(donor.name, "John Doe")

    def test_edit_donor(self):
        # First, add a donor
        donor = Donor(name="Jane Doe", email="jane.doe@example.com")
        db.session.add(donor)
        db.session.commit()

        response = self.client.post(
            f"/donor/{donor.id}/edit",
            data={
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone": "0987654321",
                "address": "456 Oak Ave",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Jane Smith", response.data)
        updated_donor = db.session.get(Donor, donor.id)
        self.assertEqual(updated_donor.name, "Jane Smith")
        self.assertEqual(updated_donor.email, "jane.smith@example.com")

    def test_delete_donor(self):
        # First, add a donor
        donor = Donor(name="Mark Doe", email="mark.doe@example.com")
        db.session.add(donor)
        db.session.commit()

        response = self.client.post(
            f"/donor/{donor.id}/delete",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Donors", response.data)
        deleted_donor = db.session.get(Donor, donor.id)
        self.assertIsNone(deleted_donor)

    def test_add_donation(self):
        # First, add a donor
        donor = Donor(name="Sam Doe", email="sam.doe@example.com")
        db.session.add(donor)
        db.session.commit()

        response = self.client.post(
            f"/donor/{donor.id}/add_donation",
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
