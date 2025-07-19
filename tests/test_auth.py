from app.extensions import db
from app.models import User
from tests.base import BaseTestCase
from tests.factories import UserFactory
from app.auth.services import create_user


class AuthTestCase(BaseTestCase):
    def test_registration(self) -> None:
        response = self.client.post(
            "/auth/register",
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password",
                "password2": "password",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        user = db.session.execute(
            db.select(User).filter_by(username="testuser")
        ).scalar_one_or_none()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")

    def test_login_logout(self) -> None:
        user = UserFactory(password="password")
        response = self.client.post(
            "/auth/login",
            data={"username": user.username, "password": "password"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)

        response = self.client.get("/auth/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sign In", response.data)

    def test_login_with_invalid_password(self) -> None:
        user = UserFactory(password="password")
        response = self.client.post(
            "/auth/login",
            data={"username": user.username, "password": "wrongpassword"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid username or password", response.data)
        self.assertIn(b"Sign In", response.data)

    def test_registration_with_existing_username(self) -> None:
        user = UserFactory()
        response = self.client.post(
            "/auth/register",
            data={
                "username": user.username,
                "email": "another@example.com",
                "password": "password",
                "password2": "password",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please use a different username.", response.data)

    def test_registration_with_existing_email(self) -> None:
        user = UserFactory()
        response = self.client.post(
            "/auth/register",
            data={
                "username": "anotheruser",
                "email": user.email,
                "password": "password",
                "password2": "password",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please use a different email address.", response.data)

    def test_login_page_when_logged_in(self) -> None:
        user = UserFactory(password="password")
        self.client.post(
            "/auth/login", data={"username": user.username, "password": "password"}
        )
        response = self.client.get("/auth/login", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)
        self.assertNotIn(b"Sign In", response.data)

    def test_register_page_when_logged_in(self) -> None:
        user = UserFactory(password="password")
        self.client.post(
            "/auth/login", data={"username": user.username, "password": "password"}
        )
        response = self.client.get("/auth/register", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)
        self.assertNotIn(b"Register", response.data)

    def test_user_loader(self) -> None:
        user = UserFactory(password="password")
        self.client.post(
            "/auth/login", data={"username": user.username, "password": "password"}
        )
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)

    def test_user_loader_after_logout(self) -> None:
        user = UserFactory(password="password")
        self.client.post(
            "/auth/login", data={"username": user.username, "password": "password"}
        )
        self.client.get("/auth/logout")
        self.client.post(
            "/auth/login", data={"username": user.username, "password": "password"}
        )
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)

    def test_user_loader_with_new_client(self) -> None:
        create_user("testuser", "test@example.com", "password")
        self.client.post(
            "/auth/login", data={"username": "testuser", "password": "password"}
        )
        client2 = self.app.test_client()
        response = client2.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)
