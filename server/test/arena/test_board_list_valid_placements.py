import unittest

from arena.game import Board
from arena.piece import Orientation, Piece


class ValidPlacementsTest(unittest.TestCase):
  def setUp(self):
    self.piece1 = Piece(2, 2, [2, 5])
    self.piece2 = Piece(1, 3, [0, 1, 4])

  def test_list_valid_placements(self):
    board = Board(8)
    board.place_initial(self.piece1)

    placements = list(board.valid_placements(self.piece2))

    for placed_piece in placements:
      self.assertIsNone(board.validate_placement(placed_piece))

    expected_placements = [
      (5, 4, Orientation.East),
      (6, 4, Orientation.North),
      (8, 3, Orientation.West),
      (3, 5, Orientation.South),
      (3, 6, Orientation.East),
      (4, 8, Orientation.North)
    ]

    for expected_placement in expected_placements:
      ok = any(expected_placement == (p.x, p.y, p.orientation) for p in placements)
      self.assertTrue(ok)
