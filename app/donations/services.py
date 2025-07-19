from app.extensions import db
from app.models import Donation, Donor
from datetime import datetime
from decimal import Decimal
from app.donations.forms import DonationForm


def create_donation(donor: "Donor", form: "DonationForm") -> "Donation":
    """Create a new donation."""
    donation = Donation()
    donation.amount = form.amount.data
    donation.date = form.date.data
    donation.type = form.type.data
    donation.donor = donor
    db.session.add(donation)
    db.session.commit()
    return donation


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
