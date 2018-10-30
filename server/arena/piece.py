from enum import Enum

from ._shapes import Point, Rect


class Orientation(Enum):
  North = 'north'
  East  = 'east'
  South = 'south'
  West  = 'west'


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

  @staticmethod
  def official_pieces():
    connectors = [
      [0, 3, 4], [1, 6, 7], [3, 5, 6], [0, 2, 3],
      [1, 3, 6], [0, 1, 7], [1, 4, 5], [3, 4, 7],
      [0, 2, 4], [0, 3, 5], [0, 4, 5], [0, 1, 2],
      [3, 5, 7], [1, 3, 5], [1, 2, 3], [2, 5, 6],
      [3, 6, 7], [1, 2, 4], [0, 2, 7], [0, 2, 6],
      [1, 3, 4], [2, 6, 7], [1, 4, 6], [2, 4, 7],
      [0, 1, 6], [1, 2, 5], [4, 5, 7], [0, 6, 7],
    ]

    return [Piece(1, 3, c) for c in connectors]


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
    commmon_docks = docks.keys() & other_docks.keys()

    assert len(docks) > 0, 'no docking points'
    assert len(other_docks) > 0, 'no other docking points'

    if len(commmon_docks) == 0:
      return False

    are_docks_compatible = all(docks[p] == other_docks[p] for p in commmon_docks)
    has_connector_match = any(docks[p] and other_docks[p] for p in commmon_docks)
    return are_docks_compatible and has_connector_match

  def docking_points(self):
    """Calculate the points where this piece can connect to another piece.

    Returns a map from points to bool: the map's value is True iff the
    point is a docking point.
    """
    docking_points = {}
    origin = Point(self.x, self.y)
    w = self.piece.width
    h = self.piece.height
    e1, e2 = self.units_for_orientation()

    is_connector = (n in self.piece.connectors for n in range(2*w*2*h))

    # top edge
    top_left = origin + e1 * 0.5
    for (x, y) in top_left.ray(e1, steps=w):
      docking_points[(x, y)] = next(is_connector)

    # right edge
    top_right = origin + e1 * w + e2 * 0.5
    for (x, y) in top_right.ray(e2, steps=h):
      docking_points[(x, y)] = next(is_connector)

    # bottom edge, right to left
    bottom_right = origin + e1 * w + e2 * h - e1 * 0.5
    for (x, y) in bottom_right.ray(-e1, steps=w):
      docking_points[(x, y)] = next(is_connector)

    # left edge, bottom to top
    bottom_left = origin + e2 * h - e2 * 0.5
    for (x, y) in bottom_left.ray(-e2, steps=h):
      docking_points[(x, y)] = next(is_connector)

    return docking_points

  def units_for_orientation(self):
    """Return the unit vectors for this piece's area according to the current orientation.

    The first vector points towards the second point of the rectangle
    in clockwise direction. The first vector points towards the fourth
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
