import json

from asynctest import CoroutineMock, MagicMock, TestCase

from main import BootstrapEvent
from arena.lobby import Lobby
from arena.logic.piece import Piece
from arena.events import *
from eventing.event_queue import EventQueue, HandlerFailedEvent
from net.server import ClientConnectedEvent


class GameSpec(object):
  def __init__(self, players, pieces, positions):
    self.players = players
    self.pieces = pieces
    self.positions = positions

    assert len(self.players) == 2

  async def play_on(self, event_queue):
    for player in self.players:
      event = ClientConnectedEvent(player, None, None)
      await event_queue.publish(event)

    await event_queue.run_until_complete()

    i = 0
    for piece, (x, y, orientation) in zip(self.pieces, self.positions):
      player = self.players[i]
      event = PlayerMoveEvent(player, x, y, orientation)
      await event_queue.publish(event)
      await event_queue.run_until_complete()
      i = 1 - i

  @classmethod
  def from_file(clss, path):
    with open(path) as f:
      game = json.load(f)

      players = list(game['objectives'])
      pieces = []
      positions = []
      for p in game['stones']:
        pieces.append(Piece(p['width'], p['height'], p['connectors']))
        pos = p['position']
        positions.append((pos['x'], pos['y'], pos['orientation']))

      return clss(players, pieces, positions)


class GamePlan(object):
  def __init__(self, gamespec):
    self.gamespec = gamespec
    self.event_queue = EventQueue(debug=True)

    random = MagicMock()
    random.sample.side_effect = lambda l, n: l[:n]
    self.lobby = Lobby(random)

  async def run(self):
    self.event_queue.register(BootstrapEvent, self.lobby)
    await self.event_queue.publish(BootstrapEvent())
    await self.event_queue.run_until_complete()
    await self.gamespec.play_on(self.event_queue)


class LobbyTest(TestCase):
  def handler_failed(self, event):
    print('ERROR:', event.exception)

  async def test_spec_game(self):
    gamespec = GameSpec.from_file('../protocol/examples/populated-field.json')
    gameplan = GamePlan(gamespec)
    gameplan.event_queue.register(HandlerFailedEvent, lambda e: print(e.exception))
    await gameplan.run()

    import arena.serializers as s
    print(s.GameSerializer.serialize(gameplan.lobby.game))
