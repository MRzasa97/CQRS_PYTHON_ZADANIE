from __future__ import annotations
from dataclasses import asdict
from typing import List, Dict, Callable, Type, TYPE_CHECKING
from reportMailer.domain import commands
from . import messagebus
if TYPE_CHECKING:
    from reportMailer.adapters import notifications

class InvalidSku(Exception):
    pass

def send_invoice_report(
        cmd: commands.SendReportCommand,
        notifications: notifications.AbstractNotifications,
):
    print('Sending report')
    notifications.send(
        destination=cmd.email,
        message=cmd.data,
    )

COMMAND_HANDLERS = {
    commands.SendReportCommand: send_invoice_report,
} # type: Dict[Type[commands.Command], Callable]