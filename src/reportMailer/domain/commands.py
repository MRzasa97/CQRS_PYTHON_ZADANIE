from dataclasses import dataclass

class Command:
    pass

@dataclass
class SendReportCommand(Command):
    data: str
    email: str