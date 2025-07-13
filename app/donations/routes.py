from flask import render_template, redirect, url_for, flash, request
from flask.typing import ResponseReturnValue
from flask_login import login_required
from app.donations import bp
from app.forms import DonationForm
from app.donations.services import (
    get_donation_or_404,
    update_donation,
    delete_donation,
    create_donation,
)
from app.main.services import get_donor_or_404


@bp.route("/donor/<int:id>/add_donation", methods=["POST"])
@login_required
def add_donation(id: int) -> ResponseReturnValue:
    donor = get_donor_or_404(id)
    form = DonationForm()
    if form.validate_on_submit():
        create_donation(donor, form)
        flash("Donation added successfully.")
        return redirect(url_for("main.donor_detail", id=id))
    return render_template("donations/detail.html", title=donor.name, donor=donor, form=form)


@bp.route("/<int:donation_id>/edit", methods=["GET", "POST"])
@login_required
def edit_donation_route(donation_id):
    donation = get_donation_or_404(donation_id)
    form = DonationForm(obj=donation)
    if form.validate_on_submit():
        update_donation(donation, form.amount.data, form.date.data, form.type.data)
        flash("Donation updated successfully.", "success")
        return redirect(url_for("main.donor_detail", id=donation.donor_id))
    return render_template(
        "donations/edit.html", title="Edit Donation", form=form, donation=donation
    )


@bp.route("/<int:donation_id>/delete", methods=["POST"])
@login_required
def delete_donation_route(donation_id):
    donation = get_donation_or_404(donation_id)
    donor_id = donation.donor_id
    delete_donation(donation)
    flash("Donation deleted successfully.", "success")
    return redirect(url_for("main.donor_detail", id=donor_id))
