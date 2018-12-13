from enum import Enum
from .events import *
from .logic import game, piece


class Disqualification(Enum):
  InvalidMove = 'invalid_move'
  QuitGame = 'quit_game'


class PlayerProxy(object):
  def __init__(self, id):
    self.id = id
    self.name = None
    self.objectives = None
    self.in_game = False

  def rename(self, event):
    self.name = event.name

  def join(self, game):
    self.in_game = True

  def leave(self, game):
    self.in_game = False
    self.objectives = None

  def playing(self):
    return self.in_game


class Lobby(object):
  def __init__(self):
    self.players = {}
    self.game = None

  async def client_connected(self, event):
    assert event.id not in self.players

    self.players[event.id] = Player(event.id)
    reply = LaunchGameEvent()
    await event.event_queue.publish(reply)

  async def launch_game(self, event):
    if not self.can_start_game():
      return

    game = self.build_game()
    reply = GameStartedEvent(game)
    await event.event_queue.publish(reply)

  def can_start_game(self):
    # Start new game if enough players and there
    # is no game running
    return not self.game and len(self.players) >= 2

  def build_game(self):
    board = game.Board(18)
    player1, player2 = self.choose_participants()
    pieces = piece.Piece.official_pieces()
    new_game = game.Game(board, [player1, player2], pieces)

    return new_game

  def choose_participants(self):
    id1, id2 = random.sample(self.players, 2)
    objectiveNS = [game.Board.Side.North, game.Board.Side.South]
    objectiveWE = [game.Board.Side.West, game.Board.Side.East]
    self.players[id1].objectives = objectiveNS
    self.players[id2].objectives = objectiveWE
    return player1, player2

  def client_disconnected(self, event):
    assert event.id in self.players

    player = self.players.pop(event.id, None)
    if player.playing():
      reply = DisqualifyPlayerEvent(player, Disqualification.QuitGame)
      event.event_queue.publish(reply)

  def player_name(self, event):
    player = self.players[event.id]
    player.rename(event.name)

  async def player_move(self, event):
    player = self.players[event.id]
    x = event.x
    y = event.y
    orientation = event.orientation

    try:
      self.game.make_turn(player, self.game.current_piece, x, y, orientation)
      reply = MoveAcceptedEvent(self.game, player, x, y, orientation,
                                self.game.current_piece)
    except GameException as e:
      reply = DisqualifyPlayerEvent(player, Disqualification.InvalidMove)

    await event.event_queue.publish(reply)

  async def player_cannot_move(self, event):
    player = self.players[event.id]

    if self.game.is_over():
      reply = GameIsOverEvent()
    else:
      reply = DisqualifyPlayerEvent(player, Disqualification.InvalidMove)

    await event.event_queue.publish(reply)

  async def game_started(self, event):
    self.game = event.game
    for gameplayer in self.game.players:
      gameplayer.join(self.game)

    reply = FirstTurnEvent(self.game, self.game.current_piece)
    await event.event_queue.publish(reply)

  async def disqualify_player(self, event):
    for gameplayer in self.game.players.values():
      gameplayer.leave(self.game)

    reply = GameCancelledEvent(self.game, event.reason)
    self.game = None
    await event.event_queue.publish(reply)

    reply = LaunchGameEvent()
    await event.event_queue.publish(reply)

  async def game_is_over(self, event):
    for gameplayer in self.game.players:
      gameplayer.leave(self.game)

    winner, scores = self.game.winner()
    reply = GameEndedEvent(winner, scores)
    self.game = None
    await event.event_queue.publish(reply)

    reply = LaunchGameEvent()
    await event.event_queue.publish(reply)
