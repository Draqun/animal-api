from pathlib import Path
from typing import Dict

from connexion import ProblemException, FlaskApp
from connexion.resolver import RestyResolver
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from common.common_logging.configure_logging import configure_logging
from api.webapp.error_handler import handle_error


def create_app(specification_path: Path, name: str, host: str, port: int,
               log_level: str, options: Dict = {'swagger_ui': True}) -> FlaskApp:
    app = FlaskApp(
        import_name=__name__,
        host=host,
        port=port,
        specification_dir=specification_path.parent,
        resolver = RestyResolver('api'),
        options=options
    )

    configure_logging(app=app.app, name=name, log_level=log_level)

    # Add custom error handler
    for exception in (ProblemException, HTTPException):
        app.add_error_handler(exception, handle_error)

    app.add_api(
        specification=specification_path.name,
        validate_responses=True
    )

    CORS(app.app)
    return app