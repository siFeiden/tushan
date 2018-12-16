import unittest

from arena.logic.game import Board, InvalidPlacementError, Player
from arena.logic.piece import Orientation, Piece


class OutOfBoardTest(unittest.TestCase):
  def setUp(self):
    self.piece1 = Piece(1, 3, [0, 1, 2, 3, 4, 5, 6, 7])
    self.piece2 = Piece(2, 2, [0, 1, 2, 3, 4, 5, 6, 7])
    self.board = Board(4)
    self.player = Player(1, [0, 1])
    self.board.place_simple_initial(self.piece1, self.player)

  def test_completely_left_out_of_board_placement(self):
    with self.assertRaises(InvalidPlacementError):
      # out of board to the left
      self.board.place(self.piece1, -1, 0, Orientation.South, None)

  def test_completely_right_out_of_board_placement(self):
    with self.assertRaises(InvalidPlacementError):
      # out of board to the right
      self.board.place(self.piece1, 4, 3, Orientation.North, None)

  def test_completely_top_out_of_board_placement(self):
    with self.assertRaises(InvalidPlacementError):
      # out of board to the top
      self.board.place(self.piece1, 0, 0, Orientation.East, None)

  def test_completely_bottom_out_of_board_placement(self):
    with self.assertRaises(InvalidPlacementError):
      # out of board to the bottom
      self.board.place(self.piece1, 4, 4, Orientation.West, None)

  def test_slightly_left_out_of_board_placement(self):
    with self.assertRaises(InvalidPlacementError):
      # out of board to the left
      self.board.place(self.piece2, 1, 1, Orientation.West, None)

  def test_slightly_right_out_of_board_placement(self):
    with self.assertRaises(InvalidPlacementError):
      # out of board to the right
      self.board.place(self.piece2, 3, 3, Orientation.East, None)

  def test_slightly_top_out_of_board_placement(self):
    with self.assertRaises(InvalidPlacementError):
      # out of board to the top
      self.board.place(self.piece1, 0, -2, Orientation.South, None)

  def test_slightly_bottom_out_of_board_placement(self):
    with self.assertRaises(InvalidPlacementError):
      # out of board to the bottom
      self.board.place(self.piece1, 1, 5, Orientation.North, None)
