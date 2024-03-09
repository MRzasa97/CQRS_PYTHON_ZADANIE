from invoice.service_layer import unit_of_work
from sqlalchemy import text

def get_invoice_by_email(
        email: str, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        results = uow.session.execute(
            text('SELECT email, amount FROM invoices WHERE email=:email'), 
            {'email': email}
            ).fetchall()
    return [tuple(result) for result in results]

def get_invoice_less_then_amount(
        amount: int, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        results = uow.session.execute(
            text('SELECT email, amount FROM invoices WHERE amount<:amount'), 
            {'amount': amount}
            ).fetchall()
    return [tuple(result) for result in results]

def get_invoice_greater_then_amount(
        amount: int, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        results = uow.session.execute(
            text('SELECT email, amount FROM invoices WHERE amount>:amount'), 
            {'amount': amount}
            ).fetchall()
    return [tuple(result) for result in results]

def get_all_invoices(
        uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        results = uow.session.execute(
            text('SELECT email, amount FROM invoices')
            ).fetchall()
    return [tuple(result) for result in results]