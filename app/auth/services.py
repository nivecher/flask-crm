from app.extensions import db
from app.models import User


def create_user(username, email, password):
    """Create a new user."""
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def authenticate_user(username, password):
    """Authenticate a user."""
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return None
    return user
