from collections import deque
from enum import Enum

from ._shapes import Point, Rect


class Orientation(Enum):
  North = 'north'
  East  = 'east'
  South = 'south'
  West  = 'west'


class Piece(object):
  """A piece before it is placed on the board

  Its implicit orientation is South.
  """
  def __init__(self, width, height, connectors):
    self.width = width
    self.height = height
    self.connectors = connectors

    assert width > 0, 'width must be positive'
    assert height > 0, 'height must be positive'
    assert all(0 <= c < 2*width+2*height for c in connectors), 'invalid connector'

  @staticmethod
  def official_connectors():
    connectors = [
      [0, 3, 4], [1, 6, 7], [3, 5, 6], [0, 2, 3],
      [1, 3, 6], [0, 1, 7], [1, 4, 5], [3, 4, 7],
      [0, 2, 4], [0, 3, 5], [0, 4, 5], [0, 1, 2],
      [3, 5, 7], [1, 3, 5], [1, 2, 3], [2, 5, 6],
      [3, 6, 7], [1, 2, 4], [0, 2, 7], [0, 2, 6],
      [1, 3, 4], [2, 6, 7], [1, 4, 6], [2, 4, 7],
      [0, 1, 6], [1, 2, 5], [4, 5, 7], [0, 6, 7],
    ]

    return (Piece(1, 3, c) for c in connectors)


class PlacedPiece(object):
  def __init__(self, piece, x, y, orientation, player):
    self.piece = piece
    self.x = x
    self.y = y
    self.orientation = orientation
    self.player = player

    assert Orientation(orientation), 'invalid orientation'

  def other_corner(self):
    w = self.piece.width - 1
    h = self.piece.height - 1

    if self.orientation == Orientation.North:
      return (x - w, y - h)
    elif self.orientation == Orientation.East:
      return (x + h, y - w)
    elif self.orientation == Orientation.South:
      return (x + w, y + h)
    elif self.orientation == Orientation.West:
      return (x - h, y + w)

    assert Orientation(self.orientation), 'invalid orientation'

  def collides(self, other):
    area = Rect.of(self.x, self.y, *self.other_corner())
    other_area = Rect.of(other.x, other.y, *other.other_corner())
    return area.overlaps(other_area)

  def connects_to(self, other):
    docks = self.docking_points()
    other_docks = other.docking_points()
    commmon_docks = docks.keys() & other_docks.keys()

    assert len(docks) > 0, 'no docking points'
    assert len(other_docks) > 0, 'no other docking points'

    if len(commmon_docks) == 0:
      return False

    are_docks_compatible = all(docks[p] == other_docks[p] for p in commmon_docks)
    has_connector_match = any(docks[p] and other_docks[p] for p in commmon_docks)
    return are_docks_compatible and has_connector_match

  def docking_points(self):
    docking_points = {}
    w = self.piece.width
    h = self.piece.height
    e1 = Point(1.0, 0.0)
    e2 = Point(0.0, 1.0)

    # TODO consider orientation
    is_connector = (n in self.piece.connectors for n in range(2*w*2*h))

    # top edge
    top_left = Point(self.x + 0.5, self.y)
    for (x, y) in top_left.ray(e1, steps=w):
      docking_points[(x, y)] = next(is_connector)

    # right edge
    top_right = Point(self.x + w, self.y + 0.5)
    for (x, y) in top_right.ray(e2, steps=h):
      docking_points[(x, y)] = next(is_connector)

    # bottom edge, right to left
    bottom_right = Point(self.x + w - 0.5, self.y + h)
    for (x, y) in bottom_right.ray(-e1, steps=w):
      docking_points[(x, y)] = next(is_connector)

    # left edge, bottom to top
    bottom_left = Point(self.x, self.y + h - 0.5)
    for (x, y) in bottom_left.ray(-e2, steps=h):
      docking_points[(x, y)] = next(is_connector)

    return docking_points


class InvalidPlacementError(Exception):
  pass


class Board(object):
  class Side(Enum):
    North = 'north'
    East  = 'east'
    South = 'south'
    West  = 'west'

  def __init__(self, size, initial_piece):
    self.size = size
    self.pieces = []

    center = size // 2
    self.place(initial_piece, center, center - 1, Orientation.South, None)

    assert size > 0, 'field size must be positive'
    assert size % 2 == 0, 'field size not even'

  def place(self, piece, x, y, orientation, player):
    assert 0 <= x < self.size, 'piece placed outside the board'
    assert 0 <= y < self.size, 'piece placed outside the board'
    assert Orientation(orientation), 'invalid orientation'

    placed_piece = PlacedPiece(piece, x, y, orientation, player)

    if not self.contains(placed_piece):
      raise InvalidPlacementError()

    if self.collides_any(placed_piece):
      raise InvalidPlacementError()

    if not self.connects_one(placed_piece):
      raise InvalidPlacementError()

    self.pieces.append(placed_piece)
    return placed_piece

  def contains(self, piece):
    s = self.size - 1
    board_area = Rect.of(0, 0, s, s)

    corner1 = Point(piece.x, piece.y)
    corner2 = Point(*piece.other_corner())

    return board_area.contains(corner1) and board_area.contains(corner2)

  def collides_any(self, piece):
    return any(piece.collides(placed) for placed in self.piece)

  def connects_one(self, piece):
    return any(piece.connects_to(placed) for placed in self.piece)


class Player(object):
  def __init__(self, id):
    self.id = id


class Game(object):
  def __init__(self, players, objectives):
    self.players = deque(players)
    self.objectives = objectives

    assert len(players) >= 2, 'game needs at least two players'
    assert all(len(objectives[p]) == 2 for p in players), 'invalid player objectives'
