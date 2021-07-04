from dataclasses import dataclass
import os

@dataclass(frozen=True)
class AppConfig:
    host: str
    port: int
    log_level: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str

    @classmethod
    def read_config(cls):
        return cls(
            host=os.environ['HOST'],
            port=os.environ['PORT'],
            log_level=os.environ['LOG_LEVEL'],
            db_host=os.environ['DB_HOST'],
            db_port=os.environ['DB_PORT'],
            db_name=os.environ['DB_NAME'],
            db_user=os.environ['DB_USER'],
            db_pass=os.environ['DB_PASS']
        )

    @property
    def endpoint_url(self):
        return f'http://{self.db_host}:{self.db_port}'

    @property
    def connection_string(self):
        return f'mysql+pymysql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'


config = AppConfig.read_config()
