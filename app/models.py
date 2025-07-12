from __future__ import annotations
from datetime import datetime, UTC
from typing import TYPE_CHECKING
from .extensions import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, Numeric, DateTime

if TYPE_CHECKING:
    from decimal import Decimal


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


@login.user_loader
def load_user(id: str) -> User | None:
    return db.session.get(User, int(id))


class Donor(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    address: Mapped[str | None] = mapped_column(String(200), nullable=True)
    donations: Mapped[list[Donation]] = relationship("Donation", backref="donor", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Donor {self.name}>"


class Donation(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, index=True, default=lambda: datetime.now(UTC))
    type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # e.g., 'Online', 'Check', 'In-Kind'
    donor_id: Mapped[int] = mapped_column(Integer, ForeignKey("donor.id"))

    def __repr__(self) -> str:
        return f"<Donation ${self.amount}>"
