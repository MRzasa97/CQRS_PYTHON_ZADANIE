import inspect
from typing import Callable
from reportMailer.service_layer import messagebus, handlers, unit_of_work
from reportMailer.adapters.notifications import (
    AbstractNotifications, EmailNotifications
)
def bootstrap(
        notifications: AbstractNotifications = None,
) -> messagebus.MessageBus:
    if notifications is None:
        notifications = EmailNotifications()

    dependencies = {'notifications': notifications}
    injected_command_handlers = {
        command: inject_dependencies(handler, dependencies)
        for command, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(
        command_handlers=injected_command_handlers,
    )

def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)