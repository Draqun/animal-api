from pathlib import Path

from connexion import ProblemException, FlaskApp
from connexion.resolver import RestyResolver
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from api.webapp.settings import config
from api.webapp.error_handler import handle_error
from common.common_logging.configure_logging import configure_logging

SWAGGER_PATH = Path(__file__).absolute().parents[1] / 'openapi.yaml'

if __name__ == '__main__':
    app = FlaskApp(
        import_name=__name__,
        host=config.host,
        port=config.port,
        specification_dir=SWAGGER_PATH.parent,
        resolver = RestyResolver('api'),
        options={'swagger_ui': True}
    )

    configure_logging(app=app.app, name='api', log_level=config.log_level)

    # Add custom error handler
    for exception in (ProblemException, HTTPException):
        app.add_error_handler(exception, handle_error)

    app.add_api(
        specification=SWAGGER_PATH.name,
        validate_responses=True
    )

    CORS(app.app)
    app.run()