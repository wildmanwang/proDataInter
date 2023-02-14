from flask import Blueprint

goods = Blueprint("goods", __name__, url_prefix="/goods")

from . import models, control, views
__all__ = ["models", "control", "views"]
