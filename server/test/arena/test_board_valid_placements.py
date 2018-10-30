import unittest

from arena.game import Board
from arena.piece import Orientation, Piece


class ValidPlacementsTest(unittest.TestCase):
  def setUp(self):
    self.piece1 = Piece(2, 2, [2, 5])
    self.piece2 = Piece(1, 3, [0, 1, 4])

  def test_valid_placement_p1c2_p2c0(self):
    board = Board(8, self.piece1)

    placed_piece = board.place(self.piece2, 5, 4, Orientation.East, None)
    self.assertIsNotNone(placed_piece)

  def test_valid_placement_p1c2_p2c1(self):
    board = Board(8, self.piece1)

    placed_piece = board.place(self.piece2, 6, 4, Orientation.North, None)
    self.assertIsNotNone(placed_piece)

  def test_valid_placement_p1c2_p2c4(self):
    board = Board(8, self.piece1)

    placed_piece = board.place(self.piece2, 8, 3, Orientation.West, None)
    self.assertIsNotNone(placed_piece)

  def test_valid_placement_p1c5_p2c0(self):
    board = Board(8, self.piece1)

    placed_piece = board.place(self.piece2, 3, 5, Orientation.South, None)
    self.assertIsNotNone(placed_piece)

  def test_valid_placement_p1c5_p2c1(self):
    board = Board(8, self.piece1)

    placed_piece = board.place(self.piece2, 3, 6, Orientation.East, None)
    self.assertIsNotNone(placed_piece)

  def test_valid_placement_p1c5_p2c4(self):
    board = Board(8, self.piece1)

    placed_piece = board.place(self.piece2, 4, 8, Orientation.North, None)
    self.assertIsNotNone(placed_piece)
