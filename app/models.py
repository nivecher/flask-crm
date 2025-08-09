from __future__ import annotations
from sqlalchemy import Integer, String, Numeric, DateTime, ForeignKey
import sqlalchemy as sa

from datetime import datetime, timezone
from decimal import Decimal

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db, login


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: db.Mapped[int] = db.mapped_column(Integer, primary_key=True)
    username: db.Mapped[str] = db.mapped_column(String(64), index=True, unique=True)
    email: db.Mapped[str] = db.mapped_column(String(120), index=True, unique=True)
    password_hash: db.Mapped[str] = db.mapped_column(String(128))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return self.password_hash is not None and check_password_hash(
            self.password_hash, password
        )

    def __repr__(self) -> str:
        return f"<User {self.username or self.email}>"


@login.user_loader
def load_user(id: int) -> User | None:
    return db.session.get(User, id)


class Donor(db.Model):
    __tablename__ = "donors"
    id: db.Mapped[int] = db.mapped_column(Integer, primary_key=True)
    name: db.Mapped[str] = db.mapped_column(String(128), nullable=False)
    email: db.Mapped[str] = db.mapped_column(String(120), index=True, unique=True)
    phone: db.Mapped[str | None] = db.mapped_column(String(20), nullable=True)
    donations: db.Mapped[list["Donation"]] = db.relationship(
        back_populates="donor", cascade="all, delete-orphan", passive_deletes=True
    )
    addresses: db.Mapped[list["DonorAddress"]] = db.relationship(
        back_populates="donor", cascade="all, delete-orphan"
    )

    @property
    def current_address(self) -> Address | None:
        current = [da.address for da in self.addresses if da.is_current]
        return current[0] if current else None

    def __repr__(self) -> str:
        return f"<Donor {self.name}>"


class Address(db.Model):
    __tablename__ = "addresses"
    id: db.Mapped[int] = db.mapped_column(Integer, primary_key=True)
    address_line1: db.Mapped[str] = db.mapped_column(sa.String(128), nullable=False)
    address_line2: db.Mapped[str | None] = db.mapped_column(sa.String(128))
    city: db.Mapped[str] = db.mapped_column(sa.String(64), nullable=False)
    state: db.Mapped[str] = db.mapped_column(sa.String(64), nullable=False)
    postal_code: db.Mapped[str] = db.mapped_column(sa.String(20), nullable=False)
    country: db.Mapped[str] = db.mapped_column(sa.String(64), nullable=False)
    donors: db.Mapped[list["DonorAddress"]] = db.relationship(
        back_populates="address", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Address {self.address_line1}>"


class DonorAddress(db.Model):
    __tablename__ = "donor_addresses"
    donor_id: db.Mapped[int] = db.mapped_column(
        Integer, ForeignKey("donors.id"), primary_key=True
    )
    address_id: db.Mapped[int] = db.mapped_column(
        Integer, ForeignKey("addresses.id"), primary_key=True
    )
    is_current: db.Mapped[bool] = db.mapped_column(default=True, nullable=False)
    donor: db.Mapped["Donor"] = db.relationship(back_populates="addresses")
    address: db.Mapped["Address"] = db.relationship(back_populates="donors")

    def __repr__(self) -> str:
        return f"<DonorAddress donor_id={self.donor_id} address_id={self.address_id}>"


class Donation(db.Model):
    __tablename__ = "donations"
    id: db.Mapped[int] = db.mapped_column(Integer, primary_key=True)
    amount: db.Mapped[Decimal] = db.mapped_column(Numeric(10, 2), nullable=False)
    date: db.Mapped[datetime] = db.mapped_column(
        DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )
    type: db.Mapped[str | None] = db.mapped_column(
        String(50), nullable=True
    )  # e.g., 'Online', 'Check', 'In-Kind'
    donor_id: db.Mapped[int] = db.mapped_column(Integer, ForeignKey("donors.id"))
    donor: db.Mapped["Donor"] = db.relationship(back_populates="donations")

    def __repr__(self) -> str:
        return f"<Donation ${self.amount:.2f}>" if self.amount else "<Donation None>"
