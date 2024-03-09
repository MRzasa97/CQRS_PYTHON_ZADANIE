import abc
from typing import Set
from reportMailer import model

class AbstractRepository(abc.ABC):

    def __init__(self):
        self.seen = set() # type: Set[model.InvoiceReport]

class SqlAlchemyRepository(AbstractRepository):
    
        def __init__(self, session):
            super().__init__()
            self.session = session
