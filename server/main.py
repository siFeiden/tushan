import argparse
import asyncio as aio

from net.server import *
from eventing.event_queue import EventQueue, HandlerFailedEvent
from arena.lobby import Lobby
from arena.message_translator import MessageTranslator
from arena import events as evt


class Tushan(object):
  def create_argparser(self):
    parser = argparse.ArgumentParser(description='Tushan game server')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('host')
    parser.add_argument('port', type=int)

    return parser

  async def bootstrap(self, options):
    event_queue = EventQueue()
    server = Server(event_queue, options.host, options.port)

    lobby = Lobby()
    message_translator = MessageTranslator()

    event_queue.register(MessageReceivedEvent, message_translator.onMessageReceived)
    event_queue.register(HandlerFailedEvent, lambda e: print('ERROR:', e.exception))

    event_queue.register(ClientConnectedEvent, lobby.client_connected)
    event_queue.register(ClientDisconnectedEvent, lobby.client_disconnected)
    event_queue.register(evt.LaunchGameEvent, lobby.launch_game)
    event_queue.register(evt.GameStartedEvent, lobby.game_started)
    event_queue.register(evt.PlayerNameEvent, lobby.player_name)
    event_queue.register(evt.PlayerMoveEvent, lobby.player_move)
    event_queue.register(evt.PlayerCannotMoveEvent, lobby.player_cannot_move)
    event_queue.register(evt.GameIsOverEvent, lobby.game_is_over)
    event_queue.register(evt.DisqualifyPlayerEvent, lobby.disqualify_player)

    await server.start()
    await event_queue.run()

  def run(self):
    argparser = self.create_argparser()
    options = argparser.parse_args()

    aio.run(self.bootstrap(options), debug=options.debug)

if __name__ == '__main__':
  Tushan().run()
