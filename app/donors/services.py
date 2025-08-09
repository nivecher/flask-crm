from app.extensions import db
from app.models import Donor, Address, DonorAddress
from flask_sqlalchemy.pagination import Pagination
from app.donors.forms import DonorForm, AddressForm


def get_donors_paginated(page: int) -> Pagination:
    """Get a paginated list of donors."""
    return db.paginate(
        db.select(Donor).order_by(Donor.name), page=page, per_page=10, error_out=False
    )


def get_donor_or_404(donor_id: int) -> Donor:
    """Get a donor by ID or raise a 404 error."""
    return db.get_or_404(Donor, donor_id)


def create_donor(form: "DonorForm", current_address_data: dict) -> "Donor":
    """Create a new donor."""
    donor = Donor(
        name=form.name.data,
        email=form.email.data,
        phone=form.phone.data,
    )
    db.session.add(donor)
    db.session.flush()  # Ensure donor has an ID before creating DonorAddress

    if current_address_data and current_address_data.get("address_line1"):
        address = Address(**current_address_data)
        db.session.add(address)
        db.session.flush()

        donor_address = DonorAddress(
            donor_id=donor.id, address_id=address.id, is_current=True
        )
        db.session.add(donor_address)

    db.session.commit()
    return donor


def _manage_donor_address(
    donor: Donor, address_data: dict[str, str], is_current: bool
) -> None:
    """Helper function to manage donor addresses."""
    if not any(address_data.values()) or not address_data.get("address_line1"):
        return

    # Normalize address data by stripping whitespace
    normalized_address_data = {
        k: v.strip() for k, v in address_data.items() if isinstance(v, str)
    }

    # Check if an identical address already exists
    address = db.session.execute(
        db.select(Address).filter_by(**normalized_address_data)
    ).scalar_one_or_none()

    if not address:
        address = Address(**normalized_address_data)
        db.session.add(address)
        db.session.flush()

    # If setting a new current address, deactivate the old one
    if is_current:
        for da in donor.addresses:
            if da.is_current:
                da.is_current = False

    # Check if the relationship already exists
    donor_address = db.session.execute(
        db.select(DonorAddress).filter_by(donor_id=donor.id, address_id=address.id)
    ).scalar_one_or_none()

    if donor_address:
        donor_address.is_current = is_current
    else:
        donor_address = DonorAddress(
            donor_id=donor.id, address_id=address.id, is_current=is_current
        )
        db.session.add(donor_address)


def update_donor(donor: Donor, form: DonorForm, current_address_data: dict) -> Donor:
    """Update an existing donor."""
    donor.name = form.name.data
    email_changed = donor.email != form.email.data
    donor.email = form.email.data
    donor.phone = form.phone.data or None

    # Manage current address
    _manage_donor_address(donor, current_address_data, is_current=True)

    db.session.commit()
    return donor


def delete_donor(donor: Donor) -> None:
    """Delete a donor."""
    db.session.delete(donor)
    db.session.commit()


def get_all_donors() -> list[Donor]:
    """Get all donors."""
    return db.session.scalars(db.select(Donor).order_by(Donor.name)).all()
