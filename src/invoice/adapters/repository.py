import abc
from typing import Set
from invoice.adapters import orm
from invoice.domain import model

class AbstractRepository(abc.ABC):

    def __init__(self):
        self.seen = set() # type: Set[model.Invoice]

    def add(self, invoice: model.Invoice):
        self._add(invoice)
        self.seen.add(invoice)

    def get(self, id) -> model.Invoice:
        invoice = self._get(id)
        if invoice:
            self.seen.add(invoice)
        return invoice
    
    def get_by_amount(self, amount) -> model.Invoice:
        invoice = self._get_by_amount(amount)
        if invoice:
            self.seen.add(invoice)
        return invoice
    
    def delete(self, invoice: model.Invoice):
        self._delete(invoice)
        self.seen.remove(invoice)
    
    def get_by_email(self, email) -> model.Invoice:
        invoices = self._get_by_email(email)
        for invoice in invoices:
            self.seen.add(invoice)
        return invoices
    
    @abc.abstractmethod
    def _add(self, invoice: model.Invoice):
        raise NotImplementedError
    
    @abc.abstractmethod
    def _get(self, email) -> model.Invoice:
        raise NotImplementedError
    
    @abc.abstractmethod
    def _get_by_amount(self, amount) -> model.Invoice:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_email(self, email) -> model.Invoice:
        raise NotImplementedError
    

class SqlAlchemyRepository(AbstractRepository):
    
        def __init__(self, session):
            super().__init__()
            self.session = session
    
        def _add(self, invoice):
            self.session.add(invoice)
    
        def _get(self, id):
            return self.session.query(model.Invoice).filter_by(id=id).first()
        
        def _get_by_amount(self, amount):
            return self.session.query(model.Invoice).filter_by(amount=amount).first()
        
        def _delete(self, invoice):
            self.session.delete(invoice)

        def _get_by_email(self, email):
            return self.session.query(model.Invoice).filter_by(email=email).all()