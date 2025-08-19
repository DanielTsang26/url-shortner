from flask_limiter import Limiter 
from flask_limiter.util import get_remote_address

def create_limiter(app, limit= ["10 per day"]):
    """creates and configures a rate limiter for the Flask app."""

    return  Limiter(
    get_remote_address,
    app = app,
    default_limits = limit
)