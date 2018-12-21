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
  def __init__(self, players, objectives, pieces, positions, size):
    self.players = players
    self.objectives = objectives
    self.pieces = pieces
    self.positions = positions
    self.size = size

    assert len(players) == 2
    assert len(pieces) == len(positions)
    assert size > 0 and size % 2 == 0

  @classmethod
  def from_file(clss, path):
    with open(path) as f:
      game = json.load(f)

      size = game['dimension']
      players = list(game['objectives'])
      all_objectives = {}
      pieces = []
      positions = []

      for name, objectives in game['objectives'].items():
        all_objectives[name] = [Board.Side(side) for side in objectives]

      for p in game['stones']:
        pieces.append(Piece(p['width'], p['height'], p['connectors']))
        pos = p['position']
        x, y = pos['x'], pos['y']
        orientation = Orientation(pos['orientation'])
        positions.append((x, y, orientation))

      return clss(players, all_objectives, pieces, positions, size)


class GamePlan(object):
  def __init__(self, gamespec):
    self.gamespec = gamespec
    self.lobby = Lobby(self) # pass self as GameBuilder interface

  def build_game(self, players):
    """Build game according to the gamespec passed in constructor

    With this method we implement the GameBuilder interface, see
    also OfficialGameBuilder
    """

    board = Board(self.gamespec.size)
    chosen_players = [players[id] for id in self.gamespec.players]
    objectives = {player: self.gamespec.objectives[player.id] for player in chosen_players}

    return Game(board, chosen_players, objectives, self.gamespec.pieces)

  async def execute_on(self, event_queue):
    """Execute the game specified via gamespec on the given EventQueue

    This means events for client connections and turn are published
    on the event queue.
    """
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
