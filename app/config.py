import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallbacksecret")
    DEBUG = os.environ.get("FLASK_ENV") == "development"
