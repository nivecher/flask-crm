import logging
from flask import (
    render_template,
    request,
    Response,
    jsonify,
    current_app,
)
from flask.typing import ResponseReturnValue
from flask_login import login_required
from app.main import bp
from app.main.services import get_dashboard_data
import requests


@bp.route("/api/address-autocomplete")
@login_required
def address_autocomplete() -> "Response":
    try:
        query = request.args.get("query", "")
        api_key = current_app.config["GOOGLE_API_KEY"]
        logging.info(f"Google API Key: {api_key}")
        if not api_key:
            return jsonify({"error": "Address validation is not configured."}), 500
        if not query:
            return jsonify([])

        url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={query}&key={api_key}&types=address"
        response = requests.get(url)
        if response.status_code == 200:
            predictions = response.json().get("predictions", [])
            logging.info(f"Google Places API response: {predictions}")
            return jsonify(predictions)
        return jsonify([])
    except Exception:
        logging.exception("Error in address_autocomplete")
        return jsonify({"error": "An unexpected error occurred."}), 500


@bp.route("/api/place-details")
@login_required
def place_details() -> "Response":
    try:
        place_id = request.args.get("place_id", "")
        api_key = current_app.config["GOOGLE_API_KEY"]
        logging.info(f"Google API Key: {api_key}")
        if not api_key:
            return jsonify({"error": "Address validation is not configured."}), 500
        if not place_id:
            return jsonify({"error": "Missing place_id"}), 400

        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}&fields=address_components,formatted_address"
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify(response.json().get("result", {}))
        return jsonify({"error": "Failed to fetch place details"}), 500
    except Exception:
        logging.exception("Error in place_details")
        return jsonify({"error": "An unexpected error occurred."}), 500


@bp.route("/")
@bp.route("/dashboard")
@login_required
def dashboard() -> "ResponseReturnValue":
    total_donations, recent_donations, top_donors = get_dashboard_data()
    return render_template(
        "dashboard.html",
        title="Dashboard",
        total_donations=total_donations,
        recent_donations=recent_donations,
        top_donors=top_donors,
    )
