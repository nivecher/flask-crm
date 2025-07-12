from app.extensions import db
from app.models import Donor, Donation
from sqlalchemy import func


def get_dashboard_data():
    """Get data for the dashboard."""
    total_donations = db.session.query(func.sum(Donation.amount)).scalar() or 0
    recent_donations = Donation.query.order_by(Donation.date.desc()).limit(5).all()
    top_donors = (
        db.session.query(Donor, func.sum(Donation.amount).label("total"))
        .join(Donation)
        .group_by(Donor)
        .order_by(func.sum(Donation.amount).desc())
        .limit(5)
        .all()
    )
    return total_donations, recent_donations, top_donors


def get_donors_paginated(page):
    """Get a paginated list of donors."""
    return Donor.query.order_by(Donor.name).paginate(page=page, per_page=10, error_out=False)


def get_donor_or_404(donor_id):
    """Get a donor by ID or raise a 404 error."""
    return db.get_or_404(Donor, donor_id)


def create_donor(form):
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


def update_donor(donor, form):
    """Update an existing donor."""
    donor.name = form.name.data
    donor.email = form.email.data
    donor.phone = form.phone.data
    donor.address = form.address.data
    db.session.commit()
    return donor


def delete_donor(donor):
    """Delete a donor."""
    db.session.delete(donor)
    db.session.commit()


def create_donation(donor, form):
    """Create a new donation."""
    donation = Donation(
        amount=form.amount.data,
        date=form.date.data,
        type=form.type.data,
        donor=donor,
    )
    db.session.add(donation)
    db.session.commit()
    return donation
