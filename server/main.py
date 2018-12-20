import argparse
import asyncio as aio
import random

from arena.bots import Simpleton
from arena.lobby import Lobby, OfficialGameBuilder
from arena.message_translator import MessageTranslator
from arena import events as evt
from eventing.event_queue import Event, EventQueue, HandlerFailedEvent
from net.server import *


class BootstrapEvent(Event):
  """Sent as the very first event in an EventQueue"""


class Tushan(object):
  def create_argparser(self):
    parser = argparse.ArgumentParser(description='Tushan game server')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-b', '--bot', action='store_true')
    parser.add_argument('host')
    parser.add_argument('port', type=int)

    return parser

  def handler_failed(self, event):
    print('ERROR:', event.exception)

  async def bootstrap(self, options):
    event_queue = EventQueue(options.debug)
    server = Server(event_queue, options.host, options.port)

    game_builder = OfficialGameBuilder()
    lobby = Lobby(game_builder)
    message_translator = MessageTranslator()

    if options.bot:
      bot = Simpleton()
      event_queue.register(BootstrapEvent, bot)

    event_queue.register(HandlerFailedEvent, self.handler_failed)
    event_queue.register(BootstrapEvent, lobby)
    event_queue.register(BootstrapEvent, message_translator)

    # Send BootstrapEvent to allow other components to register listeners themselves
    event = BootstrapEvent()
    await event_queue.publish(event)

    await server.start()
    await event_queue.run()

  def run(self):
    argparser = self.create_argparser()
    options = argparser.parse_args()

    aio.run(self.bootstrap(options), debug=options.debug)

if __name__ == '__main__':
  Tushan().run()
