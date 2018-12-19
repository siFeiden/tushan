import unittest

from arena.logic.game import Board, InvalidPlacementError, Player
from arena.logic.piece import Orientation, Piece


class InitialPlacementsTest(unittest.TestCase):
  def setUp(self):
    self.piece1 = Piece(1, 3, [1, 7])
    self.piece2 = Piece(4, 4, [0])
    self.board = Board(8)

  def test_valid_initial_placement(self):
    placed_piece = self.board.place_initial(self.piece1, 3, 1, Orientation.South, None)
    self.assertIsNotNone(placed_piece)

  def test_valid_initial_placement_all_orientations(self):
    for o in Orientation:
      with self.subTest(orientation=o):
        board = Board(8)
        placed_piece = board.place_initial(self.piece1, 4, 4, o, None)
        self.assertIsNotNone(placed_piece)

  def test_initial_piece_large_area(self):
    placed_piece = self.board.place_initial(self.piece2, 2, 2, Orientation.South, None)
    self.assertIsNotNone(placed_piece)

  def test_invalid_initial_placement_far_away(self):
    with self.assertRaises(InvalidPlacementError):
      self.board.place_initial(self.piece1, 0, 0, Orientation.South, None)

  def test_invalid_initial_placement_close_by(self):
    with self.assertRaises(InvalidPlacementError):
      self.board.place_initial(self.piece1, 3, 6, Orientation.East, None)

  def test_invalid_initial_placement_out_of_board_but_in_initial_area(self):
    with self.assertRaises(InvalidPlacementError):
      board = Board(4)
      board.place_initial(self.piece2, 1, 1, Orientation.South, None)

  def test_initial_piece_placed_twice(self):
    self.board.place_initial(self.piece1, 3, 3, Orientation.South, None)

    with self.assertRaises(InvalidPlacementError):
      self.board.place_initial(self.piece1, 4, 3, Orientation.South, None)
