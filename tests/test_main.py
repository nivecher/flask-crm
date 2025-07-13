from app.extensions import db
from app.models import Donor, Donation
from tests.base import BaseTestCase
from tests.factories import UserFactory, DonorFactory, DonationFactory


class MainTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        user = UserFactory(password="password")
        self.client.post(
            "/auth/login",
            data={"username": user.username, "password": "password"},
            follow_redirects=True,
        )

    def test_add_donor(self):
        from unittest.mock import patch

        with patch("app.forms.validate_address", return_value=True):
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
        from unittest.mock import patch

        donor = DonorFactory()
        with patch("app.forms.validate_address", return_value=True):
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
        donor = DonorFactory()
        response = self.client.post(
            f"/donor/{donor.id}/delete",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Donors", response.data)
        deleted_donor = db.session.get(Donor, donor.id)
        self.assertIsNone(deleted_donor)

    def test_add_donation(self):
        donor = DonorFactory()
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

    def test_add_donor_with_existing_email(self):
        from unittest.mock import patch

        donor = DonorFactory()
        with patch("app.forms.validate_address", return_value=True):
            response = self.client.post(
                "/donor/new",
                data={
                    "name": "Jane Doe",
                    "email": donor.email,
                    "phone": "1234567890",
                    "address": "123 Main St",
                },
                follow_redirects=True,
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This email is already registered.", response.data)

    def test_edit_donor_get(self):
        donor = DonorFactory()
        response = self.client.get(f"/donor/{donor.id}/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes(donor.name, "utf-8"), response.data)

    def test_add_donation_invalid(self):
        donor = DonorFactory()
        response = self.client.post(
            f"/donor/{donor.id}/add_donation",
            data={"amount": "", "date": "2025-07-12", "type": "Online"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This field is required.", response.data)

    def test_export_donors_csv(self):
        # Create some donors
        donor1 = DonorFactory(name="John Doe", email="john@example.com")
        donor2 = DonorFactory(name="Jane Smith", email="jane@example.com")

        response = self.client.get("/donors/export/csv")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/csv")
        self.assertIn("attachment;filename=donors.csv", response.headers["Content-Disposition"])

        data = response.data.decode("utf-8")
        self.assertIn("ID,Name,Email,Phone,Address", data)
        self.assertIn(f"{donor1.id},{donor1.name},{donor1.email}", data)
        self.assertIn(f"{donor2.id},{donor2.name},{donor2.email}", data)

    def test_add_donor_with_invalid_address(self):
        with self.app.app_context():
            with self.app.test_request_context():
                from unittest.mock import patch

                with patch("app.utils.validate_address", return_value=False):
                    response = self.client.post(
                        "/donor/new",
                        data={
                            "name": "Test Donor",
                            "email": "test@example.com",
                            "address": "Invalid Address",
                        },
                        follow_redirects=True,
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertIn(b"The address appears to be invalid.", response.data)

    def test_add_donor_with_valid_address(self):
        with self.app.app_context():
            with self.app.test_request_context():
                from unittest.mock import patch

                with patch("app.utils.validate_address", return_value=True):
                    response = self.client.post(
                        "/donor/new",
                        data={
                            "name": "Test Donor",
                            "email": "test@example.com",
                            "address": "Valid Address",
                        },
                        follow_redirects=True,
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertIn(b"Donors", response.data)

    def test_add_donor_no_api_key(self):
        self.app.config["GOOGLE_API_KEY"] = None
        with self.app.app_context():
            with self.app.test_request_context():
                response = self.client.post(
                    "/donor/new",
                    data={
                        "name": "Test Donor",
                        "email": "test@example.com",
                        "address": "Any Address",
                    },
                    follow_redirects=True,
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn(b"Donors", response.data)

    def test_add_donor_geocoder_timeout(self):
        with self.app.app_context():
            with self.app.test_request_context():
                from unittest.mock import patch
                from geopy.exc import GeocoderTimedOut

                with patch("app.utils.GoogleV3.geocode", side_effect=GeocoderTimedOut):
                    response = self.client.post(
                        "/donor/new",
                        data={
                            "name": "Test Donor",
                            "email": "test@example.com",
                            "address": "Any Address",
                        },
                        follow_redirects=True,
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertIn(b"The address appears to be invalid.", response.data)
