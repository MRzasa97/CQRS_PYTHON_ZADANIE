from typing import Dict, Type, Callable
from invoice.service_layer import messagebus, handlers
from invoice.domain import commands
from invoice.adapters import orm, redis_eventpublisher
from invoice.service_layer import unit_of_work
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from invoice import config
from invoice.adapters import repository
from tenacity import retry, stop_after_delay
import inspect
import logging

def bootstrap(
        start_orm: bool = True,
        uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
        publish: Callable = redis_eventpublisher.publish,

) -> messagebus.MessageBus:
    if start_orm:
        orm.start_mappers()
    engine = create_engine(config.get_postgres_uri())
    wait_for_postgres_to_come_up(engine)
    orm.metadata.create_all(engine)



    dependencies = {'uow': uow, 'publish': publish}

    injected_event_handlers = {
        event: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    
    injected_command_handlers = {
        command: inject_dependencies(handler, dependencies)
        for command, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(
        uow=uow,
        command_handlers=injected_command_handlers,
        event_handlers=injected_event_handlers,
    )

def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)

@retry(stop=stop_after_delay(30))
def wait_for_postgres_to_come_up(engine):
    return engine.connect()