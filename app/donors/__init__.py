from flask import Blueprint

bp = Blueprint("donors", __name__)

from app.donors import routes
