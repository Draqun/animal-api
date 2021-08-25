from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from api.webapp.settings import AppConfig
from common.ports.repository.unit_of_work import UnitOfWork


class SQLUnitOfWork(UnitOfWork):
    _session: Session

    def __init__(self, config: AppConfig):
        self._config = config
        self._session_cls = sessionmaker(bind=create_engine(self._config.connection_string, echo=True))

    def __enter__(self):
        self._session = self._session_cls()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.rollback()

    def commit(self) -> None:
        self._session.commit()

    def add(self, item: Any, flush=False) -> Any:
        self._session.add(item)
        if flush:
            self._session.flush()
        return item

    def query(self, *args, **kwargs) -> Any:
        return self._session.query(*args, **kwargs)
