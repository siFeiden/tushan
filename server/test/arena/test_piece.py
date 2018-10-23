import unittest

from arena.game import Piece, PlacedPiece, Orientation


class PieceTest(unittest.TestCase):
  """
    1  2 2  3  4 4  5 5  6  7
  1 +--+ +--+--+ +--+ +--+
    |  > <  |  | |  | |p5>
  2 +--+ +--+--+ +--+ +v^+--+
    |p1> <  p2 | |p3> <  |  |
  3 +--+ +--+--+ +--+ +--+--+
    |  > <  |  | <  > <  p4 |
  4 +--+ +==+==+ +--+ +--+--+
  """
  def setUp(self):
    piece1 = Piece(1, 3, [1, 2, 3])
    self.placed_piece1 = PlacedPiece(piece1, 1, 1, Orientation.South, None)

    piece2 = Piece(2, 3, [7, 8, 9])
    self.placed_piece2 = PlacedPiece(piece2, 2, 1, Orientation.South, None)

    piece3 = Piece(1, 3, [2, 3, 5])
    self.placed_piece3 = PlacedPiece(piece3, 4, 1, Orientation.South, None)

    piece4 = Piece(2, 2, [0, 6, 7])
    self.placed_piece4 = PlacedPiece(piece4, 5, 2, Orientation.South, None)

    piece5 = Piece(1, 1, [1, 2])
    self.placed_piece5 = PlacedPiece(piece5, 5, 1, Orientation.South, None)


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
