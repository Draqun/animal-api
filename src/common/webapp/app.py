from pathlib import Path
from typing import Dict

from connexion import ProblemException, FlaskApp
from connexion.resolver import RestyResolver
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from api.webapp.error_handler import handle_error


def create_app(specification_path: Path, host: str, port: int, log_level: str, swagger_ui: bool = False) -> FlaskApp:
    options: Dict = {'swagger_ui': swagger_ui}
    app = FlaskApp(
        import_name=__name__,
        host=host,
        port=port,
        specification_dir=specification_path.parent,
        resolver=RestyResolver('api'),
        debug=log_level == 'DEBUG',
        options=options
    )

    # Add custom error handler
    for exception in (ProblemException, HTTPException):
        app.add_error_handler(exception, handle_error)

    app.add_api(
        specification=specification_path.name,
        validate_responses=True
    )

    CORS(app.app)
    return app
