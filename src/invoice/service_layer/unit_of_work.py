from __future__ import annotations
import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from invoice import config
from invoice.adapters import repository

class AbstractUnitOfWork(abc.ABC):
    invoices: repository.AbstractRepository
    self_events = []

    def __enter__(self) -> AbstractUnitOfWork:
        return self
    
    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def add_event(self, event):
        self.self_events.append(event)

    def collect_new_events(self):
        for object in self.self_events:
            while object._events:
                yield object._events.pop(0)


    def rollback(self):
        self._rollback()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def _rollback(self):
        raise NotImplementedError
    
DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(
    config.get_postgres_uri(), isolation_level="REPEATABLE READ",
))

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory() # type: Session
        self.invoices = repository.SqlAlchemyRepository(self.session)
        return super().__enter__()
    
    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def _rollback(self):
        self.session.rollback()