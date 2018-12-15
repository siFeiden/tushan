import unittest

from arena.logic.game import Board, InvalidPlacementError
from arena.logic.piece import Orientation, Piece


class NonConnectionPiecesBoardTest(unittest.TestCase):
  def setUp(self):
    self.piece1 = Piece(2, 2, [2, 3, 7])
    self.piece2 = Piece(1, 3, [1, 2])
    self.piece3 = Piece(1, 3, [0, 7])

    self.board1 = Board(8)
    self.board1.place_initial(self.piece1)

    self.board2 = Board(8)
    self.board2.place_initial(self.piece1)
    self.board2.place(self.piece3, 5, 4, Orientation.East, None)

  def test_pieces_too_far_apart_1(self):
    with self.assertRaises(InvalidPlacementError):
      self.board1.place(self.piece2, 1, 1, Orientation.South, None)

  def test_pieces_too_far_apart_2(self):
    with self.assertRaises(InvalidPlacementError):
      self.board1.place(self.piece2, 4, 7, Orientation.East, None)

  def test_pieces_too_far_apart_3(self):
    with self.assertRaises(InvalidPlacementError):
      self.board1.place(self.piece2, 7, 3, Orientation.North, None)

  def test_no_connectors_1(self):
    with self.assertRaises(InvalidPlacementError):
      self.board1.place(self.piece2, 3, 0, Orientation.South, None)

  def test_no_connectors_2(self):
    with self.assertRaises(InvalidPlacementError):
      self.board1.place(self.piece2, 2, 3, Orientation.East, None)

  def test_connectors_mismatch_1(self):
    with self.assertRaises(InvalidPlacementError):
      self.board1.place(self.piece2, 3, 2, Orientation.South, None)

  def test_connectors_mismatch_2(self):
    with self.assertRaises(InvalidPlacementError):
      self.board1.place(self.piece2, 3, 6, Orientation.North, None)

  def test_connectors_mismatch_3(self):
    with self.assertRaises(InvalidPlacementError):
      self.board1.place(self.piece2, 5, 2, Orientation.South, None)

  def test_multi_piece_connector_mismatch(self):
    with self.assertRaises(InvalidPlacementError):
      self.board2.place(self.piece2, 5, 5, Orientation.South, None)
