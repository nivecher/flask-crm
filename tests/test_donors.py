from app.extensions import db
from app.models import Donor
from tests.base import BaseTestCase
from tests.factories import UserFactory, DonorFactory


class DonorTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        user = UserFactory(password="password")
        self.client.post(
            "/auth/login",
            data={"username": user.username, "password": "password"},
            follow_redirects=True,
        )

    def test_add_donor(self) -> None:
        from unittest.mock import patch

        with patch("phonenumbers.parse"), patch(
            "phonenumbers.is_valid_number", return_value=True
        ):
            response = self.client.post(
                "/donors/new",
                data={
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "phone": "1234567890",
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

    def test_edit_donor(self) -> None:
        from unittest.mock import patch

        donor = DonorFactory()
        with patch("phonenumbers.parse"), patch(
            "phonenumbers.is_valid_number", return_value=True
        ):
            response = self.client.post(
                f"/donors/{donor.id}/edit",
                data={
                    "name": "Jane Smith",
                    "email": donor.email,
                    "phone": "0987654321",
                },
                follow_redirects=True,
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Jane Smith", response.data)
        updated_donor = db.session.get(Donor, donor.id)
        self.assertEqual(updated_donor.name, "Jane Smith")
        self.assertEqual(updated_donor.email, donor.email)

    def test_delete_donor(self) -> None:
        donor = DonorFactory()
        response = self.client.post(
            f"/donors/{donor.id}/delete",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Donors", response.data)
        deleted_donor = db.session.get(Donor, donor.id)
        self.assertIsNone(deleted_donor)

    def test_add_donor_with_existing_email(self) -> None:
        donor = DonorFactory()
        response = self.client.post(
            "/donors/new",
            data={
                "name": "Jane Doe",
                "email": donor.email,
                "phone": "1234567890",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This email is already registered.", response.data)

    def test_edit_donor_get(self) -> None:
        donor = DonorFactory()
        response = self.client.get(f"/donors/{donor.id}/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes(donor.name, "utf-8"), response.data)

    def test_export_donors_csv(self) -> None:
        # Create some donors
        donor1 = DonorFactory(name="John Doe", email="john@example.com")
        donor2 = DonorFactory(name="Jane Smith", email="jane@example.com")

        response = self.client.get("/donors/export/csv")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/csv")
        self.assertIn(
            "attachment;filename=donors.csv",
            response.headers["Content-Disposition"],
        )

        data = response.data.decode("utf-8")
        expected_header = "ID,Name,Email,Phone,Address Line 1,Address Line 2,City,State,Postal Code,Country"  # noqa: E501
        self.assertIn(expected_header, data)
        self.assertIn(f"{donor1.id},{donor1.name},{donor1.email}", data)
        self.assertIn(f"{donor2.id},{donor2.name},{donor2.email}", data)

    def test_add_donor_with_invalid_phone(self) -> None:
        response = self.client.post(
            "/donors/new",
            data={
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "123",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid phone number.", response.data)

    def test_add_donor_with_invalid_email(self) -> None:
        response = self.client.post(
            "/donors/new",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "phone": "1234567890",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid email address.", response.data)
