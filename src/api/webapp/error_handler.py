from typing import Any

import werkzeug
from connexion import FlaskApp
from connexion.exceptions import ProblemException


def handle_error(error: Any):
    if isinstance(error, ProblemException):
        if error.status == 500:
            error = werkzeug.exceptions.InternalServerError()

    return FlaskApp.common_error_handler(error)
