import pytest
from invoice.domain import commands
from invoice.service_layer import handlers
from invoice import bootstrap
from invoice.adapters import repository
from invoice.service_layer import unit_of_work

# Write test for enpoints in flask_app.py

class FakeRepository(repository.AbstractRepository):
    def __init__(self, invoices):
        super().__init__()
        self._invoices = set(invoices)

    def _add(self, invoice):
        self._invoices.add(invoice)

    def _get_by_email(self, email):
        return [i for i in self._invoices if i.email == email]
    
    def _get_by_amount(self, amount):
        return [i for i in self._invoices if i.amount == amount]
    
    def _get(self, id):
        return next(i for i in self._invoices if i.id == id)

    def _update(self, id, amount):
        for i in self._invoices:
            if i.id == id:
                i.amount = amount
                return i

    def _all(self):
        return self.invoices
    
class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.invoices = FakeRepository([])
        self.commited = False

    def _commit(self):
        self.commited = True

    def _rollback(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

def bootstrap_test_app():
    return bootstrap.bootstrap(
        start_orm=False,
        uow=FakeUnitOfWork(),
        publish=lambda *args: None
    )

def test_create_invoice():
    bus = bootstrap_test_app()
    bus.handle(commands.CreateInvoice("test1@test.pl", 100))
    assert bus.uow.invoices.get_by_email("test1@test.pl") is not None
    assert bus.uow.commited
    

