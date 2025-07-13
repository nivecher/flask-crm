from app.extensions import db
from app.models import Donor, Donation
from app.auth.services import create_user
from tests.base import BaseTestCase
from datetime import datetime


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

    def test_edit_donation(self):
        # First, add a donor and a donation
        donor = Donor(name="Test Donor", email="test.donor@example.com")
        db.session.add(donor)
        db.session.commit()
        donation = Donation(amount=100.00, date=datetime.utcnow(), type="Online", donor_id=donor.id)
        db.session.add(donation)
        db.session.commit()

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
        # First, add a donor and a donation
        donor = Donor(name="Test Donor", email="test.donor@example.com")
        db.session.add(donor)
        db.session.commit()
        donation = Donation(amount=100.00, date=datetime.utcnow(), type="Online", donor_id=donor.id)
        db.session.add(donation)
        db.session.commit()

        response = self.client.post(
            f"/donation/{donation.id}/delete",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        deleted_donation = db.session.get(Donation, donation.id)
        self.assertIsNone(deleted_donation)

    def test_edit_nonexistent_donation(self):
        response = self.client.get("/donation/999/edit", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Donation not found.", response.data)

    def test_delete_nonexistent_donation(self):
        response = self.client.post("/donation/999/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Donation not found.", response.data)

    def test_edit_donation_get(self):
        # First, add a donor and a donation
        donor = Donor(name="Test Donor", email="test.donor@example.com")
        db.session.add(donor)
        db.session.commit()
        donation = Donation(amount=100.00, date=datetime.utcnow(), type="Online", donor_id=donor.id)
        db.session.add(donation)
        db.session.commit()

        response = self.client.get(f"/donation/{donation.id}/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit Donation", response.data)

    def test_add_donor_with_existing_email(self):
        # First, add a donor
        donor = Donor(name="John Doe", email="john.doe@example.com")
        db.session.add(donor)
        db.session.commit()

        response = self.client.post(
            "/donor/new",
            data={
                "name": "Jane Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890",
                "address": "123 Main St",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This email is already registered.", response.data)

    def test_edit_donor_get(self):
        # First, add a donor
        donor = Donor(name="Jane Doe", email="jane.doe@example.com")
        db.session.add(donor)
        db.session.commit()

        response = self.client.get(f"/donor/{donor.id}/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Jane Doe", response.data)

    def test_add_donation_invalid(self):
        # First, add a donor
        donor = Donor(name="Sam Doe", email="sam.doe@example.com")
        db.session.add(donor)
        db.session.commit()

        response = self.client.post(
            f"/donor/{donor.id}/add_donation",
            data={"amount": "", "date": "2025-07-12", "type": "Online"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This field is required.", response.data)
