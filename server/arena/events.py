from eventing.event_queue import Event
from .serializers import *


class LaunchGameEvent(Event):
  """Event to send when it may be possible
  that a new game can be launched

  Eg: is always sent when a player connects
  """


class GameStartedEvent(Event):
  """Sent when a new game was started"""
  def __init__(self, game):
    super().__init__()
    self.game = game

  def to_json(self):
    return {
      'type': 'gamestarted',
      'game': GameSerializer.serialize(self.game)
    }


class PlayerNameEvent(Event):
  """Sent when a player sends his name"""
  def __init__(self, player, name):
    super().__init__()
    self.player = player
    self.name = name


class PlayerMoveEvent(Event):
  """Sent when a player has sent a move"""
  def __init__(self, player, x, y, orientation):
    super().__init__()
    self.player = player
    self.x = x
    self.y = y
    self.orientation = orientation


class PlayerCannotMoveEvent(Event):
  """Sent when a player says he cannot move anymore"""
  def __init__(self, player):
    super().__init__()
    self.player = player


class BadMessageReceivedEvent(Event):
  """Sent when a player's message cannot be interpreted"""
  def __init__(self, player, content):
    super().__init__()
    self.player = player
    self.content = content


class DisqualifyPlayerEvent(Event):
  """Sent when a player is disqualified"""
  def __init__(self, player, reason):
    super().__init__()
    self.player = player
    self.reason = reason


class MoveAcceptedEvent(Event):
  """Sent when a player's move has been accepted"""
  def __init__(self, game, placed_piece, next_piece):
    super().__init__()
    self.game = game
    self.placed_piece = placed_piece
    self.next_piece = next_piece

  def to_json(self):
    return {
      'type': 'moveaccepted',
      'game': GameSerializer.serialize(self.game),
      'placed_piece': PlacedPieceSerializer.serialize(self.placed_piece),
      'next_piece': PieceSerializer.serialize(self.next_piece)
    }


class GameIsOverEvent(Event):
  """Sent when no more moves in a game are possible"""

  def to_json(self):
    return {
      'type': 'gameisover'
    }


class GameEndedEvent(Event):
  """Sent when a game has ended and scores and winner
  have been calculated
  """
  def __init__(self, winner, scores):
    super().__init__()
    self.winner = winner
    self.scores = scores

  def to_json(self):
    scores_serial = {player.id: score for player, score in self.scores.items()}

    return {
      'type': 'gameended',
      'winner': PlayerSerializer.serialize(self.winner),
      'scores': scores_serial
    }


class GameCancelledEvent(Event):
  """Sent when a game must be cancelled because of a disqualification"""
  def __init__(self, game, reason):
    super().__init__()
    self.game = game
    self.reason = reason

  def to_json(self):
    return {
      'type': 'gamecancelled',
      'game': GameSerializer.serialize(self.game),
      'reason': EnumSerializer.serialize(self.reason)
    }


class FirstTurnEvent(Event):
  """Sent when the first turn should be made"""
  def __init__(self, game, piece):
    super().__init__()
    self.game = game
    self.piece = piece

  def to_json(self):
    return {
      'type': 'firstturn',
      'game': GameSerializer.serialize(self.game),
      'piece': PieceSerializer.serialize(self.piece)
    }
