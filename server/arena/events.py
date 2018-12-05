from eventing.event_queue import Event


class LaunchGameEvent(Event):
  """Event to send when it may be possible
  that a new game can be launched

  Eg: is always sent when a player connects
  """


class GameStartedEvent(Event):
  """Sent when a new game was started"""
  def __init__(self, game):
    self.game = game


class DisqualifyPlayerEvent(Event):
  """Sent when a player is disqualified"""
  def __init__(self, player, reason):
    self.player = player
    self.reason = reason


class MoveAcceptedEvent(Event):
  """Sent when a player's move has been accepted"""
  def __init__(self, game, player, x, y, orientation):
    self.game = game
    self.player = player
    self.x = x
    self.y = y
    self.orientation = orientation


class GameIsOverEvent(Event):
  """Sent when no more moves in a game are possible"""


class GameEndedEvent(Event):
  """Sent when a game has ended and scores and winner
  have been calculated
  """
  def __init__(self, winner, scores):
    self.winner = winner
    self.scores = scores


class GameCancelledEvent(Event):
  """Sent when a game must be cancelled because of a disqualification"""
  def __init__(self, game, reason):
    self.game = game
    self.reason = reason


class FirstTurnEvent(Event):
  """Sent when the first turn should be made"""
  def __init__(self, game, piece):
    self.game = game
    self.piece = piece
