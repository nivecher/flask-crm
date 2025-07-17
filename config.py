import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    VERSION = "1.0.2"


class ProdConfig(Config):
    """Production configuration."""

    ENV = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")


class DevConfig(Config):
    """Development configuration."""

    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret-key"

config_by_name = dict(
    development=DevConfig,
    testing=TestingConfig,
    production=ProdConfig,
)