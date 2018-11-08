import argparse
import asyncio as aio

from net.server import *
from eventing.event_queue import EventQueue, HandlerFailedEvent


class Tushan(object):
  def __init__(self):
    pass

  def create_argparser(self):
    parser = argparse.ArgumentParser(description='Tushan game server')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('host')
    parser.add_argument('port', type=int)

    return parser

  async def bootstrap(self, options):
    event_queue = EventQueue()
    server = Server(event_queue, options.host, options.port)

    event_queue.register(ClientConnectedEvent, lambda e: print('client connected'))
    event_queue.register(ClientDisconnectedEvent, lambda e: print('client disconnected'))
    event_queue.register(MessageReceivedEvent, lambda e: print(e.json, end=''))
    event_queue.register(HandlerFailedEvent, lambda e: print('ERROR:', e.exception))

    await server.start()
    await event_queue.run()

  def run(self):
    argparser = self.create_argparser()
    options = argparser.parse_args()

    aio.run(self.bootstrap(options), debug=options.debug)

if __name__ == '__main__':
  Tushan().run()
