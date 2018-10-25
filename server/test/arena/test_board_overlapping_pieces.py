import unittest

from arena.game import Board, InvalidPlacementError, Piece, Orientation

class OverlappingPiecesBoardTest(unittest.TestCase):
  def setUp(self):
    self.piece1 = Piece(2, 2, [0, 1, 2, 3, 4, 5, 6, 7])
    self.piece2 = Piece(1, 3, [0, 1, 2, 3, 4, 5, 6, 7])
    self.board = Board(8, self.piece1)

  def test_overlap_left_placement(self):
    with self.assertRaises(InvalidPlacementError):
      self.board.place(self.piece2, 2, 5, Orientation.East, None)

  def test_overlap_right_placement(self):
    with self.assertRaises(InvalidPlacementError):
      self.board.place(self.piece2, 6, 3, Orientation.West, None)

  def test_overlap_top_placement(self):
    with self.assertRaises(InvalidPlacementError):
      self.board.place(self.piece2, 3, 1, Orientation.South, None)

  def test_overlap_bottom_placement(self):
    with self.assertRaises(InvalidPlacementError):
      self.board.place(self.piece2, 4, 7, Orientation.North, None)
