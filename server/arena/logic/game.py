from collections import Counter, deque
from enum import Enum

from .piece import Orientation, Piece, PieceConnection, PlacedPiece
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

  def place_simple_initial(self, piece, owner):
    center = self.size // 2 - 1
    self.place_initial(piece, center, center, Orientation.South, owner)

  def place_initial(self, piece, x, y, orientation, owner):
    """Place the first stone on the board.

    Collisions and connections with other stones are not checked
    but piece must be placed in the middle of the board.
    """
    placed_piece = PlacedPiece(piece, x, y, orientation, owner)

    if len(self.pieces) > 0:
      raise InvalidPlacementError('Only one initial piece can be placed')

    if not self.contains(placed_piece):
      raise InvalidPlacementError('Piece not in board')

    if not self.overlaps_initial_area(placed_piece):
      raise InvalidPlacementError('Initial piece must be placed in center of board')

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

  def overlaps_initial_area(self, piece):
    """Check if piece is in the area the inital piece must overlap.

    This area contains the four central cells on a board of even size.
    """
    center = self.size // 2
    center_area = Rect.of(center - 1, center - 1, center + 1, center + 1)
    return center_area.overlaps(piece.area())

  def contains(self, piece):
    """Check if the board's area contains piece."""
    board_area = Rect.of(0, 0, self.size, self.size)
    return board_area.contains_rect(piece.area())

  def collides_any(self, piece):
    """Check if piece collides with any piece on the board."""
    return any(piece.collides(placed) for placed in self.pieces)

  def connects_one(self, piece):
    """Check if piece connects to any piece on the board."""
    connections = [piece.connects_to(placed) for placed in self.pieces]

    return (PieceConnection.Incompatible not in connections and
            PieceConnection.Match in connections)

  def valid_placements(self, piece):
    yield from ValidPlacements(self, piece)


class Player(object):
  def __init__(self, id):
    self.id = id

  def __eq__(self, other):
    return self.id == other.id

  def __hash__(self):
    return hash(self.id)


class Game(object):
  def __init__(self, board, players, objectives, pieces):
    self.board = board
    self.players = deque(players)
    self.objectives = objectives
    self.pieces = deque(pieces)

    assert len(self.pieces) > 0, 'game needs at least one piece'
    assert len(self.players) >= 2, 'game needs at least two players'
    assert len(objectives) == len(players), 'each player needs objectives'
    assert all(len(objectives[p]) == 2 for p in players), 'each player needs two board sides'

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

    if len(self.board.pieces) == 0:
      placed_piece = self.board.place_initial(piece, x, y, orientation, player)
    else:
      placed_piece = self.board.place(piece, x, y, orientation, player)
    self.prepare_next_turn()
    return placed_piece

  def prepare_next_turn(self):
    self.players.rotate()
    self.pieces.popleft()

  def is_over(self):
    no_more_pieces = len(self.pieces) == 0
    if no_more_pieces:
      return True

    valid_placements = self.board.valid_placements(self.current_piece)
    no_more_placements = len(list(valid_placements)) == 0
    return no_more_placements

  def scores(self):
    sides = Counter(dock.board_side(self.board)
                    for placed_piece in self.board.pieces
                    for dock in placed_piece.docking_points()
                    if dock.is_connector)

    scores = {}
    for player in self.players:
      side1, side2 = self.objectives[player]
      scores[player] = sides[side1] * sides[side2]

    return scores
