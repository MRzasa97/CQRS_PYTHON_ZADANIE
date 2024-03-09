from __future__ import annotations
import logging
from typing import Callable, Dict, List, Union, Type, TYPE_CHECKING
from reportMailer.domain import commands

logger = logging.getLogger(__name__)

Message = Union[commands.Command]

class MessageBus:
    def __init__(
        self,
        command_handlers: Dict[Type[commands.Command], Callable],
    ):
        self.command_handlers = command_handlers

    def handle(self, message: Message):
        self.queue = [message]
        logger.info(f'Handling message {message} with {self.command_handlers}')
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, commands.Command):
                self.handle_command(message)
            else:
                raise Exception(f'{message} was not a command')
            
    def handle_command(self, command: commands.Command):
        handler = self.command_handlers[type(command)]
        try:
            handler(command)
        except Exception as e:
            logger.exception(e)
            raise