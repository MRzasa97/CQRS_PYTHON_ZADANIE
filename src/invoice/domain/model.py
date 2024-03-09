from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set
from invoice.domain import events
from . import commands
import csv
from io import StringIO

class Invoice:

    def __init__(self, email: str, amount: float):
        self.email = email
        self.amount = amount
        self._events = [] # type: List[events.Event]


class Report:
    
    def __init__(self, data: str, email: str):
        self.data = data
        self.email = email
        self._events = [] # type: List[events.Event]

    def generate_report(self):
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(['email', 'amount'])
        csv_writer.writerows(self.data)
        csv_string = csv_buffer.getvalue()
        self._events.append(events.ReportGenerated(data=csv_string, email=self.email))
        csv_buffer.close()
        return self._events
        