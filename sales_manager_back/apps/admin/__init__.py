from flask import Blueprint

admin = Blueprint("admin", __name__)

from apps.admin import views

__all__ = ["models", "control", "views"]
