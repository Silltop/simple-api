import json
import logging
from typing import Type
from werkzeug.exceptions import default_exceptions, HTTPException
from api import app


def override_flask_exceptions() -> None:
    """Loop over flask exceptions and override default error handler."""
    for exc in default_exceptions:
        app.register_error_handler(exc, _handle_flask_exception)


def _handle_flask_exception(exception_object) -> str:
    """Custom error handler for flask exceptions for JSON format."""
    response = exception_object.get_response()
    http_error_code = exception_object.code
    if 400 <= http_error_code < 500:
        error_description = "This is a client error, make sure you provided correct data."
    elif 500 <= http_error_code < 600:
        error_description = "This is a server error, please provide this error to support team."
    else:
        error_description = "Unknown error"
    response_data = {
        "status": exception_object.code,
        "description": error_description,
        "error": exception_object.description,
    }
    response.data = json.dumps(response_data)  # Convert data to JSON string
    response.content_type = "application/json"  # Set content type
    logging.error(f"API returned error: {http_error_code}, with description: {exception_object.description}")
    return response
