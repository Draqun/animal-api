from abc import ABC, abstractmethod
from typing import Any

RepoClass = Any


class UnitOfWork(ABC):
    """ Unit of work pattern class """

    @abstractmethod
    def __enter__(self):
        """ Setting up context manager """

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Setting down context manager """

    @abstractmethod
    def commit(self) -> None:
        """ Commit operations """

    @abstractmethod
    def add(self, item: Any, flush: bool) -> Any:
        """ Add object to session """

    @abstractmethod
    def query(self, *args, **kwargs) -> Any:
        """ Query method """
