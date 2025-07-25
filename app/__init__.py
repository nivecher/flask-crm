from flask import Flask
from config import config_by_name
from .extensions import db, login, migrate
import os


def create_app(config_name: str | None = None) -> "Flask":
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    login.init_app(app)
    login.login_view = "auth.login"
    login.login_message = "Please log in to access this page."
    migrate.init_app(app, db)

    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.donations import bp as donations_bp

    app.register_blueprint(donations_bp, url_prefix="/donation")

    from app.donors import bp as donors_bp

    app.register_blueprint(donors_bp, url_prefix="/donors")

    with app.app_context():
        from . import models  # noqa: F401

    return app
