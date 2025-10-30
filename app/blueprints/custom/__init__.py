from flask import Blueprint


custom = Blueprint("custom", __name__, template_folder="templates")

from . import routes  # noqa: E402,F401
