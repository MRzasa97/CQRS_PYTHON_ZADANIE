import json
import logging
import redis

from reportMailer import bootstrap, config
from reportMailer.domain import commands

logger = logging.getLogger(__name__)

r = redis.Redis(**config.get_redis_host_and_port())

def main():
    bus = bootstrap.bootstrap()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe('report_generated')

    for message in pubsub.listen():
        print(f'Got message {message}')
        handle(message, bus)

def handle(message, bus):
    data = json.loads(message['data'])
    cmd = commands.SendReportCommand(data['data'], data['email'])
    bus.handle(cmd)

if __name__ == '__main__':
    main()