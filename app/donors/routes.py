from flask import render_template, redirect, url_for, flash, request, Response
from flask.typing import ResponseReturnValue
from flask_login import login_required
from . import bp
from app.donors.forms import DonorForm
from app.donors.services import (
    get_donors_paginated,
    get_donor_or_404,
    create_donor,
    update_donor,
    delete_donor,
    get_all_donors,
)
import csv
import io
from datetime import datetime, UTC
from app.donations.forms import DonationForm


@bp.route(
    "/<int:donor_id>/address/<int:address_id>/set-current", methods=["POST", "GET"]
)
@login_required
def set_current_address(donor_id: int, address_id: int):
    donor = get_donor_or_404(donor_id)
    address = None
    for da in donor.addresses:
        if da.address.id == address_id:
            address = da.address
            da.is_current = True
        else:
            da.is_current = False
    if address:
        from app.extensions import db

        db.session.commit()
        flash("Current address updated.")
    else:
        flash("Address not found.", "danger")
    return redirect(url_for("donors.donor_detail", id=donor_id))


from flask import render_template, redirect, url_for, flash, request, Response
from flask.typing import ResponseReturnValue
from flask_login import login_required
from . import bp
from app.donors.forms import DonorForm
from app.donors.services import (
    get_donors_paginated,
    get_donor_or_404,
    create_donor,
    update_donor,
    delete_donor,
    get_all_donors,
)
import csv
import io
from datetime import datetime, UTC
from app.donations.forms import DonationForm


@bp.route("/")
@login_required
def donors() -> "ResponseReturnValue":
    page = request.args.get("page", 1, type=int)
    donors_pagination = get_donors_paginated(page)
    next_url = (
        url_for("donors.donors", page=donors_pagination.next_num)
        if donors_pagination.has_next
        else None
    )
    prev_url = (
        url_for("donors.donors", page=donors_pagination.prev_num)
        if donors_pagination.has_prev
        else None
    )
    return render_template(
        "donors/list.html",
        title="Donors",
        donors=donors_pagination.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@bp.route("/export/csv")
@login_required
def export_donors_csv() -> Response:
    """Export donors to a CSV file."""
    donors = get_all_donors()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(
        [
            "ID",
            "Name",
            "Email",
            "Phone",
            "Address Line 1",
            "Address Line 2",
            "City",
            "State",
            "Postal Code",
            "Country",
        ]
    )
    for donor in donors:
        current_address = donor.current_address
        cw.writerow(
            [
                donor.id,
                donor.name,
                donor.email,
                donor.phone,
                current_address.address_line1 if current_address else "",
                current_address.address_line2 if current_address else "",
                current_address.city if current_address else "",
                current_address.state if current_address else "",
                current_address.postal_code if current_address else "",
                current_address.country if current_address else "",
            ]
        )
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=donors.csv"},
    )


@bp.route("/<int:id>")
@login_required
def donor_detail(id: int) -> ResponseReturnValue:
    donor = get_donor_or_404(id)
    form = DonationForm()
    if request.method == "GET":
        form.date.data = datetime.now(UTC)
    former_addresses = [da.address for da in donor.addresses if not da.is_current]
    return render_template(
        "donations/detail.html",
        title=donor.name,
        donor=donor,
        form=form,
        former_addresses=former_addresses,
    )


@bp.route("/new", methods=["GET", "POST"])
@login_required
def add_donor() -> ResponseReturnValue:
    form = DonorForm()
    if form.validate_on_submit():
        current_address_data = form.current_address.data
        create_donor(form, current_address_data)
        flash("Donor added successfully.")
        return redirect(url_for("donors.donors"))
    return render_template("donors/form.html", title="Add Donor", form=form)


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_donor(id: int) -> ResponseReturnValue:
    donor = get_donor_or_404(id)
    form = DonorForm(obj=donor)
    address = donor.current_address
    if address:
        for field in form.current_address.form:
            if hasattr(address, field.name):
                field.data = getattr(address, field.name)
    if form.validate_on_submit():
        current_address_data = form.current_address.data
        update_donor(donor, form, current_address_data)
        flash("Donor updated successfully.")
        return redirect(url_for("donors.donor_detail", id=donor.id))
    else:
        import logging

        logging.warning(f"Donor form not valid: {form.errors}")
        flash(
            "Form submission failed. Please check for errors and try again.", "danger"
        )
    return render_template(
        "donors/form.html", title="Edit Donor", form=form, donor=donor
    )


@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_donor_route(id: int) -> ResponseReturnValue:
    donor = get_donor_or_404(id)
    delete_donor(donor)
    flash("Donor deleted successfully.")
    return redirect(url_for("donors.donors"))
