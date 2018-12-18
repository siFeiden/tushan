import json

from asynctest import MagicMock

from main import BootstrapEvent
from arena.lobby import Lobby
from arena.logic.game import Board, Game, Player
from arena.logic.piece import Orientation, Piece
from arena.events import *
from eventing.event_queue import HandlerFailedEvent
from net.server import ClientConnectedEvent
from test.event_queue import TestingEventQueue


class GameSpec(object):
  def __init__(self, players, pieces, positions):
    self.players = players
    self.pieces = pieces
    self.positions = positions

    assert len(self.players) == 2

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
        x = pos['x']
        y = pos['y']
        orientation = Orientation(pos['orientation'])
        positions.append((x, y, orientation))

      return clss(players, pieces, positions)


class GamePlan(object):
  def __init__(self, gamespec):
    self.gamespec = gamespec

    random = MagicMock()
    random.sample.side_effect = lambda l, n: l[:n]
    random.shuffle.side_effect = self.set_lobby_pieces
    self.lobby = Lobby(random)

  def set_lobby_pieces(self, piece_list):
    piece_list.clear()
    piece_list.extend(self.gamespec.pieces)

  async def execute_on(self, event_queue):
    event_queue.register(BootstrapEvent, self.lobby)
    await event_queue.publish(BootstrapEvent())
    await event_queue.run_until_complete()

    for player in self.gamespec.players:
      event = ClientConnectedEvent(player, None, None)
      await event_queue.publish(event)
      await event_queue.run_until_complete()

    i = 0
    for piece, (x, y, orientation) in zip(self.gamespec.pieces, self.gamespec.positions):
      player = self.gamespec.players[i]
      event = PlayerMoveEvent(player, x, y, orientation)
      await event_queue.publish(event)
      await event_queue.run_until_complete()
      i = 1 - i
