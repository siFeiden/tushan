from collections import deque
from enum import Enum

from _shapes import Point, Rect


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

    raise ValueError('Invalid orientation given')

  def collides(self, other):
    area = Rect.of(self.x, self.y, *self.other_corner())
    other_area = Rect.of(other.x, other.y, *other.other_corner())
    return area.overlaps(other_area)

  def connects_to(self, other):
    docking_points = self.docking_points()
    other_docking_points = other.docking_points()
    commmon_docking_points = docking_points.keys() & other_docking_points.keys()

    return all(docking_points[c] == other_docking_points[c] for connector in commmon_docking_points)

  def docking_points(self):
    docking_points = []
    n = 0

    x = self.x + 0.5
    y = self.y
    w = self.piece.width - 1
    h = self.piece.height - 1

    for i in range(self.piece.w):
      is_connector = n in self.piece.connectors
      docking_points[(x, y)] = is_connector
      x += 1
      n += 1

    x += 0.5
    y += 0.5

    for i in range(self.piece.h):
      is_connector = n in self.piece.connectors
      docking_points[(x, y)] = is_connector
      y += 1
      n += 1

    x -= 0.5
    y += 0.5

    for i in range(self.piece.w):
      is_connector = n in self.piece.connectors
      docking_points[(x, y)] = is_connector
      x -= 1
      n += 1

    x -= 0.5
    y -= 0.5

    for i in range(self.piece.h):
      is_connector = n in self.piece.connectors
      docking_points[(x, y)] = is_connector
      y -= 1
      n += 1

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

  def place(self, piece, x, y, orientation, player):
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
    return 1 == sum(piece.connects_to(placed) for placed in self.piece)


class Player(object):
  def __init__(self, id):
    self.id = id


class Game(object):
  def __init__(self, players, objectives):
    self.players = deque(players)
    self.objectives = objectives


