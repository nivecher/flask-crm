from flask import render_template
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error: Exception) -> tuple[str, int]:
    return render_template("errors/404.html"), 404
