from app.extensions import db
from app.models import Donor, Donation
from sqlalchemy import func, desc
from flask_sqlalchemy.pagination import Pagination
from app.forms import DonorForm, DonationForm
from decimal import Decimal


def get_dashboard_data() -> tuple[Decimal, list[Donation], list[tuple[Donor, Decimal]]]:
    """Get data for the dashboard."""
    total_donations = db.session.scalar(db.select(func.sum(Donation.amount))) or Decimal(0)
    recent_donations_query = db.select(Donation).order_by(Donation.date.desc()).limit(5)
    recent_donations = db.session.scalars(recent_donations_query).all()

    total_donations_agg = func.sum(Donation.amount).label("total")
    top_donors_query = (
        db.select(Donor, total_donations_agg)
        .join(Donation)
        .group_by(Donor)
        .order_by(desc("total"))
        .limit(5)
    )
    top_donors = db.session.execute(top_donors_query).all()
    return total_donations, recent_donations, top_donors


def get_donors_paginated(page: int) -> Pagination:
    """Get a paginated list of donors."""
    return db.paginate(db.select(Donor).order_by(Donor.name), page=page, per_page=10, error_out=False)


def get_donor_or_404(donor_id: int) -> Donor:
    """Get a donor by ID or raise a 404 error."""
    return db.get_or_404(Donor, donor_id)


def create_donor(form: DonorForm) -> Donor:
    """Create a new donor."""
    donor = Donor(
        name=form.name.data,
        email=form.email.data,
        phone=form.phone.data,
        address=form.address.data,
    )
    db.session.add(donor)
    db.session.commit()
    return donor


def update_donor(donor: Donor, form: DonorForm) -> Donor:
    """Update an existing donor."""
    donor.name = form.name.data
    donor.email = form.email.data
    donor.phone = form.phone.data or None
    donor.address = form.address.data or None
    db.session.commit()
    return donor


def delete_donor(donor: Donor) -> None:
    """Delete a donor."""
    db.session.delete(donor)
    db.session.commit()





def get_all_donors() -> list[Donor]:
    """Get all donors."""
    return db.session.scalars(db.select(Donor).order_by(Donor.name)).all()
