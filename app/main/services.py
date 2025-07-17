from app.extensions import db
from app.models import Donor, Donation
from sqlalchemy import func, desc
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



