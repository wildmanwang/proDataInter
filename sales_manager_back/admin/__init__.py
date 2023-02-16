from flask import Blueprint

admin = Blueprint("admin", __name__)

from admin import views
__all__ = ["models", "control", "views"]
