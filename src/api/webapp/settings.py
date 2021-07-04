from dataclasses import dataclass
import os

@dataclass(frozen=True)
class AppConfig:
    host: str
    port: int
    log_level: str

    @classmethod
    def read_config(cls):
        return cls(
            host=os.environ['HOST'],
            port=os.environ['PORT'],
            log_level=os.environ['LOG_LEVEL']
        )

config = AppConfig.read_config()