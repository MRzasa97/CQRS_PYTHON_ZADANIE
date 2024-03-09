from dataclasses import dataclass

class Command:
    pass

@dataclass
class CreateInvoice(Command):
    email: str
    amount: float

@dataclass
class UpdateInvoice(Command):
    id: int
    amount: float

@dataclass
class DeleteInvoice(Command):
    id: int

@dataclass
class GenerateInvoiceReport(Command):
    email: str