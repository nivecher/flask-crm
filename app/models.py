from __future__ import annotations
import sqlalchemy as sa
from sqlalchemy import Integer, String, Numeric, DateTime, ForeignKey
import sqlalchemy.orm as so
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from decimal import Decimal

Base = db.Model

if TYPE_CHECKING:
    from app.models import Donation



class User(UserMixin, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username or self.email}>"


@login.user_loader
def load_user(id: str) -> User | None:
    return db.session.get(User, int(id))


class Donor(Base):
    __tablename__ = "donors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    address_line1: so.Mapped[str | None] = so.mapped_column(sa.String(128))
    address_line2: so.Mapped[str | None] = so.mapped_column(sa.String(128))
    city: so.Mapped[str | None] = so.mapped_column(sa.String(64))
    state: so.Mapped[str | None] = so.mapped_column(sa.String(64))
    postal_code: so.Mapped[str | None] = so.mapped_column(sa.String(20))
    country: so.Mapped[str | None] = so.mapped_column(sa.String(64))
    donations: so.Mapped[list["Donation"]] = so.relationship(
        back_populates="donor", cascade="all, delete-orphan", passive_deletes=True
    )

    def __repr__(self) -> str:
        return f"<Donor {self.name}>"


class Donation(Base):
    __tablename__ = "donations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, index=True, default=lambda: datetime.now(UTC))
    type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # e.g., 'Online', 'Check', 'In-Kind'
    donor_id: Mapped[int] = mapped_column(Integer, ForeignKey("donors.id"))
    donor: Mapped["Donor"] = so.relationship(back_populates="donations")

    def __repr__(self) -> str:
        return f"<Donation ${self.amount:.2f}>" if self.amount else "<Donation None>"
