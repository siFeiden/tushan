import asyncio as aio
import json
import random

from net.server import ClientConnectedEvent, ClientDisconnectedEvent
from arena.events import FirstTurnEvent, MoveAcceptedEvent, PlayerMoveEvent
from arena.logic.piece import Piece, Orientation
from arena.logic.placements import ValidPlacements
from asynctest import Mock


class Bot(object):
  def __init__(self, name):
    self.name = name

  async def __call__(self, event):
    event.event_queue.register(FirstTurnEvent, self.first_turn_event)
    event.event_queue.register(MoveAcceptedEvent, self.next_turn_event)

    # send this to let lobby know that bot wants to play
    reader = Mock(spec=aio.StreamReader)
    writer = Mock(spec=aio.StreamWriter)
    await event.event_queue.publish(ClientConnectedEvent(self.name, reader, writer))

  async def first_turn_event(self, event):
    game = event.game
    if game.current_player.id != self.name:
      return

    (x, y, o) = self.first_turn(game.board, event.piece)
    reply = PlayerMoveEvent(self.name, x, y, o)
    await event.event_queue.publish(reply)

  async def next_turn_event(self, event):
    game = event.game
    if game.current_player.id != self.name:
      return

    (x, y, o) = self.next_turn(game.board, event.next_piece)
    reply = PlayerMoveEvent(self.name, x, y, o)
    await event.event_queue.publish(reply)

  def first_turn(self, board, piece):
    raise NotImplementedError()

  def next_turn(self, board, piece):
    raise NotImplementedError()


class Simpleton(Bot):
  def __init__(self):
    super().__init__('simpleton-0.1')

  def first_turn(self, board, piece):
    size = board.size
    center = size // 2 - 1
    return (center, center, Orientation.South)

  def next_turn(self, board, piece):
    placements = ValidPlacements(board, piece)
    chosen = random.choice(list(placements))
    return (chosen.x, chosen.y, chosen.orientation)
