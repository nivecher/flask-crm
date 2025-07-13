from flask import Blueprint

bp = Blueprint("donations", __name__)

from app.donations import routes  # noqa: F401, E402
