from flask import Blueprint


media = Blueprint("media", __name__, template_folder="templates")

from . import routes  # noqa: E402,F401
