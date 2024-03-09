from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set
from . import commands

class InvoiceReport:
    def __init__(self, email: str, amount: float):
        self.email = email
        self.amount = amount