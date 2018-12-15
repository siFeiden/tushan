import unittest

from arena.logic.piece import DockingPoint, Orientation, Piece, PlacedPiece


class PieceTest(unittest.TestCase):
  """
    1  2 2  3  4 4  5 5  6  7
  1 +--+ +--+--+ +--+ +--+
    |  > <  |  | |  | |p5>
  2 +--+ +--+--+ +--+ +v^+--+
    |p1> <  p2 | |p3> <  |  |
  3 +--+ +--+--+ +--+ +--+--+
    |  > <  |  | <  > <  p4 |
  4 +v-+ +--+v-+ +--+ +v-+v-+
  4 +^-+--^-+--+----+--^-+^-+
    |  p6: orient. west     |
  5 +--+----+--+----+----+--+
  """
  def setUp(self):
    piece1 = Piece(1, 3, [1, 2, 3, 4])
    self.placed_piece1 = PlacedPiece(piece1, 1, 1, Orientation.South, None)

    piece2 = Piece(2, 3, [5, 7, 8, 9])
    self.placed_piece2 = PlacedPiece(piece2, 2, 1, Orientation.South, None)

    piece3 = Piece(1, 3, [2, 3, 5])
    self.placed_piece3 = PlacedPiece(piece3, 4, 1, Orientation.South, None)

    piece4 = Piece(2, 2, [0, 4, 5 , 6, 7])
    self.placed_piece4 = PlacedPiece(piece4, 5, 2, Orientation.South, None)

    piece5 = Piece(1, 1, [1, 2])
    self.placed_piece5 = PlacedPiece(piece5, 5, 1, Orientation.South, None)
    self.pp5_west = PlacedPiece(piece5, 5, 1, Orientation.West, None)
    self.pp5_north = PlacedPiece(piece5, 5, 1, Orientation.North, None)
    self.pp5_east = PlacedPiece(piece5, 5, 1, Orientation.East, None)

    piece6 = Piece(1, 6, [8, 9, 12, 13])
    self.placed_piece6 = PlacedPiece(piece6, 7, 4, Orientation.West, None)

  def test_p1_docking_points(self):
    expected_docks = {
      DockingPoint(1.5, 1.0, False),
      DockingPoint(2.0, 1.5, True),
      DockingPoint(2.0, 2.5, True),
      DockingPoint(2.0, 3.5, True),
      DockingPoint(1.5, 4.0, True),
      DockingPoint(1.0, 3.5, False),
      DockingPoint(1.0, 2.5, False),
      DockingPoint(1.0, 1.5, False),
    }

    docks = self.placed_piece1.docking_points()
    self.assertSetEqual(expected_docks, docks)

  def test_p4_docking_points(self):
    expected_docks = {
      DockingPoint(5.5, 2.0, True),
      DockingPoint(6.5, 2.0, False),
      DockingPoint(7.0, 2.5, False),
      DockingPoint(7.0, 3.5, False),
      DockingPoint(6.5, 4.0, True),
      DockingPoint(5.5, 4.0, True),
      DockingPoint(5.0, 3.5, True),
      DockingPoint(5.0, 2.5, True),
    }

    docks = self.placed_piece4.docking_points()
    self.assertSetEqual(expected_docks, docks)

  def test_p5_docking_points(self):
    expected_docks = {
      DockingPoint(5.5, 1.0, False),
      DockingPoint(6.0, 1.5, True),
      DockingPoint(5.5, 2.0, True),
      DockingPoint(5.0, 1.5, False),
    }

    docks = self.placed_piece5.docking_points()
    self.assertSetEqual(expected_docks, docks)

  def test_p5_west_docking_points(self):
    expected_docks = {
      DockingPoint(5.0, 1.5, False),
      DockingPoint(4.5, 2.0, True),
      DockingPoint(4.0, 1.5, True),
      DockingPoint(4.5, 1.0, False),
    }

    docks = self.pp5_west.docking_points()
    self.assertSetEqual(expected_docks, docks)

  def test_p5_north_docking_points(self):
    expected_docks = {
      DockingPoint(4.5, 1.0, False),
      DockingPoint(4.0, 0.5, True),
      DockingPoint(4.5, 0.0, True),
      DockingPoint(5.0, 0.5, False),
    }

    docks = self.pp5_north.docking_points()
    self.assertSetEqual(expected_docks, docks)

  def test_p5_east_docking_points(self):
    expected_docks = {
      DockingPoint(5.0, 0.5, False),
      DockingPoint(5.5, 0.0, True),
      DockingPoint(6.0, 0.5, True),
      DockingPoint(5.5, 1.0, False),
    }

    docks = self.pp5_east.docking_points()
    self.assertSetEqual(expected_docks, docks)

  def test_p1_connects_to_p2(self):
    self.assertTrue(self.placed_piece1.connects_to(self.placed_piece2))
    self.assertTrue(self.placed_piece2.connects_to(self.placed_piece1))

  def test_p1_not_connects_to_p3(self):
    self.assertFalse(self.placed_piece1.connects_to(self.placed_piece3))
    self.assertFalse(self.placed_piece3.connects_to(self.placed_piece1))

  def test_p2_not_connects_to_p3(self):
    self.assertFalse(self.placed_piece2.connects_to(self.placed_piece3))
    self.assertFalse(self.placed_piece3.connects_to(self.placed_piece2))

  def test_p3_connects_to_p4(self):
    self.assertTrue(self.placed_piece3.connects_to(self.placed_piece4))
    self.assertTrue(self.placed_piece4.connects_to(self.placed_piece3))

  def test_p3_not_connects_to_p5(self):
    self.assertFalse(self.placed_piece3.connects_to(self.placed_piece5))
    self.assertFalse(self.placed_piece5.connects_to(self.placed_piece3))

  def test_p4_connects_to_p5(self):
    self.assertTrue(self.placed_piece4.connects_to(self.placed_piece5))
    self.assertTrue(self.placed_piece5.connects_to(self.placed_piece4))

  def test_p4_not_connects_to_p5_west(self):
    self.assertFalse(self.placed_piece4.connects_to(self.pp5_west))
    self.assertFalse(self.pp5_west.connects_to(self.placed_piece4))

  def test_p1_connects_to_p6(self):
    self.assertTrue(self.placed_piece1.connects_to(self.placed_piece6))
    self.assertTrue(self.placed_piece6.connects_to(self.placed_piece1))

  def test_p2_not_connects_to_p6(self):
    self.assertFalse(self.placed_piece2.connects_to(self.placed_piece6))
    self.assertFalse(self.placed_piece6.connects_to(self.placed_piece2))

  def test_p3_not_connects_to_p6(self):
    self.assertFalse(self.placed_piece3.connects_to(self.placed_piece6))
    self.assertFalse(self.placed_piece6.connects_to(self.placed_piece3))

  def test_p4_connects_to_p6(self):
    self.assertTrue(self.placed_piece4.connects_to(self.placed_piece6))
    self.assertTrue(self.placed_piece6.connects_to(self.placed_piece4))
