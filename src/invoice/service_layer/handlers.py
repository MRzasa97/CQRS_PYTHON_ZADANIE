from invoice.domain import commands, events
from invoice.domain.model import Invoice, Report
from typing import List, Dict, Callable, Type, TYPE_CHECKING
import logging
from invoice.service_layer import unit_of_work
from . import messagebus
from invoice.views import get_invoice_by_email
from invoice import bootstrap

logger = logging.getLogger(__name__)

def create_invoice(
        cmd: commands.CreateInvoice, uow: unit_of_work.AbstractUnitOfWork
):
        with uow:
                print('Creating invoice')
                invoice = Invoice(cmd.email, cmd.amount)
                uow.invoices.add(
                        invoice
                )
                uow.commit()

def update_invoice(
        cmd: commands.UpdateInvoice, uow: unit_of_work.AbstractUnitOfWork
):
        with uow:
                invoice = uow.invoices.get(id=cmd.id)
                invoice.amount = cmd.amount
                uow.commit()

def delete_invoice(
        cmd: commands.DeleteInvoice, uow: unit_of_work.AbstractUnitOfWork
):
        with uow:
                invoice = uow.invoices.get(id=cmd.id)
                uow.invoices.delete(invoice)
                uow.commit()
        
def publish_invoice_created(event: events.InvoiceCreated, publish: Callable):
        publish('report_generated', event)

def generate_report(
        cmd: commands.GenerateInvoiceReport, uow: unit_of_work.AbstractUnitOfWork, publish: Callable
):
        with uow:
                invoices = get_invoice_by_email(cmd.email, uow)
                report = Report(invoices, cmd.email)
                result = report.generate_report()
                uow.add_event(report)

def new_events(*args):
        for arg in args:
                if isinstance(arg, events.Event):
                        yield arg

EVENT_HANDLERS = {
        events.InvoiceCreated: [publish_invoice_created],
        events.ReportGenerated: [publish_invoice_created],
} # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
        commands.CreateInvoice: create_invoice,
        commands.UpdateInvoice: update_invoice,
        commands.DeleteInvoice: delete_invoice,
        commands.GenerateInvoiceReport: generate_report,
} # type: Dict[Type[commands.Command], Callable]