from app.extensions import db
from app.models import Donation
from datetime import datetime
from decimal import Decimal


def get_donation_or_404(donation_id: int) -> Donation:
    return db.get_or_404(Donation, donation_id)


def update_donation(
    donation: Donation, amount: Decimal, date: datetime, type: str | None
) -> None:
    donation.amount = amount
    donation.date = date
    donation.type = type
    db.session.commit()


def delete_donation(donation: Donation) -> None:
    db.session.delete(donation)
    db.session.commit()
