from dataclasses import dataclass
import os
from typing import Optional


@dataclass(frozen=True)
class AppConfig:
    host: Optional[str]
    port: Optional[int]
    log_level: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str
    swagger_ui: bool

    @classmethod
    def read_config(cls):
        port = os.environ.get('PORT', None)
        if port:
            port = int(port)

        display_ui: str = os.environ.get('SWAGGER', 'false')

        return cls(
            host=os.environ.get('HOST', None),
            port=port,
            log_level=os.environ.get('LOG_LEVEL', 'INFO'),
            db_host=os.environ['DB_HOST'],
            db_port=int(os.environ['DB_PORT']),
            db_name=os.environ['DB_NAME'],
            db_user=os.environ['DB_USER'],
            db_pass=os.environ['DB_PASS'],
            swagger_ui=True if display_ui.lower() == 'true' else False
        )

    @property
    def endpoint_url(self):
        return f'http://{self.db_host}:{self.db_port}'

    @property
    def connection_string(self):
        return f'mysql+pymysql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'


config = AppConfig.read_config()
