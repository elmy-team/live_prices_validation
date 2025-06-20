from flask import Blueprint

api = Blueprint('api', __name__)

from . import validate_prices, get_live_prices  # noqa: E402, F401
