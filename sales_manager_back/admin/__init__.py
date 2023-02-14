from flask import Blueprint

admin = Blueprint("admin", __name__, url_prefix="")

from . import models, control, views
__all__ = ["models", "control", "views"]
