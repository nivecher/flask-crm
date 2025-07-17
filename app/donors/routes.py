from flask import render_template, redirect, url_for, flash, request, Response
from flask.typing import ResponseReturnValue
from flask_login import login_required
from app.donors import bp
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
from app.forms import DonationForm


@bp.route("/")
@login_required
def donors() -> ResponseReturnValue:
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
    cw.writerow(["ID", "Name", "Email", "Phone", "Address Line 1", "Address Line 2", "City", "State", "Postal Code", "Country"])
    for donor in donors:
        cw.writerow([donor.id, donor.name, donor.email, donor.phone, donor.address_line1, donor.address_line2, donor.city, donor.state, donor.postal_code, donor.country])
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
    return render_template(
        "donations/detail.html", title=donor.name, donor=donor, form=form
    )


@bp.route("/new", methods=["GET", "POST"])
@login_required
def add_donor() -> ResponseReturnValue:
    form = DonorForm()
    if form.validate_on_submit():
        create_donor(form)
        flash("Donor added successfully.")
        return redirect(url_for("donors.donors"))
    return render_template("donors/form.html", title="Add Donor", form=form)


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_donor(id: int) -> ResponseReturnValue:
    donor = get_donor_or_404(id)
    form = DonorForm(obj=donor)
    form.instance = donor  # Pass instance to form
    if form.validate_on_submit():
        update_donor(donor, form)
        flash("Donor updated successfully.")
        return redirect(url_for("donors.donor_detail", id=donor.id))
    return render_template("donors/form.html", title="Edit Donor", form=form)


@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_donor_route(id: int) -> ResponseReturnValue:
    donor = get_donor_or_404(id)
    delete_donor(donor)
    flash("Donor deleted successfully.")
    return redirect(url_for("donors.donors"))
