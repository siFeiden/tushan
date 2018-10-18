import argparse
import asyncio as aio

from net.server import Server, SpawnReadersListener
from eventing.event_queue import EventQueue


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

    event_queue.register_class(SpawnReadersListener())

    await server.start()
    await event_queue.run()

  def run(self):
    argparser = self.create_argparser()
    options = argparser.parse_args()

    aio.run(self.bootstrap(options), debug=options.debug)

if __name__ == '__main__':
  Tushan().run()
