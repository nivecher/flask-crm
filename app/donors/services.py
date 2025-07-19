from app.extensions import db
from app.models import Donor
from flask_sqlalchemy.pagination import Pagination
from app.donors.forms import DonorForm


def get_donors_paginated(page: int) -> Pagination:
    """Get a paginated list of donors."""
    return db.paginate(
        db.select(Donor).order_by(Donor.name), page=page, per_page=10, error_out=False
    )


def get_donor_or_404(donor_id: int) -> Donor:
    """Get a donor by ID or raise a 404 error."""
    return db.get_or_404(Donor, donor_id)


def create_donor(form: "DonorForm") -> "Donor":
    """Create a new donor."""
    donor = Donor(
        name=form.name.data,
        email=form.email.data,
        phone=form.phone.data,
        address_line1=form.address_line1.data,
        address_line2=form.address_line2.data,
        city=form.city.data,
        state=form.state.data,
        postal_code=form.postal_code.data,
        country=form.country.data,
    )
    db.session.add(donor)
    db.session.commit()
    return donor


def update_donor(donor: Donor, form: DonorForm) -> Donor:
    """Update an existing donor."""
    donor.name = form.name.data
    donor.email = form.email.data
    donor.phone = form.phone.data or None
    donor.address_line1 = form.address_line1.data or None
    donor.address_line2 = form.address_line2.data or None
    donor.city = form.city.data or None
    donor.state = form.state.data or None
    donor.postal_code = form.postal_code.data or None
    donor.country = form.country.data or None
    db.session.commit()
    return donor


def delete_donor(donor: Donor) -> None:
    """Delete a donor."""
    db.session.delete(donor)
    db.session.commit()


def get_all_donors() -> list[Donor]:
    """Get all donors."""
    return db.session.scalars(db.select(Donor).order_by(Donor.name)).all()
