from pathlib import Path

from common.webapp.app import create_app
from api.webapp.settings import config

SWAGGER_PATH = Path(__file__).absolute().parents[1] / 'openapi.yaml'

app = create_app(
    specification_path=SWAGGER_PATH,
    host=config.host,
    port=config.port,
    log_level=config.log_level,
    swagger_ui=config.swagger_ui
)

if __name__ == '__main__':
    app.run()
