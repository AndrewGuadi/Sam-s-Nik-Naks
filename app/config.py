import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallbacksecret")
    DEBUG = os.environ.get("FLASK_ENV") == "development"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_DIR = os.environ.get("FLASK_INSTANCE_PATH") or os.path.join(os.path.dirname(BASE_DIR), "instance")
    DATABASE_PATH = os.environ.get("DATABASE_PATH") or os.path.join(INSTANCE_DIR, "sams_nik_naks.db")
