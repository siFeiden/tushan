from collections import Counter, deque
from enum import Enum

from .piece import Orientation, Piece, PlacedPiece
from .placements import ValidPlacements
from ._shapes import Point, Rect


class GameException(Exception):
  pass


class InvalidPlacementError(GameException):
  pass


class NotPlayersTurnError(GameException):
  pass


class WrongPiecePlayedError(GameException):
  pass


class Board(object):
  class Side(Enum):
    North = 'north'
    East  = 'east'
    South = 'south'
    West  = 'west'

  def __init__(self, size):
    self.size = size
    self.pieces = []

    assert size > 0, 'field size must be positive'
    assert size % 2 == 0, 'field size not even'

  def place_initial(self, piece, owner):
    """Place the first stone on the board.

    Collisions and connections with other stones are not checked
    """
    center = self.size // 2 - 1
    placed_piece = PlacedPiece(piece, center, center, Orientation.South, owner)

    if not self.contains(placed_piece):
      raise InvalidPlacementError()

    self.pieces.append(placed_piece)
    return placed_piece

  def validate_placement(self, placed_piece):
    """Check if a stone can be placed on the board.

    Raise InvalidPlacementError if placement is not valid.
    """

    if not self.contains(placed_piece):
      raise InvalidPlacementError('Piece not in board')

    if self.collides_any(placed_piece):
      raise InvalidPlacementError('Pieces overlap')

    if not self.connects_one(placed_piece):
      raise InvalidPlacementError('Piece does not connect')

  def place(self, piece, x, y, orientation, player):
    """Place a stone on the board."""
    assert Orientation(orientation), 'invalid orientation'

    placed_piece = PlacedPiece(piece, x, y, orientation, player)
    self.validate_placement(placed_piece)
    self.pieces.append(placed_piece)
    return placed_piece

  def contains(self, piece):
    """Check if the board's area contains piece."""
    board_area = Rect.of(0, 0, self.size, self.size)
    return board_area.contains_rect(piece.area())

  def collides_any(self, piece):
    """Check if piece collides with any piece on the board."""
    return any(piece.collides(placed) for placed in self.pieces)

  def connects_one(self, piece):
    """Check if piece connects to any piece on the board."""
    return any(piece.connects_to(placed) for placed in self.pieces)

  def valid_placements(self, piece):
    yield from ValidPlacements(self, piece)


class Player(object):
  def __init__(self, id, objectives):
    self.id = id
    self.objectives = objectives

    assert len(objectives) == 2, 'invalid player objectives'


class Game(object):
  def __init__(self, board, players, pieces):
    self.board = board
    self.players = deque(players)

    initial_piece, *playing_pieces = pieces
    # we give the initial piece a random owner to avoid None
    board.place_initial(initial_piece, self.current_player)
    self.pieces = deque(playing_pieces)

    assert len(self.pieces) > 0, 'game needs at least one piece'
    assert len(players) >= 2, 'game needs at least two players'

  @property
  def current_player(self):
    return self.players[0]

  @property
  def current_piece(self):
    return self.pieces[0]

  def make_turn(self, player, piece, x, y, orientation):
    if player != self.current_player:
      raise NotPlayersTurnError(player)

    if piece != self.current_piece:
      raise WrongPiecePlayedError(piece)

    placed_piece = self.board.place(piece, x, y, orientation, player)
    self.prepare_next_turn()
    return placed_piece

  def prepare_next_turn(self):
    self.players.rotate()
    self.pieces.popleft()

  def is_over(self):
    no_more_pieces = len(self.pieces) == 0
    no_more_placements = len(board.valid_placements(self.current_piece)) == 0
    return no_more_pieces or no_more_placements

  def scores(self):
    sides = Counter(dock.board_side(self.board)
                    for placed_piece in self.board.pieces
                    for dock in placed_piece.docking_points()
                    if dock.is_connector)

    scores = {}
    for player in self.players:
      side1, side2 = player.objectives
      scores[player] = sides[side1] * sides[side2]

    return scores
