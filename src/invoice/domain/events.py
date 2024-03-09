from dataclasses import dataclass

class Event:
    pass

@dataclass
class InvoiceCreated(Event):
    email: str
    amount: float

@dataclass
class ReportGenerated(Event):
    data: str
    email: str