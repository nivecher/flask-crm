from datetime import datetime, UTC
from .extensions import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    donations = db.relationship("Donation", backref="donor", lazy="dynamic")

    def __repr__(self):
        return f"<Donor {self.name}>"


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.DateTime, index=True, default=lambda: datetime.now(UTC))
    type = db.Column(db.String(50))  # e.g., 'Online', 'Check', 'In-Kind'
    donor_id = db.Column(db.Integer, db.ForeignKey("donor.id"))

    def __repr__(self):
        return f"<Donation ${self.amount}>"
