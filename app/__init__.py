from os import getenv
from flask import Flask


def setup_app() -> object:
    """
    Creates a new Flask application
    :rtype: Flask object
    """
    _app = Flask(__name__)
    _app.config.from_object(
        f"config.{getenv('FLASK_ENV', 'development')}"
    )
    return _app


app = setup_app()
