from enum import Enum

from ._shapes import Point, Rect


class Orientation(Enum):
  North = 'north'
  East  = 'east'
  South = 'south'
  West  = 'west'


class PieceConnection(Enum):
  Match = 'match' # Pieces have at least two matching connectors
  Neutral = 'neutral' # Pieces fit next to each other but have no match
  Incompatible = 'incompatible' # Pieces are incompatible

  def __bool__(self):
    """A PieceConnection is truthy if it is a match.
    Implemented for backwards compatibility.
    """
    return self == PieceConnection.Match


class DockingPoint(object):
  def __init__(self, x, y, is_connector):
    self.x = x
    self.y = y
    self.is_connector = is_connector

  def board_side(self, board):
    if self.x == 0:
      return board.Side.West
    if self.y == 0:
      return board.Side.North
    if self.x == board.size:
      return board.Side.East
    if self.y == board.size:
      return board.Side.South

    return None

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __hash__(self):
    return hash((self.x, self.y))


class Piece(object):
  """A piece before it is placed on the board.

  Its implicit orientation is South.
  """
  def __init__(self, width, height, connectors):
    self.width = width
    self.height = height
    self.connectors = connectors

    assert width > 0, 'width must be positive'
    assert height > 0, 'height must be positive'
    assert all(0 <= c < 2*width+2*height for c in connectors), 'invalid connector'


class PlacedPiece(object):
  def __init__(self, piece, x, y, orientation, player):
    self.piece = piece
    self.x = x
    self.y = y
    self.orientation = orientation
    self.player = player

    assert Orientation(orientation), 'invalid orientation'

  def area(self):
    """Return a Rect describing the area of this piece"""
    w = self.piece.width
    h = self.piece.height
    origin = Point(self.x, self.y)
    e1, e2 = self.units_for_orientation()

    return Rect(origin, origin + e1 * w + e2 * h)

  def collides(self, other):
    """Check if this piece collides with/ overlaps another piece."""
    return self.area().overlaps(other.area())

  def connects_to(self, other):
    """Check if this piece connects to another piece."""
    docks = self.docking_points()
    other_docks = other.docking_points()
    commmon_docks = docks & other_docks

    assert len(docks) > 0, 'no docking points'
    assert len(other_docks) > 0, 'no other docking points'

    if len(commmon_docks) == 0:
      return PieceConnection.Neutral

    connectors = {d for d in docks if d.is_connector}
    other_connectors = {d for d in other_docks if d.is_connector}

    docks_compatible = len((commmon_docks & connectors) ^ (commmon_docks & other_connectors)) == 0
    connector_match = len(connectors & other_connectors) > 0

    if not docks_compatible:
      return PieceConnection.Incompatible

    if connector_match:
      return PieceConnection.Match
    else:
      return PieceConnection.Neutral

  def docking_points(self):
    """Calculate the points where this piece can connect to another piece.

    Returns a set of DockingPoints.
    """
    docking_points = set()
    origin = Point(self.x, self.y)
    w = self.piece.width
    h = self.piece.height
    e1, e2 = self.units_for_orientation()

    is_connector = (n in self.piece.connectors for n in range(2*w*2*h))

    # top edge
    top_left = origin + e1 * 0.5
    for (x, y) in top_left.ray(e1, steps=w):
      docking_points.add(DockingPoint(x, y, next(is_connector)))

    # right edge
    top_right = origin + e1 * w + e2 * 0.5
    for (x, y) in top_right.ray(e2, steps=h):
      docking_points.add(DockingPoint(x, y, next(is_connector)))

    # bottom edge, right to left
    bottom_right = origin + e1 * w + e2 * h - e1 * 0.5
    for (x, y) in bottom_right.ray(-e1, steps=w):
      docking_points.add(DockingPoint(x, y, next(is_connector)))

    # left edge, bottom to top
    bottom_left = origin + e2 * h - e2 * 0.5
    for (x, y) in bottom_left.ray(-e2, steps=h):
      docking_points.add(DockingPoint(x, y, next(is_connector)))

    return docking_points

  def units_for_orientation(self):
    """Return the unit vectors for this piece's area according to the current orientation.

    The first vector points towards the second point of the rectangle
    in clockwise direction. The second vector points towards the fourth
    point of the rectangle in clockwise direction:
    --> e1
    x--+--+ | e2
    |  |  | v
    +--+--+
    """
    ex = Point(1, 0)
    ey = Point(0, 1)

    if self.orientation == Orientation.North:
      return (-ex, -ey)
    elif self.orientation == Orientation.East:
      return (-ey, ex)
    elif self.orientation == Orientation.South:
      return (ex, ey)
    elif self.orientation == Orientation.West:
      return (ey, -ex)

    assert Orientation(self.orientation), 'invalid orientation'
