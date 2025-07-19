from flask import Blueprint

bp = Blueprint("donors", __name__)

from . import routes  # noqa: F401, E402
