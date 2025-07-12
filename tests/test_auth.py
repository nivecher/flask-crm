import unittest
from app import create_app, db
from app.models import User
from app.auth.services import create_user


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration(self):
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
        user = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")

    def test_login_logout(self):
        create_user("testuser", "test@example.com", "password")
        response = self.client.post(
            "/auth/login",
            data={"username": "testuser", "password": "password"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)

        response = self.client.get("/auth/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sign In", response.data)
