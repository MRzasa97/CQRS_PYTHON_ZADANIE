from invoice.domain import commands, events
from typing import Union, Type, Dict, Callable, List
from invoice.service_layer import unit_of_work
import logging

logger = logging.getLogger(__name__)

Message = Union[commands.Command]

class MessageBus:

    def __init__(
            self,
            uow: unit_of_work.AbstractUnitOfWork,
            command_handlers: Dict[Type[commands.Command], Callable],
            event_handlers: Dict[Type[events.Event], List[Callable]],
    ):
        self.uow = uow
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers

    def handle(self, message: Message):
        self.queue = [message]
        logger.info(f'Handling message {message} with {self.command_handlers}')
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, commands.Command):
                self.handle_command(message)
            elif isinstance(message, events.Event):
                self.handle_event(message)
            else:
                raise Exception(f'{message} was not a command')
            
    def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug(f'handling event {event} with handler {handler}')
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception as e:
                logger.exception(e)
                raise
    
    def handle_command(self, command: commands.Command):
        handler = self.command_handlers[type(command)]
        try:
            handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception as e:
            logger.exception(e)
            raise